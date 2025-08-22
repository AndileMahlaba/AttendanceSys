import axios from 'axios';

// Set base URL for all API requests
axios.defaults.baseURL = 'http://localhost:5000/api';

// Enable credentials for cross-origin requests
axios.defaults.withCredentials = true;

// Add request interceptor to include auth token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log('Making API request to:', config.url);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor to handle auth errors
axios.interceptors.response.use(
  (response) => {
    console.log('API response success:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API response error:', error.response?.status, error.config?.url, error.response?.data);
    
    // Temporarily comment out the auto-logout for debugging
    // if (error.response?.status === 401) {
    //   // Token expired or invalid, redirect to login
    //   localStorage.removeItem('authToken');
    //   localStorage.removeItem('user');
    //   window.location.href = '/login';
    // }
    return Promise.reject(error);
  }
);

export default axios;
