import React, { useState } from 'react';
import axios from 'axios';

const RiskCalculator = () => {
  const [formData, setFormData] = useState({
    disease_name: '',
    temperature: '',
    humidity: '',
    rainfall: '',
    location: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const diseases = [
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Pepper__bell___Bacterial_spot'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCalculate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:5001/api/weather-risk', {
        disease_name: formData.disease_name,
        weather_data: {
          temperature: parseFloat(formData.temperature),
          humidity: parseFloat(formData.humidity),
          rainfall: parseFloat(formData.rainfall),
          location: formData.location
        }
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Error calculating risk');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    if (level > 0.7) return 'text-red-600 bg-red-100';
    if (level > 0.4) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  const getRiskCategory = (level) => {
    if (level > 0.7) return 'High Risk';
    if (level > 0.4) return 'Medium Risk';
    return 'Low Risk';
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2 text-green-700">Disease Risk Calculator</h1>
      <p className="text-gray-600 mb-8">Calculate disease risk based on weather conditions</p>

      <div className="bg-white rounded-lg shadow p-8">
        <form onSubmit={handleCalculate} className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Disease</label>
              <select
                name="disease_name"
                value={formData.disease_name}
                onChange={handleChange}
                className="w-full px-6 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                required
              >
                <option value="">Select a disease</option>
                {diseases.map(disease => (
                  <option key={disease} value={disease}>
                    {disease.replace(/_/g, ' ')}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="Enter location"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Temperature (°C)</label>
              <input
                type="number"
                name="temperature"
                value={formData.temperature}
                onChange={handleChange}
                placeholder="e.g., 25"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Humidity (%)</label>
              <input
                type="number"
                name="humidity"
                value={formData.humidity}
                onChange={handleChange}
                placeholder="e.g., 75"
                min="0"
                max="100"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Rainfall (mm)</label>
              <input
                type="number"
                name="rainfall"
                value={formData.rainfall}
                onChange={handleChange}
                placeholder="e.g., 0"
                min="0"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                required
              />
            </div>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition"
          >
            {loading ? 'Calculating...' : 'Calculate Risk'}
          </button>
        </form>

        {result && (
          <div className="mt-8 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Risk Assessment Result</h2>

            <div className="grid grid-cols-3 gap-6">
              <div className="bg-white rounded-lg p-6 text-center">
                <p className="text-sm text-gray-600 mb-2">Disease</p>
                <p className="text-lg font-bold text-gray-800">{result.disease.replace(/_/g, ' ')}</p>
              </div>

              <div className="bg-white rounded-lg p-6 text-center">
                <p className="text-sm text-gray-600 mb-2">Risk Level</p>
                <p className={`text-4xl font-bold ${getRiskColor(result.risk_level)}`}>
                  {(result.risk_level * 100).toFixed(1)}%
                </p>
              </div>

              <div className="bg-white rounded-lg p-6 text-center">
                <p className="text-sm text-gray-600 mb-2">Category</p>
                <p className={`text-lg font-bold px-4 py-2 rounded-lg inline-block ${getRiskColor(result.risk_level)}`}>
                  {getRiskCategory(result.risk_level)}
                </p>
              </div>
            </div>

            <div className="mt-6 bg-white rounded-lg p-6">
              <h3 className="font-bold text-gray-800 mb-3">Recommendations</h3>
              <ul className="list-disc list-inside space-y-2 text-gray-700">
                {result.risk_level > 0.7 && (
                  <>
                    <li>Consider preventive spraying immediately</li>
                    <li>Monitor plants closely for early symptoms</li>
                    <li>Implement strict plant hygiene measures</li>
                  </>
                )}
                {result.risk_level > 0.4 && result.risk_level <= 0.7 && (
                  <>
                    <li>Maintain good air circulation</li>
                    <li>Monitor weather conditions closely</li>
                    <li>Apply preventive treatments when needed</li>
                  </>
                )}
                {result.risk_level <= 0.4 && (
                  <>
                    <li>Maintain normal care practices</li>
                    <li>Continue regular monitoring</li>
                    <li>Update conditions if weather changes</li>
                  </>
                )}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RiskCalculator;
