import React, { useState } from 'react';
import DiseaseDetector from './components/DiseaseDetector';
import History from './components/History';
import Reminders from './components/Reminders';
import RiskCalculator from './components/RiskCalculator';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('detector');
  const [userId, setUserId] = useState(localStorage.getItem('userId') || '');
  const [password, setPassword] = useState('');
  const [authError, setAuthError] = useState('');
  const [showUserSetup, setShowUserSetup] = useState(!userId);

  const handleSetUserId = (e) => {
    e.preventDefault();
    const trimmedUserId = userId.trim();
    const trimmedPassword = password.trim();
    const expectedPassword = trimmedUserId.split('').reverse().join('');

    if (trimmedUserId && trimmedPassword && trimmedPassword === expectedPassword) {
      localStorage.setItem('userId', userId);
      setAuthError('');
      setShowUserSetup(false);
    } else {
      setAuthError('Invalid password. Use your username reversed (example: ramu -> umar).');
    }
  };

  if (showUserSetup) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-500 to-green-700 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md w-full">
          <h1 className="text-3xl font-bold text-green-700 mb-2 text-center">Plant Disease AI</h1>
          <p className="text-gray-600 text-center mb-8">Intelligent detection and treatment recommendations</p>

          <form onSubmit={handleSetUserId}>
            <label className="block text-sm font-medium text-gray-700 mb-2">Enter Your Name</label>
            <input
              type="text"
              value={userId}
              onChange={(e) => {
                setUserId(e.target.value);
                if (authError) setAuthError('');
              }}
              placeholder="Your name or ID"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent mb-4"
              required
            />
            <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                if (authError) setAuthError('');
              }}
              placeholder="Enter your password"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent mb-4"
              required
            />
            {authError && <p className="text-sm text-red-600 mb-4">{authError}</p>}
            <button
              type="submit"
              className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg transition"
            >
              Get Started
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Navigation */}
      <nav className="bg-gradient-to-r from-green-600 to-green-700 shadow-lg">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-white">🌱 Plant Disease Detector</h1>
            <button
              onClick={() => {
                localStorage.removeItem('userId');
                setShowUserSetup(true);
              }}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition"
            >
              Logout
            </button>
          </div>

          {/* Tab Navigation */}
          <div className="flex gap-2 flex-wrap">
            {[
              { id: 'detector', label: '📸 Detect Disease' },
              { id: 'history', label: '📋 History' },
              { id: 'calculator', label: '📊 Risk Calculator' },
              { id: 'reminders', label: '⏰ Reminders' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-2 rounded-lg font-semibold transition ${
                  activeTab === tab.id
                    ? 'bg-white text-green-700'
                    : 'text-white hover:bg-green-500'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* User Info */}
      <div className="bg-green-100 text-green-800 px-6 py-3 border-b border-green-300">
        <p className="text-sm">Welcome, <strong>{localStorage.getItem('userId')}</strong>!</p>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto flex-1 w-full">
        {activeTab === 'detector' && <DiseaseDetector />}
        {activeTab === 'history' && <History />}
        {activeTab === 'calculator' && <RiskCalculator />}
        {activeTab === 'reminders' && <Reminders />}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white text-center py-6 mt-auto">
        <p>© 2024 Plant Disease AI - Powered by Deep Learning | Hackathon Project</p>
      </footer>
    </div>
  );
}

export default App;
