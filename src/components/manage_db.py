#!/usr/bin/env python
"""
Dino Reserve Database Management CLI
Provides convenient commands for database operations
"""

import sys
import argparse
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from tabulate import tabulate

from main import Base, Restaurant, Table, Reservation

DATABASE_URL = "postgresql://dinouser:dinopass123@localhost:5432/dinoreserve"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DinoManager:
    """Database management commands"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __del__(self):
        self.db.close()
    
    def show_stats(self):
        """Show database statistics"""
        print("\n🦕 DINO RESERVE DATABASE STATISTICS 🦖\n")
        print("="*60)
        
        # Count records
        restaurant_count = self.db.query(Restaurant).count()
        table_count = self.db.query(Table).count()
        reservation_count = self.db.query(Reservation).count()
        
        # Active vs cancelled reservations
        active = self.db.query(Reservation).filter(Reservation.status == 'reserved').count()
        cancelled = self.db.query(Reservation).filter(Reservation.status == 'cancelled').count()
        
        # Future reservations
        now = datetime.now()
        future = self.db.query(Reservation).filter(
            Reservation.reservation_time > now,
            Reservation.status == 'reserved'
        ).count()
        
        stats = [
            ["🏢 Restaurants", restaurant_count],
            ["🪑 Total Tables", table_count],
            ["📅 Total Reservations", reservation_count],
            ["✅ Active Reservations", active],
            ["❌ Cancelled Reservations", cancelled],
            ["📆 Upcoming Reservations", future],
        ]
        
        print(tabulate(stats, headers=["Metric", "Count"], tablefmt="fancy_grid"))
        print()
    
    def list_restaurants(self):
        """List all restaurants"""
        restaurants = self.db.query(Restaurant).all()
        
        print("\n🦕 RESTAURANTS 🦖\n")
        
        data = []
        for r in restaurants:
            table_count = self.db.query(Table).filter(Table.restaurant_id == r.id).count()
            reserved = self.db.query(Table).join(Reservation).filter(
                Table.restaurant_id == r.id,
                Reservation.status == 'reserved',
                Reservation.reservation_time >= datetime.now()
            ).distinct().count()
            
            data.append([
                r.id,
                r.name,
                r.location,
                r.dino_type,
                f"{reserved}/{table_count}"
            ])
        
        print(tabulate(
            data,
            headers=["ID", "Name", "Location", "Dino Type", "Reserved/Total"],
            tablefmt="fancy_grid"
        ))
        print()
    
    def list_tables(self, restaurant_id: int):
        """List tables for a restaurant"""
        restaurant = self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        
        if not restaurant:
            print(f"❌ Restaurant {restaurant_id} not found!")
            return
        
        print(f"\n🪑 TABLES FOR {restaurant.name.upper()} 🪑\n")
        
        tables = self.db.query(Table).filter(Table.restaurant_id == restaurant_id).all()
        
        data = []
        for t in tables:
            # Check for active reservation
            active_res = self.db.query(Reservation).filter(
                Reservation.table_id == t.id,
                Reservation.status == 'reserved',
                Reservation.reservation_time >= datetime.now()
            ).first()
            
            status = "🍴 Reserved" if active_res else "🦕 Available"
            customer = active_res.customer_name if active_res else "-"
            
            data.append([
                t.table_number,
                t.capacity,
                status,
                customer
            ])
        
        print(tabulate(
            data,
            headers=["Table #", "Capacity", "Status", "Customer"],
            tablefmt="fancy_grid"
        ))
        print()
    
    def list_reservations(self, limit: int = 20, status: str = None):
        """List recent reservations"""
        query = self.db.query(Reservation).join(Table).join(Restaurant)
        
        if status:
            query = query.filter(Reservation.status == status)
        
        reservations = query.order_by(Reservation.reservation_time.desc()).limit(limit).all()
        
        print(f"\n📅 RESERVATIONS (Last {limit}) 📅\n")
        
        data = []
        for r in reservations:
            restaurant_name = r.table.restaurant.name
            time_str = r.reservation_time.strftime("%Y-%m-%d %H:%M")
            status_icon = "✅" if r.status == 'reserved' else "❌"
            
            data.append([
                r.id,
                restaurant_name,
                f"Table {r.table.table_number}",
                r.customer_name,
                r.phone,
                r.party_size,
                time_str,
                f"{status_icon} {r.status}"
            ])
        
        print(tabulate(
            data,
            headers=["ID", "Restaurant", "Table", "Customer", "Phone", "Party", "Time", "Status"],
            tablefmt="fancy_grid"
        ))
        print()
    
    def upcoming_reservations(self, days: int = 7):
        """Show upcoming reservations"""
        now = datetime.now()
        future = now + timedelta(days=days)
        
        reservations = self.db.query(Reservation).filter(
            Reservation.reservation_time.between(now, future),
            Reservation.status == 'reserved'
        ).order_by(Reservation.reservation_time).all()
        
        print(f"\n📆 UPCOMING RESERVATIONS (Next {days} days) 📆\n")
        
        if not reservations:
            print("No upcoming reservations! 🦕")
            return
        
        data = []
        for r in reservations:
            restaurant_name = r.table.restaurant.name
            time_str = r.reservation_time.strftime("%Y-%m-%d %H:%M")
            time_until = r.reservation_time - now
            hours = int(time_until.total_seconds() / 3600)
            
            data.append([
                restaurant_name,
                f"Table {r.table.table_number}",
                r.customer_name,
                r.party_size,
                time_str,
                f"in {hours}h"
            ])
        
        print(tabulate(
            data,
            headers=["Restaurant", "Table", "Customer", "Party", "Time", "In"],
            tablefmt="fancy_grid"
        ))
        print(f"\n📊 Total: {len(reservations)} reservations\n")
    
    def cancel_reservation(self, reservation_id: int):
        """Cancel a reservation"""
        reservation = self.db.query(Reservation).filter(Reservation.id == reservation_id).first()
        
        if not reservation:
            print(f"❌ Reservation {reservation_id} not found!")
            return
        
        print(f"\n⚠️  Cancelling reservation:")
        print(f"   Customer: {reservation.customer_name}")
        print(f"   Time: {reservation.reservation_time}")
        
        confirm = input("\nAre you sure? (yes/no): ")
        
        if confirm.lower() in ['yes', 'y']:
            reservation.status = 'cancelled'
            self.db.commit()
            print("✅ Reservation cancelled!")
        else:
            print("❌ Cancelled operation")
    
    def clear_old_reservations(self, days: int = 30):
        """Delete old cancelled reservations"""
        cutoff = datetime.now() - timedelta(days=days)
        
        old_reservations = self.db.query(Reservation).filter(
            Reservation.reservation_time < cutoff,
            Reservation.status == 'cancelled'
        ).all()
        
        count = len(old_reservations)
        
        if count == 0:
            print("✅ No old cancelled reservations to clean up!")
            return
        
        print(f"\n⚠️  Found {count} old cancelled reservations (before {cutoff.date()})")
        confirm = input("Delete them? (yes/no): ")
        
        if confirm.lower() in ['yes', 'y']:
            for res in old_reservations:
                self.db.delete(res)
            self.db.commit()
            print(f"✅ Deleted {count} old reservations!")
        else:
            print("❌ Cancelled operation")

def main():
    parser = argparse.ArgumentParser(
        description="🦕 Dino Reserve Database Manager 🦖",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage.py stats                    # Show database statistics
  python manage.py restaurants              # List all restaurants
  python manage.py tables 1                 # Show tables for restaurant 1
  python manage.py reservations             # List recent reservations
  python manage.py upcoming                 # Show upcoming reservations
  python manage.py cancel 42                # Cancel reservation #42
  python manage.py cleanup                  # Remove old cancelled reservations
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    # Restaurants command
    subparsers.add_parser('restaurants', help='List all restaurants')
    
    # Tables command
    tables_parser = subparsers.add_parser('tables', help='List tables for a restaurant')
    tables_parser.add_argument('restaurant_id', type=int, help='Restaurant ID')
    
    # Reservations command
    res_parser = subparsers.add_parser('reservations', help='List reservations')
    res_parser.add_argument('--limit', type=int, default=20, help='Number of results')
    res_parser.add_argument('--status', choices=['reserved', 'cancelled'], help='Filter by status')
    
    # Upcoming command
    upcoming_parser = subparsers.add_parser('upcoming', help='Show upcoming reservations')
    upcoming_parser.add_argument('--days', type=int, default=7, help='Number of days ahead')
    
    # Cancel command
    cancel_parser = subparsers.add_parser('cancel', help='Cancel a reservation')
    cancel_parser.add_argument('reservation_id', type=int, help='Reservation ID to cancel')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Delete old cancelled reservations')
    cleanup_parser.add_argument('--days', type=int, default=30, help='Delete older than N days')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = DinoManager()
    
    try:
        if args.command == 'stats':
            manager.show_stats()
        elif args.command == 'restaurants':
            manager.list_restaurants()
        elif args.command == 'tables':
            manager.list_tables(args.restaurant_id)
        elif args.command == 'reservations':
            manager.list_reservations(args.limit, args.status)
        elif args.command == 'upcoming':
            manager.upcoming_reservations(args.days)
        elif args.command == 'cancel':
            manager.cancel_reservation(args.reservation_id)
        elif args.command == 'cleanup':
            manager.clear_old_reservations(args.days)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
