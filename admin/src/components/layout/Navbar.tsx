import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import Button from '../ui/Button';

const Navbar: React.FC = () => {
  const location = useLocation();
  
  const navigation = [
    { name: 'Dashboard', href: '/' },
    { name: 'Attendance', href: '/attendance' },
    { name: 'Students', href: '/students' },
    { name: 'Venues', href: '/venues' },
  ];
  
  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-xl font-bold text-primary-600">AttendanceSystem</h1>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    isActive(item.href)
                      ? 'border-primary-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
          <div className="flex items-center">
            <Button 
              variant="secondary" 
              size="sm"
              onClick={() => {
                localStorage.removeItem('authToken');
                window.location.href = '/login';
              }}
            >
              Sign out
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;