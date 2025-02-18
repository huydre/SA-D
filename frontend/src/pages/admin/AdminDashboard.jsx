import React, { useState } from 'react';
import BookManagement from './BookManagement';
import CustomerManagement from './CustomerManagement';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('books');

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold mb-8">Admin Dashboard</h1>

        {/* Navigation Tabs */}
        <div className="flex space-x-4 mb-6">
          <button
            className={`px-4 py-2 rounded ${activeTab === 'books' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => setActiveTab('books')}
          >
            Books
          </button>
          <button
            className={`px-4 py-2 rounded ${activeTab === 'customers' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
            onClick={() => setActiveTab('customers')}
          >
            Customers
          </button>
        </div>

        {/* Content Area */}
        <div className="bg-white p-6 rounded-lg shadow">
          {activeTab === 'books' && <BookManagement />}
          {activeTab === 'customers' && <CustomerManagement />}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;