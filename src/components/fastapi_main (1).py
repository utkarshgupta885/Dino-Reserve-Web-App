from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import enum

# Database configuration
DATABASE_URL = "postgresql://user:password@localhost/dinoreserve"
# For local development with SQLite: DATABASE_URL = "sqlite:///./dinoreserve.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class ReservationStatus(str, enum.Enum):
    RESERVED = "reserved"
    CANCELLED = "cancelled"

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    dino_type = Column(String)  # Type of dino mascot
    
    tables = relationship("Table", back_populates="restaurant")

class Table(Base):
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    table_number = Column(Integer)
    capacity = Column(Integer)
    
    restaurant = relationship("Restaurant", back_populates="tables")
    reservations = relationship("Reservation", back_populates="table")

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    customer_name = Column(String)
    phone = Column(String)
    party_size = Column(Integer)
    reservation_time = Column(DateTime)
    status = Column(String, default="reserved")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    table = relationship("Table", back_populates="reservations")

# Pydantic Models
class RestaurantBase(BaseModel):
    name: str
    location: str
    dino_type: str

class RestaurantResponse(RestaurantBase):
    id: int
    
    class Config:
        from_attributes = True

class TableBase(BaseModel):
    table_number: int
    capacity: int

class TableWithStatus(TableBase):
    id: int
    restaurant_id: int
    is_reserved: bool
    current_reservation: Optional[dict] = None
    
    class Config:
        from_attributes = True

class ReservationCreate(BaseModel):
    table_id: int
    customer_name: str
    phone: str
    party_size: int
    reservation_time: datetime

class ReservationUpdate(BaseModel):
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    party_size: Optional[int] = None
    reservation_time: Optional[datetime] = None
    status: Optional[str] = None

class ReservationResponse(BaseModel):
    id: int
    table_id: int
    customer_name: str
    phone: str
    party_size: int
    reservation_time: datetime
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="Dino Reserve API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    
    # Seed initial data
    db = SessionLocal()
    if db.query(Restaurant).count() == 0:
        restaurants_data = [
            {"name": "T-Rex Tavern", "location": "Downtown Dino District", "dino_type": "trex"},
            {"name": "Bronto Bistro", "location": "Jurassic Junction", "dino_type": "bronto"},
            {"name": "Raptor Restaurant", "location": "Cretaceous Corner", "dino_type": "raptor"},
            {"name": "Stego Steakhouse", "location": "Triassic Trail", "dino_type": "stego"},
            {"name": "Pterodactyl Pub", "location": "Sky Valley", "dino_type": "ptero"}
        ]
        
        for r_data in restaurants_data:
            restaurant = Restaurant(**r_data)
            db.add(restaurant)
            db.flush()
            
            # Add 25 tables per restaurant
            for i in range(1, 26):
                capacity = 2 if i <= 10 else (4 if i <= 20 else 6)
                table = Table(
                    restaurant_id=restaurant.id,
                    table_number=i,
                    capacity=capacity
                )
                db.add(table)
        
        db.commit()
    db.close()

# API Endpoints
@app.get("/")
def root():
    return {"message": "🦕 Welcome to Dino Reserve API! 🦖"}

@app.get("/restaurants", response_model=List[RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    """Get all restaurants"""
    restaurants = db.query(Restaurant).all()
    return restaurants

@app.get("/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """Get a specific restaurant"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@app.get("/restaurants/{restaurant_id}/tables", response_model=List[TableWithStatus])
def get_tables(restaurant_id: int, db: Session = Depends(get_db)):
    """Get all tables for a restaurant with their reservation status"""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    tables = db.query(Table).filter(Table.restaurant_id == restaurant_id).all()
    
    result = []
    for table in tables:
        # Check for active reservation (today's reservations)
        active_reservation = db.query(Reservation).filter(
            Reservation.table_id == table.id,
            Reservation.status == "reserved",
            Reservation.reservation_time >= datetime.now().replace(hour=0, minute=0, second=0)
        ).first()
        
        reservation_data = None
        if active_reservation:
            reservation_data = {
                "id": active_reservation.id,
                "customer_name": active_reservation.customer_name,
                "phone": active_reservation.phone,
                "party_size": active_reservation.party_size,
                "reservation_time": active_reservation.reservation_time.isoformat(),
                "status": active_reservation.status
            }
        
        result.append({
            "id": table.id,
            "table_number": table.table_number,
            "capacity": table.capacity,
            "restaurant_id": table.restaurant_id,
            "is_reserved": active_reservation is not None,
            "current_reservation": reservation_data
        })
    
    return result

@app.post("/reservations", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    """Create a new reservation"""
    # Check if table exists
    table = db.query(Table).filter(Table.id == reservation.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Check if table is already reserved for this time
    existing = db.query(Reservation).filter(
        Reservation.table_id == reservation.table_id,
        Reservation.status == "reserved",
        Reservation.reservation_time == reservation.reservation_time
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Table already reserved for this time")
    
    # Check party size vs capacity
    if reservation.party_size > table.capacity:
        raise HTTPException(
            status_code=400, 
            detail=f"Party size exceeds table capacity ({table.capacity})"
        )
    
    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@app.put("/reservations/{reservation_id}", response_model=ReservationResponse)
def update_reservation(
    reservation_id: int, 
    reservation: ReservationUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing reservation"""
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    update_data = reservation.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reservation, field, value)
    
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@app.delete("/reservations/{reservation_id}")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """Cancel a reservation"""
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    db_reservation.status = "cancelled"
    db.commit()
    return {"message": "Reservation cancelled successfully", "id": reservation_id}

@app.get("/reservations")
def get_all_reservations(
    restaurant_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all reservations with optional filters"""
    query = db.query(Reservation).join(Table)
    
    if restaurant_id:
        query = query.filter(Table.restaurant_id == restaurant_id)
    
    if status:
        query = query.filter(Reservation.status == status)
    
    reservations = query.all()
    return reservations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
