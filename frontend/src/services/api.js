// src/services/api.js

import axios from 'axios';

// Create axios instance with custom config
const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Thay đổi URL này theo API của bạn
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('token');
    
    // If token exists, add it to request headers
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't tried to refresh token yet
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh token
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await api.post('/auth/token/refresh/', {
          refresh: refreshToken
        });

        // If refresh successful, update token
        if (response.data.access) {
          localStorage.setItem('token', response.data.access);
          
          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // If refresh fails, logout user
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// API endpoints
export const endpoints = {
  // Auth endpoints
  auth: {
    login: (data) => api.post('/auth/login/', data),
    register: (data) => api.post('/auth/register/', data),
    refreshToken: (refresh) => api.post('/auth/token/refresh/', { refresh }),
    logout: () => api.post('/auth/logout/'),
  },

  // Books endpoints
  books: {
    list: (params) => api.get('/books/', { params }),
    detail: (id) => api.get(`/books/${id}/`),
    create: (data) => api.post('/books/', data),
    update: (id, data) => api.put(`/books/${id}/`, data),
    delete: (id) => api.delete(`/books/${id}/`),
    updateStock: (id, quantity) => api.patch(`/books/${id}/update_stock/`, { quantity }),
  },

  // Cart endpoints
  cart: {
    get: () => api.get('/carts/'),
    addItem: (data) => api.post(`/carts/add_item/`, data),
    updateItem: (id, data) => api.put(`/cart-items/${id}/`, data),
    removeItem: (cartId, data) => api.post(`/carts/${cartId}/remove_item/`, data),
    clear: (cartId) => api.post(`/carts/${cartId}/clear/`),
    getItems: () => api.get('/cart-items/'),
  },

  // Customer endpoints
  customers: {
    get: () => api.get('/customers/'),
    detail: (id) => api.get(`/customers/${id}/`),
    create: (data) => api.post('/customers/', data),
    update: (id, data) => api.put(`/customers/${id}/`, data),
    delete: (id) => api.delete(`/customers/${id}/`),
  },

  // Orders endpoints
  orders: {
    list: () => api.get('/orders/'),
    detail: (id) => api.get(`/orders/${id}/`),
    create: (data) => api.post('/orders/', data),
    update: (id, data) => api.put(`/orders/${id}/`, data),
    cancel: (id) => api.post(`/orders/${id}/cancel/`),
  },
};

// Helper functions
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error
    const status = error.response.status;
    const data = error.response.data;

    switch (status) {
      case 400:
        return {
          type: 'validation',
          message: 'Please check your input',
          errors: data
        };
      case 401:
        return {
          type: 'auth',
          message: 'Please login to continue'
        };
      case 403:
        return {
          type: 'permission',
          message: 'You do not have permission to perform this action'
        };
      case 404:
        return {
          type: 'not_found',
          message: 'The requested resource was not found'
        };
      case 500:
        return {
          type: 'server',
          message: 'Internal server error'
        };
      default:
        return {
          type: 'unknown',
          message: 'An unknown error occurred'
        };
    }
  } else if (error.request) {
    // Request was made but no response
    return {
      type: 'network',
      message: 'Network error. Please check your connection'
    };
  } else {
    // Something else happened
    return {
      type: 'unknown',
      message: error.message
    };
  }
};

// Example usage of error handling
export const safeRequest = async (apiCall) => {
  try {
    const response = await apiCall();
    return { data: response.data, error: null };
  } catch (error) {
    const errorData = handleApiError(error);
    return { data: null, error: errorData };
  }
};

// Export default api instance
export default api;