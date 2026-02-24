import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

const DiseaseDetector = () => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [location, setLocation] = useState('');

  const onDrop = useCallback(acceptedFiles => {
    const file = acceptedFiles[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(file);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif']
    }
  });

  const handleDetect = async () => {
    if (!image) {
      setError('Please select an image');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', image);
      formData.append('location', location);
      formData.append('user_id', localStorage.getItem('userId') || 'anonymous');

      const response = await axios.post('http://localhost:5001/api/detect', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Error detecting disease');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    const colors = {
      'Severe': 'bg-red-100 text-red-800',
      'Moderate': 'bg-yellow-100 text-yellow-800',
      'Mild': 'bg-green-100 text-green-800'
    };
    return colors[severity] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-2 text-green-700">Plant Disease Detector</h1>
        <p className="text-gray-600 mb-8">Upload an image of a plant leaf to detect diseases and get treatment recommendations</p>

        {/* Upload Section */}
        <div className="mb-8">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition ${
              isDragActive
                ? 'border-green-500 bg-green-50'
                : 'border-gray-300 hover:border-green-400'
            }`}
          >
            <input {...getInputProps()} />
            {preview ? (
              <img src={preview} alt="Preview" className="max-h-64 mx-auto rounded-lg mb-4" />
            ) : (
              <div>
                <p className="text-lg font-semibold mb-2">
                  {isDragActive ? 'Drop the image here...' : 'Drag and drop an image, or click to select'}
                </p>
                <p className="text-sm text-gray-500">Supported formats: JPG, PNG, GIF</p>
              </div>
            )}
          </div>
        </div>

        {/* Location Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Location (optional)</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter your location for weather-based risk assessment"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          />
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Detect Button */}
        <button
          onClick={handleDetect}
          disabled={!image || loading}
          className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition mb-8"
        >
          {loading ? 'Analyzing Image...' : 'Detect Disease'}
        </button>

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            <div className="border-t-2 pt-6">
              <h2 className="text-2xl font-bold mb-6 text-gray-800">Detection Results</h2>

              {/* Main Prediction */}
              <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-6 mb-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-blue-900">{result.detected_disease}</h3>
                    <p className="text-gray-700">{result.disease_info.name}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-3xl font-bold text-blue-600">{(result.confidence * 100).toFixed(1)}%</p>
                    <p className="text-sm text-gray-600">Confidence</p>
                  </div>
                </div>

                {/* Severity and Risk */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm font-semibold text-gray-700 mb-1">Severity Level</p>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getSeverityColor(result.severity)}`}>
                      {result.severity}
                    </span>
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-700 mb-1">Disease Risk</p>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getSeverityColor(result.risk_level > 0.7 ? 'Severe' : result.risk_level > 0.4 ? 'Moderate' : 'Mild')}`}>
                      {(result.risk_level * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Disease Description */}
              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <h4 className="text-lg font-bold text-gray-800 mb-3">About This Disease</h4>
                <p className="text-gray-700 mb-4">{result.disease_info.description}</p>

                {result.disease_info.causes.length > 0 && (
                  <div className="mb-4">
                    <h5 className="font-semibold text-gray-800 mb-2">Common Causes:</h5>
                    <ul className="list-disc list-inside text-gray-700">
                      {result.disease_info.causes.map((cause, idx) => (
                        <li key={idx}>{cause}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Treatment Recommendations */}
              {result.treatments.length > 0 && (
                <div className="bg-green-50 rounded-lg p-6 mb-6">
                  <h4 className="text-lg font-bold text-green-800 mb-4">Recommended Treatments</h4>
                  <div className="space-y-4">
                    {result.treatments.map((treatment, idx) => (
                      <div key={idx} className="bg-white rounded-lg p-4 border-l-4 border-green-600">
                        <div className="flex justify-between items-start mb-2">
                          <h5 className="font-bold text-gray-800">{idx + 1}. {treatment.name}</h5>
                          <span className="bg-green-200 text-green-800 text-xs px-2 py-1 rounded">
                            {treatment.effectiveness}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2"><strong>Dosage:</strong> {treatment.dosage}</p>
                        <p className="text-sm text-gray-700 mb-2"><strong>Frequency:</strong> {treatment.frequency}</p>
                        <p className="text-sm text-gray-700"><strong>Cost:</strong> {treatment.cost}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Prevention Measures */}
              {result.disease_info.prevention.length > 0 && (
                <div className="bg-purple-50 rounded-lg p-6">
                  <h4 className="text-lg font-bold text-purple-800 mb-4">Prevention & Management</h4>
                  <ul className="list-disc list-inside text-gray-700 space-y-2">
                    {result.disease_info.prevention.map((measure, idx) => (
                      <li key={idx}>{measure}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Top Predictions */}
              <div className="mt-8 bg-gray-100 rounded-lg p-6">
                <h4 className="text-lg font-bold text-gray-800 mb-4">Alternative Predictions</h4>
                <div className="space-y-2">
                  {result.top_3_predictions.map((pred, idx) => (
                    <div key={idx} className="flex justify-between items-center">
                      <span className="text-gray-700">{idx + 1}. {pred.disease}</span>
                      <div className="w-48 bg-gray-300 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${pred.confidence * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-gray-700 font-semibold ml-4">{(pred.confidence * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DiseaseDetector;
