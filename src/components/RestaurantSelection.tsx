import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

interface Restaurant {
  id: string;
  name: string;
  dinoType: string;
  emoji: string;
  description: string;
  totalTables: number;
  availableTables: number;
  theme: string;
}

interface RestaurantSelectionProps {
  onSelectRestaurant: (restaurantId: string) => void;
}

const restaurants: Restaurant[] = [
  {
    id: 'trex-bistro',
    name: 'T-Rex Bistro',
    dinoType: 'T-Rex',
    emoji: '🦖',
    description: 'Big portions for big appetites! Our carnivore classics will make you roar with delight.',
    totalTables: 25,
    availableTables: 18,
    theme: 'bg-red-50 border-red-200'
  },
  {
    id: 'herbivore-haven',
    name: 'Herbivore Haven',
    dinoType: 'Brachiosaurus',
    emoji: '🦕',
    description: 'Fresh greens and garden delights. Tall tables for our long-necked friends!',
    totalTables: 25,
    availableTables: 12,
    theme: 'bg-green-50 border-green-200'
  },
  {
    id: 'stego-steakhouse',
    name: 'Stego Steakhouse',
    dinoType: 'Stegosaurus',
    emoji: '🦕',
    description: 'Premium cuts with our signature spiky seasoning. A true prehistoric experience.',
    totalTables: 25,
    availableTables: 8,
    theme: 'bg-orange-50 border-orange-200'
  },
  {
    id: 'raptor-cafe',
    name: 'Raptor Café',
    dinoType: 'Velociraptor',
    emoji: '🦖',
    description: 'Quick bites for fast diners. Smart service that\'ll make you feel clever!',
    totalTables: 25,
    availableTables: 20,
    theme: 'bg-yellow-50 border-yellow-200'
  },
  {
    id: 'tricera-tavern',
    name: 'Tricera Tavern',
    dinoType: 'Triceratops',
    emoji: '🦕',
    description: 'Three-course meals with triple the flavor. Family-friendly prehistoric dining.',
    totalTables: 25,
    availableTables: 15,
    theme: 'bg-purple-50 border-purple-200'
  }
];

export function RestaurantSelection({ onSelectRestaurant }: RestaurantSelectionProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-orange-50 to-yellow-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <span className="text-4xl">🦕</span>
            <h1 className="text-4xl font-bold text-green-700">Dino Reserve</h1>
            <span className="text-4xl">🦖</span>
          </div>
          <p className="text-gray-600">Select a restaurant to manage reservations</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {restaurants.map((restaurant) => (
            <Card 
              key={restaurant.id} 
              className={`${restaurant.theme} hover:shadow-lg transition-shadow cursor-pointer transform hover:scale-105 transition-transform`}
            >
              <CardHeader className="text-center">
                <div className="text-6xl mb-2">{restaurant.emoji}</div>
                <CardTitle className="text-xl text-gray-800">
                  {restaurant.name}
                </CardTitle>
                <CardDescription className="text-sm">
                  {restaurant.dinoType} themed dining
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-gray-600 text-center">
                  {restaurant.description}
                </p>
                
                <div className="flex justify-between items-center">
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Available Tables</p>
                    <Badge 
                      variant={restaurant.availableTables > 15 ? "default" : restaurant.availableTables > 8 ? "secondary" : "destructive"}
                      className="text-lg px-3 py-1"
                    >
                      {restaurant.availableTables}/{restaurant.totalTables}
                    </Badge>
                  </div>
                  <div className="text-2xl">
                    {restaurant.availableTables > 15 ? '😋' : restaurant.availableTables > 8 ? '😐' : '😴'}
                  </div>
                </div>

                <Button 
                  onClick={() => onSelectRestaurant(restaurant.id)}
                  className="w-full bg-green-600 hover:bg-green-700 text-white"
                >
                  🍽️ Manage Tables
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center mt-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-md">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600">🦕 Dino Cave synced</span>
          </div>
        </div>
      </div>
    </div>
  );
}