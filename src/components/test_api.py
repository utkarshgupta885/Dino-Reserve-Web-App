"""
API Testing Script for Dino Reserve
Tests all API endpoints to ensure they're working correctly
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name: str):
    """Print test name"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}🧪 Testing: {name}{Colors.RESET}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.RESET}")

def test_health_check():
    """Test the root endpoint"""
    print_test("Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        
        data = response.json()
        print_success(f"API is running: {data['message']}")
        return True
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False

def test_get_restaurants():
    """Test getting all restaurants"""
    print_test("Get All Restaurants")
    
    try:
        response = requests.get(f"{BASE_URL}/restaurants")
        response.raise_for_status()
        
        restaurants = response.json()
        print_success(f"Found {len(restaurants)} restaurants")
        
        for restaurant in restaurants:
            print_info(f"  🦕 {restaurant['name']} - {restaurant['location']}")
        
        return restaurants
    except Exception as e:
        print_error(f"Failed to get restaurants: {e}")
        return []

def test_get_restaurant_by_id(restaurant_id: int):
    """Test getting a specific restaurant"""
    print_test(f"Get Restaurant by ID ({restaurant_id})")
    
    try:
        response = requests.get(f"{BASE_URL}/restaurants/{restaurant_id}")
        response.raise_for_status()
        
        restaurant = response.json()
        print_success(f"Retrieved: {restaurant['name']}")
        return restaurant
    except Exception as e:
        print_error(f"Failed to get restaurant: {e}")
        return None

def test_get_tables(restaurant_id: int):
    """Test getting tables for a restaurant"""
    print_test(f"Get Tables for Restaurant {restaurant_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/restaurants/{restaurant_id}/tables")
        response.raise_for_status()
        
        tables = response.json()
        reserved = sum(1 for t in tables if t['is_reserved'])
        available = len(tables) - reserved
        
        print_success(f"Found {len(tables)} tables")
        print_info(f"  🦕 Available: {available}")
        print_info(f"  🍴 Reserved: {reserved}")
        
        return tables
    except Exception as e:
        print_error(f"Failed to get tables: {e}")
        return []

def test_create_reservation(table_id: int, capacity: int):
    """Test creating a reservation"""
    print_test("Create Reservation")
    
    # Create reservation for tomorrow at 7 PM
    tomorrow = datetime.now() + timedelta(days=1)
    reservation_time = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    
    reservation_data = {
        "table_id": table_id,
        "customer_name": "Test Dino",
        "phone": "+1-555-TEST-123",
        "party_size": min(2, capacity),
        "reservation_time": reservation_time.isoformat()
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/reservations",
            json=reservation_data
        )
        response.raise_for_status()
        
        reservation = response.json()
        print_success(f"Created reservation ID: {reservation['id']}")
        print_info(f"  Customer: {reservation['customer_name']}")
        print_info(f"  Time: {reservation['reservation_time']}")
        
        return reservation
    except Exception as e:
        print_error(f"Failed to create reservation: {e}")
        return None

def test_update_reservation(reservation_id: int):
    """Test updating a reservation"""
    print_test(f"Update Reservation {reservation_id}")
    
    update_data = {
        "customer_name": "Updated Test Dino",
        "party_size": 3
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/reservations/{reservation_id}",
            json=update_data
        )
        response.raise_for_status()
        
        reservation = response.json()
        print_success("Reservation updated successfully")
        print_info(f"  New name: {reservation['customer_name']}")
        print_info(f"  New party size: {reservation['party_size']}")
        
        return reservation
    except Exception as e:
        print_error(f"Failed to update reservation: {e}")
        return None

def test_get_all_reservations():
    """Test getting all reservations"""
    print_test("Get All Reservations")
    
    try:
        response = requests.get(f"{BASE_URL}/reservations")
        response.raise_for_status()
        
        reservations = response.json()
        print_success(f"Found {len(reservations)} total reservations")
        
        reserved = sum(1 for r in reservations if r['status'] == 'reserved')
        cancelled = sum(1 for r in reservations if r['status'] == 'cancelled')
        
        print_info(f"  ✓ Reserved: {reserved}")
        print_info(f"  ✗ Cancelled: {cancelled}")
        
        return reservations
    except Exception as e:
        print_error(f"Failed to get reservations: {e}")
        return []

def test_cancel_reservation(reservation_id: int):
    """Test cancelling a reservation"""
    print_test(f"Cancel Reservation {reservation_id}")
    
    try:
        response = requests.delete(f"{BASE_URL}/reservations/{reservation_id}")
        response.raise_for_status()
        
        result = response.json()
        print_success(f"Reservation cancelled: {result['message']}")
        return True
    except Exception as e:
        print_error(f"Failed to cancel reservation: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}🦕 DINO RESERVE API TESTS 🦖{Colors.RESET}")
    print("="*70)
    
    # Track test results
    results = {
        'passed': 0,
        'failed': 0
    }
    
    # Test 1: Health Check
    if test_health_check():
        results['passed'] += 1
    else:
        results['failed'] += 1
        print_error("Cannot proceed without working API")
        return results
    
    # Test 2: Get Restaurants
    restaurants = test_get_restaurants()
    if restaurants:
        results['passed'] += 1
    else:
        results['failed'] += 1
        return results
    
    # Test 3: Get Restaurant by ID
    if restaurants:
        restaurant = test_get_restaurant_by_id(restaurants[0]['id'])
        if restaurant:
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Test 4: Get Tables
    if restaurants:
        tables = test_get_tables(restaurants[0]['id'])
        if tables:
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        # Test 5: Create Reservation
        if tables:
            # Find an available table
            available_table = next((t for t in tables if not t['is_reserved']), None)
            
            if available_table:
                reservation = test_create_reservation(
                    available_table['id'],
                    available_table['capacity']
                )
                
                if reservation:
                    results['passed'] += 1
                    
                    # Test 6: Update Reservation
                    updated = test_update_reservation(reservation['id'])
                    if updated:
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                    
                    # Test 7: Get All Reservations
                    all_reservations = test_get_all_reservations()
                    if all_reservations:
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                    
                    # Test 8: Cancel Reservation
                    if test_cancel_reservation(reservation['id']):
                        results['passed'] += 1
                    else:
                        results['failed'] += 1
                else:
                    results['failed'] += 1
            else:
                print_info("No available tables to test reservation creation")
    
    # Print summary
    print("\n" + "="*70)
    print(f"{Colors.BOLD}📊 TEST SUMMARY{Colors.RESET}")
    print("="*70)
    print(f"{Colors.GREEN}✅ Passed: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}❌ Failed: {results['failed']}{Colors.RESET}")
    
    total = results['passed'] + results['failed']
    percentage = (results['passed'] / total * 100) if total > 0 else 0
    
    print(f"\n{Colors.BOLD}Success Rate: {percentage:.1f}%{Colors.RESET}")
    
    if results['failed'] == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! 🎉{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}⚠️  Some tests failed. Check the output above.{Colors.RESET}")
    
    print()
    return results

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")
