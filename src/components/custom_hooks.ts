// hooks/useRestaurants.ts
import { useState, useEffect } from 'react';
import { api, Restaurant } from '@/services/api';

export function useRestaurants() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRestaurants = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.restaurants.getAll();
      setRestaurants(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch restaurants');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRestaurants();
  }, []);

  return { restaurants, loading, error, refetch: fetchRestaurants };
}

// hooks/useTables.ts
import { useState, useEffect } from 'react';
import { api, Table } from '@/services/api';

export function useTables(restaurantId: number | null) {
  const [tables, setTables] = useState<Table[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTables = async () => {
    if (!restaurantId) return;

    try {
      setLoading(true);
      setError(null);
      const data = await api.restaurants.getTables(restaurantId);
      setTables(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tables');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (restaurantId) {
      fetchTables();
    }
  }, [restaurantId]);

  return { tables, loading, error, refetch: fetchTables };
}

// hooks/useReservation.ts
import { useState } from 'react';
import { api, CreateReservationData, UpdateReservationData } from '@/services/api';

export function useReservation() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createReservation = async (data: CreateReservationData) => {
    try {
      setLoading(true);
      setError(null);
      const result = await api.reservations.create(data);
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create reservation';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateReservation = async (id: number, data: UpdateReservationData) => {
    try {
      setLoading(true);
      setError(null);
      const result = await api.reservations.update(id, data);
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to update reservation';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const cancelReservation = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await api.reservations.cancel(id);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to cancel reservation';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    createReservation,
    updateReservation,
    cancelReservation,
    loading,
    error,
  };
}

// hooks/useInterval.ts
import { useEffect, useRef } from 'react';

export function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;

    const id = setInterval(() => savedCallback.current(), delay);
    return () => clearInterval(id);
  }, [delay]);
}

// hooks/useAutoRefresh.ts
import { useInterval } from './useInterval';

export function useAutoRefresh(callback: () => void, enabled: boolean = true, interval: number = 30000) {
  useInterval(enabled ? callback : null, interval);
}

// hooks/useLocalStorage.ts
import { useState, useEffect } from 'react';

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error('Error writing to localStorage:', error);
    }
  };

  return [storedValue, setValue] as const;
}

// hooks/useDebounce.ts
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// hooks/useToast.ts
import { useState, useCallback } from 'react';

export interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
}

export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((message: string, type: Toast['type'] = 'info') => {
    const id = Math.random().toString(36).substr(2, 9);
    setToasts((prev) => [...prev, { id, message, type }]);

    setTimeout(() => {
      setToasts((prev) => prev.filter((toast) => toast.id !== id));
    }, 5000);
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  return { toasts, addToast, removeToast };
}

// Export all hooks
export * from './useRestaurants';
export * from './useTables';
export * from './useReservation';
export * from './useInterval';
export * from './useAutoRefresh';
export * from './useLocalStorage';
export * from './useDebounce';
export * from './useToast';
