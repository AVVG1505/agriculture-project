import React, { useState, useEffect } from 'react';
import axios from 'axios';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const userId = localStorage.getItem('userId') || 'anonymous';
      const response = await axios.get(`http://localhost:5001/api/history/${userId}`);
      setHistory(response.data.history);
    } catch (err) {
      setError('Error fetching history');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-8">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8 text-green-700">Detection History</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {history.length === 0 ? (
        <div className="bg-gray-100 rounded-lg p-8 text-center">
          <p className="text-gray-600">No detection history yet. Start by detecting a disease!</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {history.map((item) => (
            <div key={item.id} className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-bold text-gray-800">{item.detected_disease}</h3>
                  <p className="text-sm text-gray-600 mt-1">
                    {new Date(item.timestamp).toLocaleDateString()} at {new Date(item.timestamp).toLocaleTimeString()}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-blue-600">{(item.confidence * 100).toFixed(1)}%</p>
                  <p className="text-xs text-gray-500">Confidence</p>
                </div>
              </div>
              {item.notes && (
                <p className="text-gray-700 mt-3 text-sm">{item.notes}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;
