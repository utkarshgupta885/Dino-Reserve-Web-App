"""
Database seeding script for Dino Reserve
Run this to populate the database with initial data and sample reservations
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

# Import models from main.py
from main import Base, Restaurant, Table, Reservation

# Database configuration
DATABASE_URL = "postgresql://dinouser:dinopass123@localhost:5432/dinoreserve"
# For SQLite: DATABASE_URL = "sqlite:///./dinoreserve.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sample customer names
CUSTOMER_NAMES = [
    "John Dino", "Sarah Rex", "Mike Saur", "Emily Raptor", "David Stego",
    "Lisa Bronto", "Chris Ptero", "Amanda Trike", "James Ankylo", "Rachel Diplo",
    "Tom Velo", "Jennifer Carno", "Mark Allo", "Nicole Herrera", "Brian Mega",
    "Stephanie Coelo", "Kevin Pachy", "Michelle Steno", "Ryan Iguano", "Laura Compso"
]

# Sample phone numbers
def generate_phone():
    return f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def seed_restaurants_and_tables(db):
    """Seed restaurants and their tables"""
    print("🦕 Seeding restaurants and tables...")
    
    # Check if already seeded
    if db.query(Restaurant).count() > 0:
        print("⚠️  Restaurants already exist. Skipping...")
        return
    
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
        
        print(f"  📍 Created: {restaurant.name}")
        
        # Add 25 tables per restaurant
        for i in range(1, 26):
            # Tables 1-10: capacity 2
            # Tables 11-20: capacity 4
            # Tables 21-25: capacity 6
            capacity = 2 if i <= 10 else (4 if i <= 20 else 6)
            
            table = Table(
                restaurant_id=restaurant.id,
                table_number=i,
                capacity=capacity
            )
            db.add(table)
        
        print(f"     ✓ Added 25 tables")
    
    db.commit()
    print("✅ Restaurants and tables seeded successfully!\n")

def seed_sample_reservations(db):
    """Seed sample reservations for testing"""
    print("🦖 Seeding sample reservations...")
    
    # Get all tables
    tables = db.query(Table).all()
    
    if not tables:
        print("⚠️  No tables found. Run restaurant seeding first.")
        return
    
    # Create reservations for next 7 days
    today = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    
    reservations_created = 0
    
    # Create 3-5 reservations per restaurant per day for next 3 days
    for day_offset in range(3):
        reservation_date = today + timedelta(days=day_offset)
        
        # Group tables by restaurant
        restaurants = {}
        for table in tables:
            if table.restaurant_id not in restaurants:
                restaurants[table.restaurant_id] = []
            restaurants[table.restaurant_id].append(table)
        
        # Create reservations for each restaurant
        for restaurant_id, restaurant_tables in restaurants.items():
            num_reservations = random.randint(3, 5)
            selected_tables = random.sample(restaurant_tables, min(num_reservations, len(restaurant_tables)))
            
            for table in selected_tables:
                # Random time between 12:00 and 21:00
                hour = random.randint(12, 21)
                minute = random.choice([0, 15, 30, 45])
                res_time = reservation_date.replace(hour=hour, minute=minute)
                
                # Random party size (up to table capacity)
                party_size = random.randint(1, table.capacity)
                
                reservation = Reservation(
                    table_id=table.id,
                    customer_name=random.choice(CUSTOMER_NAMES),
                    phone=generate_phone(),
                    party_size=party_size,
                    reservation_time=res_time,
                    status="reserved"
                )
                
                db.add(reservation)
                reservations_created += 1
    
    db.commit()
    print(f"✅ Created {reservations_created} sample reservations!\n")

def seed_past_reservations(db):
    """Seed some past reservations (for history/analytics)"""
    print("📅 Seeding past reservations...")
    
    tables = db.query(Table).all()
    if not tables:
        return
    
    # Create reservations for past 7 days
    today = datetime.now()
    past_reservations = 0
    
    for day_offset in range(1, 8):
        past_date = today - timedelta(days=day_offset)
        past_date = past_date.replace(hour=19, minute=0, second=0, microsecond=0)
        
        # Random 10-15 past reservations per day
        num_past_reservations = random.randint(10, 15)
        selected_tables = random.sample(tables, min(num_past_reservations, len(tables)))
        
        for table in selected_tables:
            hour = random.randint(12, 21)
            minute = random.choice([0, 15, 30, 45])
            res_time = past_date.replace(hour=hour, minute=minute)
            
            # Some cancelled, most completed
            status = "cancelled" if random.random() < 0.15 else "reserved"
            
            reservation = Reservation(
                table_id=table.id,
                customer_name=random.choice(CUSTOMER_NAMES),
                phone=generate_phone(),
                party_size=random.randint(1, table.capacity),
                reservation_time=res_time,
                status=status
            )
            
            db.add(reservation)
            past_reservations += 1
    
    db.commit()
    print(f"✅ Created {past_reservations} past reservations!\n")

def clear_all_data(db):
    """Clear all data from database (use with caution!)"""
    print("⚠️  CLEARING ALL DATA...")
    
    db.query(Reservation).delete()
    db.query(Table).delete()
    db.query(Restaurant).delete()
    db.commit()
    
    print("✅ All data cleared!\n")

def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("🦕 DINO RESERVE - DATABASE SEEDING 🦖")
    print("="*60 + "\n")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Uncomment to clear all data first
        # clear_all_data(db)
        
        # Seed data
        seed_restaurants_and_tables(db)
        seed_sample_reservations(db)
        seed_past_reservations(db)
        
        print("\n" + "="*60)
        print("🎉 DATABASE SEEDING COMPLETE! 🎉")
        print("="*60)
        print("\nYou can now start the FastAPI server and test the application!")
        print("Run: python main.py\n")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
