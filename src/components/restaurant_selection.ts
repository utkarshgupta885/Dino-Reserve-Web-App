import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface Restaurant {
  id: number;
  name: string;
  location: string;
  dino_type: string;
}

interface RestaurantSelectionProps {
  onSelectRestaurant: (restaurantId: string) => void;
}

const DINO_ICONS: Record<string, string> = {
  trex: '🦖',
  bronto: '🦕',
  raptor: '🦎',
  stego: '🦕',
  ptero: '🦅'
};

const DINO_COLORS: Record<string, string> = {
  trex: 'from-red-50 to-orange-50',
  bronto: 'from-green-50 to-emerald-50',
  raptor: 'from-orange-50 to-amber-50',
  stego: 'from-yellow-50 to-orange-50',
  ptero: 'from-purple-50 to-pink-50'
};

export function RestaurantSelection({ onSelectRestaurant }: RestaurantSelectionProps) {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchRestaurants();
  }, []);

  const fetchRestaurants = async () => {
    try {
      const response = await fetch('http://localhost:8000/restaurants');
      if (!response.ok) throw new Error('Failed to fetch restaurants');
      const data = await response.json();
      setRestaurants(data);
    } catch (err) {
      setError('Could not connect to Dino Cave. Please check if the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-orange-50 to-yellow-50">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-pulse">🦕</div>
          <p className="text-xl text-gray-600">Loading Dino Restaurants...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-orange-50 to-yellow-50 p-4">
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle className="text-red-600">⚠️ Connection Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700 mb-4">{error}</p>
            <Button onClick={fetchRestaurants} className="w-full">
              🔄 Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-orange-50 to-yellow-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-green-800 mb-2">
            🦕 Dino Reserve 🦖
          </h1>
          <p className="text-xl text-gray-600">
            Select a restaurant to manage tables and feed hungry dinos
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {restaurants.map((restaurant) => (
            <Card
              key={restaurant.id}
              className={`cursor-pointer transition-all hover:shadow-lg hover:scale-105 bg-gradient-to-br ${
                DINO_COLORS[restaurant.dino_type] || 'from-gray-50 to-gray-100'
              }`}
              onClick={() => onSelectRestaurant(restaurant.id.toString())}
            >
              <CardHeader className="text-center">
                <div className="text-6xl mb-2">
                  {DINO_ICONS[restaurant.dino_type] || '🦕'}
                </div>
                <CardTitle className="text-2xl text-gray-800">
                  {restaurant.name}
                </CardTitle>
                <CardDescription className="text-gray-600">
                  📍 {restaurant.location}
                </CardDescription>
              </CardHeader>
              <CardContent className="text-center">
                <Button className="w-full bg-green-600 hover:bg-green-700 text-white">
                  Manage Tables
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {restaurants.length === 0 && (
          <div className="text-center mt-12">
            <p className="text-gray-600 text-lg">
              No restaurants found. The dinos are still setting up! 🦕
            </p>
          </div>
        )}

        <div className="mt-8 text-center">
          <div className="inline-flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600">Dino Cave synced</span>
          </div>
        </div>
      </div>
    </div>
  );
}
