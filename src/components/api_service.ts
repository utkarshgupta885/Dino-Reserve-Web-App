// services/api.ts
// Centralized API service for all backend calls

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Type definitions
export interface Restaurant {
  id: number;
  name: string;
  location: string;
  dino_type: string;
}

export interface Table {
  id: number;
  table_number: number;
  capacity: number;
  restaurant_id: number;
  is_reserved: boolean;
  current_reservation?: Reservation | null;
}

export interface Reservation {
  id: number;
  table_id: number;
  customer_name: string;
  phone: string;
  party_size: number;
  reservation_time: string;
  status: string;
  created_at?: string;
}

export interface CreateReservationData {
  table_id: number;
  customer_name: string;
  phone: string;
  party_size: number;
  reservation_time: string;
}

export interface UpdateReservationData {
  customer_name?: string;
  phone?: string;
  party_size?: number;
  reservation_time?: string;
  status?: string;
}

// Error handling
class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Helper function for API calls
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.detail || `HTTP error! status: ${response.status}`,
        response.status,
        errorData
      );
    }

    // Handle empty responses (like DELETE)
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }
    
    return {} as T;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(
      error instanceof Error ? error.message : 'Network error occurred'
    );
  }
}

// Restaurant APIs
export const restaurantApi = {
  getAll: (): Promise<Restaurant[]> => {
    return apiRequest<Restaurant[]>('/restaurants');
  },

  getById: (id: number): Promise<Restaurant> => {
    return apiRequest<Restaurant>(`/restaurants/${id}`);
  },

  getTables: (restaurantId: number): Promise<Table[]> => {
    return apiRequest<Table[]>(`/restaurants/${restaurantId}/tables`);
  },
};

// Reservation APIs
export const reservationApi = {
  create: (data: CreateReservationData): Promise<Reservation> => {
    return apiRequest<Reservation>('/reservations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  update: (
    id: number,
    data: UpdateReservationData
  ): Promise<Reservation> => {
    return apiRequest<Reservation>(`/reservations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  cancel: (id: number): Promise<{ message: string; id: number }> => {
    return apiRequest(`/reservations/${id}`, {
      method: 'DELETE',
    });
  },

  getAll: (filters?: {
    restaurant_id?: number;
    status?: string;
  }): Promise<Reservation[]> => {
    const params = new URLSearchParams();
    if (filters?.restaurant_id) {
      params.append('restaurant_id', filters.restaurant_id.toString());
    }
    if (filters?.status) {
      params.append('status', filters.status);
    }
    
    const queryString = params.toString();
    const endpoint = queryString ? `/reservations?${queryString}` : '/reservations';
    
    return apiRequest<Reservation[]>(endpoint);
  },
};

// Health check
export const healthCheck = (): Promise<{ message: string }> => {
  return apiRequest<{ message: string }>('/');
};

// Export combined API object
export const api = {
  restaurants: restaurantApi,
  reservations: reservationApi,
  health: healthCheck,
};

export default api;
