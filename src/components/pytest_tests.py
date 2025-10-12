"""
Unit tests for Dino Reserve API
Run with: pytest test_main.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from main import app, Base, get_db, Restaurant, Table, Reservation

# Test database (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create test database before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_restaurant():
    """Create a sample restaurant with tables"""
    db = TestingSessionLocal()
    
    restaurant = Restaurant(
        name="Test T-Rex Tavern",
        location="Test Location",
        dino_type="trex"
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    
    # Add 5 test tables
    for i in range(1, 6):
        table = Table(
            restaurant_id=restaurant.id,
            table_number=i,
            capacity=4
        )
        db.add(table)
    
    db.commit()
    db.close()
    
    return restaurant

class TestHealthCheck:
    """Test API health check"""
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Dino Reserve" in data["message"]

class TestRestaurants:
    """Test restaurant endpoints"""
    
    def test_get_restaurants_empty(self):
        response = client.get("/restaurants")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_restaurants_with_data(self, sample_restaurant):
        response = client.get("/restaurants")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Test T-Rex Tavern"
        assert data[0]["dino_type"] == "trex"
    
    def test_get_restaurant_by_id(self, sample_restaurant):
        response = client.get(f"/restaurants/{sample_restaurant.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_restaurant.id
        assert data["name"] == sample_restaurant.name
    
    def test_get_restaurant_not_found(self):
        response = client.get("/restaurants/9999")
        assert response.status_code == 404

class TestTables:
    """Test table endpoints"""
    
    def test_get_tables_for_restaurant(self, sample_restaurant):
        response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5  # We created 5 tables
        
        # Check table structure
        table = data[0]
        assert "table_number" in table
        assert "capacity" in table
        assert "is_reserved" in table
        assert table["is_reserved"] == False
    
    def test_get_tables_restaurant_not_found(self):
        response = client.get("/restaurants/9999/tables")
        assert response.status_code == 404

class TestReservations:
    """Test reservation endpoints"""
    
    def test_create_reservation(self, sample_restaurant):
        # Get a table
        tables_response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        tables = tables_response.json()
        table_id = tables[0]["id"]
        
        # Create reservation
        tomorrow = datetime.now() + timedelta(days=1)
        reservation_data = {
            "table_id": table_id,
            "customer_name": "Test Customer",
            "phone": "+1-555-TEST",
            "party_size": 2,
            "reservation_time": tomorrow.isoformat()
        }
        
        response = client.post("/reservations", json=reservation_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["customer_name"] == "Test Customer"
        assert data["phone"] == "+1-555-TEST"
        assert data["party_size"] == 2
        assert data["status"] == "reserved"
    
    def test_create_reservation_table_not_found(self):
        tomorrow = datetime.now() + timedelta(days=1)
        reservation_data = {
            "table_id": 9999,
            "customer_name": "Test Customer",
            "phone": "+1-555-TEST",
            "party_size": 2,
            "reservation_time": tomorrow.isoformat()
        }
        
        response = client.post("/reservations", json=reservation_data)
        assert response.status_code == 404
    
    def test_create_reservation_exceeds_capacity(self, sample_restaurant):
        tables_response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        tables = tables_response.json()
        table_id = tables[0]["id"]
        table_capacity = tables[0]["capacity"]
        
        tomorrow = datetime.now() + timedelta(days=1)
        reservation_data = {
            "table_id": table_id,
            "customer_name": "Test Customer",
            "phone": "+1-555-TEST",
            "party_size": table_capacity + 1,  # Exceed capacity
            "reservation_time": tomorrow.isoformat()
        }
        
        response = client.post("/reservations", json=reservation_data)
        assert response.status_code == 400
        assert "capacity" in response.json()["detail"].lower()
    
    def test_update_reservation(self, sample_restaurant):
        # Create a reservation first
        tables_response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        table_id = tables_response.json()[0]["id"]
        
        tomorrow = datetime.now() + timedelta(days=1)
        reservation_data = {
            "table_id": table_id,
            "customer_name": "Original Name",
            "phone": "+1-555-TEST",
            "party_size": 2,
            "reservation_time": tomorrow.isoformat()
        }
        
        create_response = client.post("/reservations", json=reservation_data)
        reservation_id = create_response.json()["id"]
        
        # Update the reservation
        update_data = {
            "customer_name": "Updated Name",
            "party_size": 3
        }
        
        response = client.put(f"/reservations/{reservation_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["customer_name"] == "Updated Name"
        assert data["party_size"] == 3
    
    def test_cancel_reservation(self, sample_restaurant):
        # Create a reservation
        tables_response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        table_id = tables_response.json()[0]["id"]
        
        tomorrow = datetime.now() + timedelta(days=1)
        reservation_data = {
            "table_id": table_id,
            "customer_name": "Test Customer",
            "phone": "+1-555-TEST",
            "party_size": 2,
            "reservation_time": tomorrow.isoformat()
        }
        
        create_response = client.post("/reservations", json=reservation_data)
        reservation_id = create_response.json()["id"]
        
        # Cancel the reservation
        response = client.delete(f"/reservations/{reservation_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Reservation cancelled successfully"
        
        # Verify it's cancelled
        db = TestingSessionLocal()
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        assert reservation.status == "cancelled"
        db.close()
    
    def test_get_all_reservations(self, sample_restaurant):
        # Create multiple reservations
        tables_response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        tables = tables_response.json()
        
        tomorrow = datetime.now() + timedelta(days=1)
        
        for i in range(3):
            reservation_data = {
                "table_id": tables[i]["id"],
                "customer_name": f"Customer {i}",
                "phone": f"+1-555-{i:04d}",
                "party_size": 2,
                "reservation_time": tomorrow.isoformat()
            }
            client.post("/reservations", json=reservation_data)
        
        # Get all reservations
        response = client.get("/reservations")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
    
    def test_get_reservations_filtered_by_status(self, sample_restaurant):
        # Create and cancel a reservation
        tables_response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        table_id = tables_response.json()[0]["id"]
        
        tomorrow = datetime.now() + timedelta(days=1)
        reservation_data = {
            "table_id": table_id,
            "customer_name": "Test Customer",
            "phone": "+1-555-TEST",
            "party_size": 2,
            "reservation_time": tomorrow.isoformat()
        }
        
        create_response = client.post("/reservations", json=reservation_data)
        reservation_id = create_response.json()["id"]
        
        client.delete(f"/reservations/{reservation_id}")
        
        # Get cancelled reservations
        response = client.get("/reservations?status=cancelled")
        assert response.status_code == 200
        data = response.json()
        assert all(r["status"] == "cancelled" for r in data)

class TestTableStatus:
    """Test table status with reservations"""
    
    def test_table_shows_reserved_status(self, sample_restaurant):
        # Get tables
        tables_response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        tables = tables_response.json()
        table_id = tables[0]["id"]
        
        # Initially not reserved
        assert tables[0]["is_reserved"] == False
        
        # Create reservation
        tomorrow = datetime.now() + timedelta(days=1)
        reservation_data = {
            "table_id": table_id,
            "customer_name": "Test Customer",
            "phone": "+1-555-TEST",
            "party_size": 2,
            "reservation_time": tomorrow.isoformat()
        }
        client.post("/reservations", json=reservation_data)
        
        # Check table status again
        tables_response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        tables = tables_response.json()
        
        # Find our table
        reserved_table = next(t for t in tables if t["id"] == table_id)
        assert reserved_table["is_reserved"] == True
        assert reserved_table["current_reservation"] is not None
        assert reserved_table["current_reservation"]["customer_name"] == "Test Customer"

class TestDataValidation:
    """Test data validation"""
    
    def test_create_reservation_missing_fields(self, sample_restaurant):
        tables_response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        table_id = tables_response.json()[0]["id"]
        
        # Missing customer_name
        reservation_data = {
            "table_id": table_id,
            "phone": "+1-555-TEST",
            "party_size": 2,
            "reservation_time": datetime.now().isoformat()
        }
        
        response = client.post("/reservations", json=reservation_data)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_restaurant_id(self):
        response = client.get("/restaurants/not-a-number")
        assert response.status_code == 422

# Performance test (optional)
class TestPerformance:
    """Test API performance"""
    
    def test_bulk_table_retrieval(self, sample_restaurant):
        import time
        
        start = time.time()
        response = client.get(f"/restaurants/{sample_restaurant.id}/tables")
        end = time.time()
        
        assert response.status_code == 200
        assert (end - start) < 1.0  # Should complete in under 1 second

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
