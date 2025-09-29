import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ArrowLeft } from 'lucide-react';
import { ReservationModal } from './ReservationModal';

interface Table {
  id: number;
  isReserved: boolean;
  customerName?: string;
  partySize?: number;
  reservationTime?: string;
}

interface TableLayoutProps {
  restaurantId: string;
  onBack: () => void;
}

const restaurantNames = {
  'trex-bistro': { name: 'T-Rex Bistro', emoji: '🦖', theme: 'from-red-50 to-orange-50' },
  'herbivore-haven': { name: 'Herbivore Haven', emoji: '🦕', theme: 'from-green-50 to-emerald-50' },
  'stego-steakhouse': { name: 'Stego Steakhouse', emoji: '🦕', theme: 'from-orange-50 to-yellow-50' },
  'raptor-cafe': { name: 'Raptor Café', emoji: '🦖', theme: 'from-yellow-50 to-amber-50' },
  'tricera-tavern': { name: 'Tricera Tavern', emoji: '🦕', theme: 'from-purple-50 to-pink-50' }
};

export function TableLayout({ restaurantId, onBack }: TableLayoutProps) {
  const restaurant = restaurantNames[restaurantId as keyof typeof restaurantNames];
  
  // Initialize tables with some mock reservations
  const [tables, setTables] = useState<Table[]>(() => {
    const initialTables = Array.from({ length: 25 }, (_, i) => ({
      id: i + 1,
      isReserved: false
    }));
    
    // Add some mock reservations
    initialTables[2] = { id: 3, isReserved: true, customerName: 'Dr. Grant', partySize: 4, reservationTime: '19:00' };
    initialTables[7] = { id: 8, isReserved: true, customerName: 'Sarah Harding', partySize: 2, reservationTime: '18:30' };
    initialTables[15] = { id: 16, isReserved: true, customerName: 'Ian Malcolm', partySize: 3, reservationTime: '20:00' };
    
    return initialTables;
  });

  const [selectedTable, setSelectedTable] = useState<number | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleTableClick = (tableId: number) => {
    const table = tables.find(t => t.id === tableId);
    if (table && !table.isReserved) {
      setSelectedTable(tableId);
      setIsModalOpen(true);
    }
  };

  const handleReservation = (reservation: {
    customerName: string;
    phone: string;
    partySize: number;
    reservationTime: string;
  }) => {
    if (selectedTable) {
      setTables(prev => prev.map(table => 
        table.id === selectedTable 
          ? {
              ...table,
              isReserved: true,
              customerName: reservation.customerName,
              partySize: reservation.partySize,
              reservationTime: reservation.reservationTime
            }
          : table
      ));
      setSelectedTable(null);
    }
  };

  const availableCount = tables.filter(t => !t.isReserved).length;
  const reservedCount = tables.filter(t => t.isReserved).length;

  return (
    <div className={`min-h-screen bg-gradient-to-br ${restaurant.theme} p-6`}>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <Button
            onClick={onBack}
            variant="outline"
            className="flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Restaurants
          </Button>
          
          <div className="text-center">
            <div className="inline-flex items-center gap-2">
              <span className="text-3xl">{restaurant.emoji}</span>
              <h1 className="text-3xl font-bold text-gray-800">{restaurant.name}</h1>
              <span className="text-3xl">{restaurant.emoji}</span>
            </div>
          </div>
          
          <div className="flex gap-2">
            <Badge variant="default" className="bg-green-100 text-green-800">
              🦕 {availableCount} Available
            </Badge>
            <Badge variant="secondary" className="bg-orange-100 text-orange-800">
              🍽️ {reservedCount} Feeding
            </Badge>
          </div>
        </div>

        {/* Status Indicator */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-md">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600">🦕 Dino Cave synced • Last updated 2 minutes ago</span>
          </div>
        </div>

        {/* Table Grid */}
        <div className="grid grid-cols-5 gap-4">
          {tables.map((table) => (
            <Card
              key={table.id}
              className={`cursor-pointer transition-all hover:scale-105 ${
                table.isReserved 
                  ? 'bg-orange-100 border-orange-300 hover:bg-orange-200' 
                  : 'bg-green-100 border-green-300 hover:bg-green-200'
              }`}
              onClick={() => handleTableClick(table.id)}
            >
              <CardHeader className="text-center p-3">
                <div className="text-3xl mb-1">
                  {table.isReserved ? '🍴🦖' : '🦕'}
                </div>
                <CardTitle className="text-sm">Table {table.id}</CardTitle>
              </CardHeader>
              <CardContent className="p-3 pt-0">
                {table.isReserved ? (
                  <div className="text-center">
                    <Badge variant="secondary" className="text-xs mb-1">
                      Feeding Time
                    </Badge>
                    <p className="text-xs font-medium">{table.customerName}</p>
                    <p className="text-xs text-gray-600">
                      {table.partySize} dinos • {table.reservationTime}
                    </p>
                  </div>
                ) : (
                  <div className="text-center">
                    <Badge variant="default" className="text-xs mb-1 bg-green-600">
                      Hungry Dino
                    </Badge>
                    <p className="text-xs text-gray-600">Click to feed!</p>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Legend */}
        <div className="flex justify-center gap-8 mt-8">
          <div className="flex items-center gap-2">
            <div className="text-2xl">🦕</div>
            <span className="text-sm text-gray-600">Hungry Dino (Available)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="text-2xl">🍴🦖</div>
            <span className="text-sm text-gray-600">Dino Eating (Reserved)</span>
          </div>
        </div>
      </div>

      {/* Reservation Modal */}
      <ReservationModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedTable(null);
        }}
        onConfirm={handleReservation}
        tableNumber={selectedTable || 0}
      />
    </div>
  );
}