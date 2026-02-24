import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Reminders = () => {
  const [reminders, setReminders] = useState([]);
  const [newReminder, setNewReminder] = useState({
    plant_type: '',
    reminder_text: '',
    frequency: 'weekly'
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReminders();
  }, []);

  const fetchReminders = async () => {
    try {
      const userId = localStorage.getItem('userId') || 'anonymous';
      const response = await axios.get(`http://localhost:5001/api/reminders/${userId}`);
      setReminders(response.data.reminders);
    } catch (err) {
      console.error('Error fetching reminders');
    } finally {
      setLoading(false);
    }
  };

  const handleAddReminder = async (e) => {
    e.preventDefault();
    try {
      const userId = localStorage.getItem('userId') || 'anonymous';
      await axios.post('http://localhost:5001/api/reminders', {
        user_id: userId,
        ...newReminder
      });
      setNewReminder({ plant_type: '', reminder_text: '', frequency: 'weekly' });
      fetchReminders();
    } catch (err) {
      console.error('Error adding reminder');
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8 text-green-700">Crop Care Reminders</h1>

      {/* Add Reminder Form */}
      <div className="bg-white rounded-lg shadow p-8 mb-10">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Add New Reminder</h2>
        <form onSubmit={handleAddReminder} className="space-y-5">
          <div className="grid grid-cols-2 gap-5">
            <select
              value={newReminder.plant_type}
              onChange={(e) => setNewReminder({ ...newReminder, plant_type: e.target.value })}
              className="w-full px-5 py-3 text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              required
            >
              <option value="">Select Plant Type</option>
              <option value="Tomato">Tomato</option>
              <option value="Potato">Potato</option>
              <option value="Pepper">Pepper</option>
            </select>

            <select
              value={newReminder.frequency}
              onChange={(e) => setNewReminder({ ...newReminder, frequency: e.target.value })}
              className="w-full px-5 py-3 text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            >
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="bi-weekly">Bi-weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>

          <textarea
            value={newReminder.reminder_text}
            onChange={(e) => setNewReminder({ ...newReminder, reminder_text: e.target.value })}
            placeholder="Enter reminder text..."
            className="w-full px-5 py-3 text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            rows="4"
            required
          ></textarea>

          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-5 rounded-lg transition"
          >
            Add Reminder
          </button>
        </form>
      </div>

      {/* Reminders List */}
      {loading ? (
        <div className="text-center py-8">Loading reminders...</div>
      ) : reminders.length === 0 ? (
        <div className="bg-gray-100 rounded-lg p-8 text-center">
          <p className="text-gray-600">No reminders yet. Add one to get started!</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {reminders.map((reminder) => (
            <div key={reminder.id} className="bg-white rounded-lg shadow p-6 border-l-4 border-green-600">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-800">{reminder.plant_type}</h3>
                  <p className="text-gray-700 mt-2">{reminder.reminder_text}</p>
                  <div className="flex gap-4 mt-3">
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      {reminder.frequency}
                    </span>
                    {reminder.last_sent && (
                      <span className="text-xs text-gray-500">
                        Last sent: {new Date(reminder.last_sent).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Reminders;
