import React, { useState } from 'react';
import { LoginPage } from './components/LoginPage';
import { RestaurantSelection } from './components/RestaurantSelection';
import { TableLayout } from './components/TableLayout';

type AppState = 'login' | 'restaurant-selection' | 'table-layout';

export default function App() {
  const [currentPage, setCurrentPage] = useState<AppState>('login');
  const [selectedRestaurant, setSelectedRestaurant] = useState<string>('');

  const handleLogin = () => {
    setCurrentPage('restaurant-selection');
  };

  const handleSelectRestaurant = (restaurantId: string) => {
    setSelectedRestaurant(restaurantId);
    setCurrentPage('table-layout');
  };

  const handleBackToRestaurants = () => {
    setCurrentPage('restaurant-selection');
    setSelectedRestaurant('');
  };

  return (
    <div className="min-h-screen">
      {currentPage === 'login' && (
        <LoginPage onLogin={handleLogin} />
      )}
      
      {currentPage === 'restaurant-selection' && (
        <RestaurantSelection onSelectRestaurant={handleSelectRestaurant} />
      )}
      
      {currentPage === 'table-layout' && selectedRestaurant && (
        <TableLayout 
          restaurantId={selectedRestaurant} 
          onBack={handleBackToRestaurants} 
        />
      )}
    </div>
  );
}