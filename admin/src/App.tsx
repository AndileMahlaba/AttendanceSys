import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';

// Protected route component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = localStorage.getItem('authToken');
  console.log('ProtectedRoute - Token:', token);
  return token ? <>{children}</> : <Navigate to="/login" replace />;
};

// Public route component (redirect to dashboard if already logged in)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = localStorage.getItem('authToken');
  console.log('PublicRoute - Token:', token);
  return !token ? <>{children}</> : <Navigate to="/" replace />;
};

const App: React.FC = () => {
  useEffect(() => {
    console.log('App mounted - Checking auth token:', localStorage.getItem('authToken'));
  }, []);

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          } 
        />
        <Route 
          path="/register" 
          element={
            <PublicRoute>
              <Register />
            </PublicRoute>
          } 
        />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <Layout>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/attendance" element={<div>Attendance Page - Coming Soon</div>} />
                  <Route path="/students" element={<div>Students Page - Coming Soon</div>} />
                  <Route path="/venues" element={<div>Venues Page - Coming Soon</div>} />
                </Routes>
              </Layout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
