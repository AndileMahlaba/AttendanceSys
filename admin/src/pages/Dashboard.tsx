import React, { useState, useEffect } from 'react';
import Card from '../components/ui/Card';
import axios from '../services/api';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    totalStudents: 0,
    totalVenues: 0,
    todayAttendance: 0,
    weeklyAttendance: 0,
  });
  const [loading, setLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState('checking...');

  useEffect(() => {
    const testApiConnection = async () => {
      try {
        console.log('Testing API connection...');
        
        // First, test if we can reach the API at all
        const healthResponse = await axios.get('/health');
        console.log('Health check:', healthResponse.data);
        setApiStatus('API is connected ✓');
        
        // Try to get venues (if this endpoint exists)
        try {
          const venuesResponse = await axios.get('/venues');
          setStats(prev => ({ ...prev, totalVenues: venuesResponse.data.length || 0 }));
          console.log('Venues loaded:', venuesResponse.data);
        } catch (venueError) {
          console.log('Venues endpoint not available or error:', venueError);
          setStats(prev => ({ ...prev, totalVenues: 3 })); // Fallback data
        }
        
        // Try to get students
        try {
          const studentsResponse = await axios.get('/attendance/students');
          setStats(prev => ({ ...prev, totalStudents: studentsResponse.data.students?.length || 0 }));
          console.log('Students loaded:', studentsResponse.data);
        } catch (studentError) {
          console.log('Students endpoint not available or error:', studentError);
          setStats(prev => ({ ...prev, totalStudents: 25 })); // Fallback data
        }
        
        // Try to get attendance
        try {
          const attendanceResponse = await axios.get('/attendance/');
          setStats(prev => ({ ...prev, todayAttendance: attendanceResponse.data.attendance?.length || 0 }));
          console.log('Attendance loaded:', attendanceResponse.data);
        } catch (attendanceError) {
          console.log('Attendance endpoint not available or error:', attendanceError);
          setStats(prev => ({ ...prev, todayAttendance: 20 })); // Fallback data
        }
        
      } catch (error) {
        console.error('API connection failed:', error);
        setApiStatus('API connection failed ❌');
        // Use fallback data if API is not available
        setStats({
          totalStudents: 25,
          totalVenues: 3,
          todayAttendance: 20,
          weeklyAttendance: 85,
        });
      } finally {
        setLoading(false);
      }
    };

    testApiConnection();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p className="ml-4">Loading dashboard... {apiStatus}</p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
        <p className="text-blue-700">API Status: {apiStatus}</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="text-center">
          <h3 className="text-lg font-medium text-gray-500">Total Students</h3>
          <p className="text-3xl font-bold text-primary-600">{stats.totalStudents}</p>
        </Card>
        
        <Card className="text-center">
          <h3 className="text-lg font-medium text-gray-500">Total Venues</h3>
          <p className="text-3xl font-bold text-primary-600">{stats.totalVenues}</p>
        </Card>
        
        <Card className="text-center">
          <h3 className="text-lg font-medium text-gray-500">Today's Attendance</h3>
          <p className="text-3xl font-bold text-primary-600">{stats.todayAttendance}</p>
        </Card>
        
        <Card className="text-center">
          <h3 className="text-lg font-medium text-gray-500">Weekly Attendance</h3>
          <p className="text-3xl font-bold text-primary-600">{stats.weeklyAttendance}</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Student check-in</span>
              <span className="text-sm text-gray-400">2 minutes ago</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">New student registered</span>
              <span className="text-sm text-gray-400">5 minutes ago</span>
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="w-full text-left px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-md text-sm">
              Register New Student
            </button>
            <button className="w-full text-left px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-md text-sm">
              Create New Venue
            </button>
            <button className="w-full text-left px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-md text-sm">
              View Attendance Reports
            </button>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
