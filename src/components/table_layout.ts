import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ArrowLeft } from 'lucide-react';

interface Table {
  id: number;
  table_number: number;
  capacity: number;
  restaurant_id: number;
  is_reserved: boolean;
  current_reservation?: {
    id: number;
    customer_name: string;
    phone: string;
    party_size: number;
    reservation_time: string;
    status: string;
  } | null;
}

interface Restaurant {
  id: number;
  name: string;
  location: string;
  dino_type: string;
}

interface TableLayoutProps {
  restaurantId: string;
  onBack: () => void;
}

export function TableLayout({ restaurantId, onBack }: TableLayoutProps) {
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [tables, setTables] = useState<Table[]>([]);
  const [selectedTable, setSelectedTable] = useState<Table | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    customer_name: '',
    phone: '',
    party_size: '',
    reservation_time: ''
  });

  useEffect(() => {
    fetchData();
  }, [restaurantId]);

  const fetchData = async () => {
    try {
      const [restaurantRes, tablesRes] = await Promise.all([
        fetch(`http://localhost:8000/restaurants/${restaurantId}`),
        fetch(`http://localhost:8000/restaurants/${restaurantId}/tables`)
      ]);

      const restaurantData = await restaurantRes.json();
      const tablesData = await tablesRes.json();

      setRestaurant(restaurantData);
      setTables(tablesData);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTableClick = (table: Table) => {
    setSelectedTable(table);
    if (table.is_reserved && table.current_reservation) {
      setFormData({
        customer_name: table.current_reservation.customer_name,
        phone: table.current_reservation.phone,
        party_size: table.current_reservation.party_size.toString(),
        reservation_time: table.current_reservation.reservation_time.slice(0, 16)
      });
    } else {
      setFormData({
        customer_name: '',
        phone: '',
        party_size: '',
        reservation_time: ''
      });
    }
    setIsDialogOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedTable) return;

    try {
      const reservationData = {
        table_id: selectedTable.id,
        customer_name: formData.customer_name,
        phone: formData.phone,
        party_size: parseInt(formData.party_size),
        reservation_time: new Date(formData.reservation_time).toISOString()
      };

      if (selectedTable.is_reserved && selectedTable.current_reservation) {
        await fetch(`http://localhost:8000/reservations/${selectedTable.current_reservation.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(reservationData)
        });
      } else {
        await fetch('http://localhost:8000/reservations', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(reservationData)
        });
      }

      setIsDialogOpen(false);
      fetchData();
    } catch (err) {
      console.error('Error saving reservation:', err);
      alert('Failed to save reservation. Please try again.');
    }
  };

  const handleCancel = async () => {
    if (!selectedTable?.current_reservation) return;

    try {
      await fetch(`http://localhost:8000/reservations/${selectedTable.current_reservation.id}`, {
        method: 'DELETE'
      });
      setIsDialogOpen(false);
      fetchData();
    } catch (err) {
      console.error('Error canceling reservation:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-orange-50 to-yellow-50">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-pulse">🦕</div>
          <p className="text-xl text-gray-600">Loading tables...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-orange-50 to-yellow-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <Button
            onClick={onBack}
            variant="outline"
            className="flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Restaurants
          </Button>
          <div className="inline-flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600">Dino Cave synced</span>
          </div>
        </div>

        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-3xl text-green-800">
              🦕 {restaurant?.name}
            </CardTitle>
            <p className="text-gray-600">📍 {restaurant?.location}</p>
          </CardHeader>
        </Card>

        <div className="grid grid-cols-5 gap-4 mb-6">
          {tables.map((table) => (
            <Card
              key={table.id}
              onClick={() => handleTableClick(table)}
              className={`cursor-pointer transition-all hover:shadow-lg hover:scale-105 ${
                table.is_reserved
                  ? 'bg-orange-100 border-orange-300'
                  : 'bg-green-100 border-green-300'
              }`}
            >
              <CardContent className="p-4 text-center">
                <div className="text-4xl mb-2">
                  {table.is_reserved ? '🍴🦖' : '🦕'}
                </div>
                <div className="font-semibold text-gray-800">
                  Table {table.table_number}
                </div>
                <div className="text-sm text-gray-600">
                  Capacity: {table.capacity}
                </div>
                <div className="mt-2 text-xs font-medium">
                  {table.is_reserved ? (
                    <span className="text-orange-800">Dino is eating</span>
                  ) : (
                    <span className="text-green-800">Hungry dino waiting</span>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card className="bg-white">
          <CardContent className="p-4">
            <div className="flex items-center justify-around text-center">
              <div>
                <div className="text-2xl mb-1">🦕</div>
                <div className="text-sm font-medium text-gray-700">Available</div>
                <div className="text-2xl font-bold text-green-600">
                  {tables.filter(t => !t.is_reserved).length}
                </div>
              </div>
              <div>
                <div className="text-2xl mb-1">🍴🦖</div>
                <div className="text-sm font-medium text-gray-700">Reserved</div>
                <div className="text-2xl font-bold text-orange-600">
                  {tables.filter(t => t.is_reserved).length}
                </div>
              </div>
              <div>
                <div className="text-2xl mb-1">🍽️</div>
                <div className="text-sm font-medium text-gray-700">Total Tables</div>
                <div className="text-2xl font-bold text-gray-800">25</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="text-2xl">
              {selectedTable?.is_reserved ? '🍴 Update Reservation' : '🦕 Feed the Dino'}
            </DialogTitle>
            <DialogDescription>
              Table {selectedTable?.table_number} (Capacity: {selectedTable?.capacity})
            </DialogDescription>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="customer_name">Customer Name</Label>
              <Input
                id="customer_name"
                value={formData.customer_name}
                onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
                required
                placeholder="Enter customer name"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="phone">Phone Number</Label>
              <Input
                id="phone"
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                required
                placeholder="Enter phone number"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="party_size">Party Size</Label>
              <Input
                id="party_size"
                type="number"
                min="1"
                max={selectedTable?.capacity}
                value={formData.party_size}
                onChange={(e) => setFormData({ ...formData, party_size: e.target.value })}
                required
                placeholder="Number of guests"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="reservation_time">Reservation Time</Label>
              <Input
                id="reservation_time"
                type="datetime-local"
                value={formData.reservation_time}
                onChange={(e) => setFormData({ ...formData, reservation_time: e.target.value })}
                required
              />
            </div>

            <div className="flex gap-2">
              <Button
                type="submit"
                className="flex-1 bg-green-600 hover:bg-green-700 text-white"
              >
                {selectedTable?.is_reserved ? '✏️ Update' : '🦖 Feed Dino'}
              </Button>
              {selectedTable?.is_reserved && (
                <Button
                  type="button"
                  onClick={handleCancel}
                  variant="destructive"
                  className="flex-1"
                >
                  ❌ Cancel
                </Button>
              )}
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
