import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [symptoms, setSymptoms] = useState('');
  const [predictions, setPredictions] = useState([]);
  const [selectedDisease, setSelectedDisease] = useState(null);
  const [loading, setLoading] = useState(false);
  const [allDiseases, setAllDiseases] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  // Common symptoms for quick selection
  const commonSymptoms = [
    'fever', 'headache', 'cough', 'fatigue', 'nausea', 'vomiting',
    'abdominal_pain', 'chest_pain', 'dizziness', 'skin_rash', 'joint_pain',
    'breathlessness', 'sweating', 'chills', 'weight_loss', 'loss_of_appetite'
  ];

  useEffect(() => {
    fetchAllDiseases();
  }, []);

  const fetchAllDiseases = async () => {
    try {
      const response = await fetch(`${API_URL}/api/diseases`);
      const data = await response.json();
      setAllDiseases(data);
    } catch (error) {
      console.error('Error fetching diseases:', error);
    }
  };

  const analyzeSymptoms = async () => {
    if (!symptoms.trim()) {
      alert('Please enter some symptoms');
      return;
    }

    setLoading(true);
    try {
      const symptomList = symptoms.split(',').map(s => s.trim()).filter(s => s);
      
      const response = await fetch(`${API_URL}/api/predict-disease`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symptoms: symptomList
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze symptoms');
      }

      const data = await response.json();
      setPredictions(data);
      setCurrentView('results');
    } catch (error) {
      console.error('Error analyzing symptoms:', error);
      alert('Error analyzing symptoms. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const viewDiseaseDetails = async (diseaseId) => {
    try {
      const response = await fetch(`${API_URL}/api/disease/${diseaseId}`);
      const data = await response.json();
      setSelectedDisease(data);
      setCurrentView('details');
    } catch (error) {
      console.error('Error fetching disease details:', error);
    }
  };

  const addSymptom = (symptom) => {
    const currentSymptoms = symptoms.split(',').map(s => s.trim()).filter(s => s);
    if (!currentSymptoms.includes(symptom)) {
      setSymptoms(prevSymptoms => 
        prevSymptoms ? `${prevSymptoms}, ${symptom}` : symptom
      );
    }
  };

  const filteredDiseases = allDiseases.filter(disease =>
    disease.disease.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-purple-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-purple-700 rounded-lg flex items-center justify-center mr-3">
                <span className="text-white font-bold text-xl">🩺</span>
              </div>
              <h1 className="text-2xl font-bold text-gray-900">Curely 2.0</h1>
              <span className="ml-2 text-sm text-purple-600 font-medium">Smart Medical Assistant</span>
            </div>
            <nav className="flex space-x-6">
              <button
                onClick={() => setCurrentView('home')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  currentView === 'home'
                    ? 'bg-purple-100 text-purple-700'
                    : 'text-gray-600 hover:text-purple-600'
                }`}
              >
                Symptom Checker
              </button>
              <button
                onClick={() => setCurrentView('directory')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  currentView === 'directory'
                    ? 'bg-purple-100 text-purple-700'
                    : 'text-gray-600 hover:text-purple-600'
                }`}
              >
                Disease Directory
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Home View - Symptom Checker */}
        {currentView === 'home' && (
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="text-center py-12">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                AI-Powered Health Assessment
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Enter your symptoms and get instant insights about potential health conditions. 
                Our smart assistant analyzes symptoms and provides educational information.
              </p>
              <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg max-w-2xl mx-auto">
                <p className="text-sm text-yellow-800">
                  ⚠️ <strong>Medical Disclaimer:</strong> This tool is for educational purposes only. 
                  Always consult healthcare professionals for medical advice.
                </p>
              </div>
            </div>

            {/* Symptom Input */}
            <div className="bg-white rounded-xl shadow-lg p-8">
              <h3 className="text-2xl font-semibold text-gray-900 mb-6">Describe Your Symptoms</h3>
              
              {/* Quick Symptom Selection */}
              <div className="mb-6">
                <h4 className="text-lg font-medium text-gray-700 mb-3">Quick Selection (Click to Add):</h4>
                <div className="flex flex-wrap gap-2">
                  {commonSymptoms.map((symptom) => (
                    <button
                      key={symptom}
                      onClick={() => addSymptom(symptom)}
                      className="px-3 py-2 bg-purple-50 text-purple-700 rounded-lg text-sm font-medium 
                               hover:bg-purple-100 transition-colors border border-purple-200"
                    >
                      {symptom.replace('_', ' ')}
                    </button>
                  ))}
                </div>
              </div>

              {/* Text Input */}
              <div className="mb-6">
                <label htmlFor="symptoms" className="block text-lg font-medium text-gray-700 mb-3">
                  Enter symptoms (separated by commas):
                </label>
                <textarea
                  id="symptoms"
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  placeholder="e.g., fever, headache, cough, fatigue..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 
                           focus:ring-purple-500 focus:border-transparent resize-none"
                  rows="4"
                />
              </div>

              {/* Analyze Button */}
              <button
                onClick={analyzeSymptoms}
                disabled={loading || !symptoms.trim()}
                className="w-full bg-gradient-to-r from-purple-600 to-purple-700 text-white font-semibold 
                         py-4 px-6 rounded-lg hover:from-purple-700 hover:to-purple-800 
                         disabled:opacity-50 disabled:cursor-not-allowed transition-all transform 
                         hover:scale-105 focus:ring-4 focus:ring-purple-300"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                    Analyzing Symptoms...
                  </div>
                ) : (
                  'Analyze Symptoms'
                )}
              </button>
            </div>
          </div>
        )}

        {/* Results View */}
        {currentView === 'results' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold text-gray-900">Analysis Results</h2>
              <button
                onClick={() => setCurrentView('home')}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 
                         transition-colors font-medium"
              >
                ← Back to Checker
              </button>
            </div>

            {predictions.length === 0 ? (
              <div className="bg-white rounded-xl shadow-lg p-8 text-center">
                <div className="text-6xl mb-4">🤔</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No Matches Found</h3>
                <p className="text-gray-600">
                  We couldn't find any conditions matching your symptoms. 
                  Try different or more specific symptoms.
                </p>
              </div>
            ) : (
              <div className="grid gap-6">
                {predictions.map((prediction, index) => (
                  <div
                    key={prediction.id}
                    className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer"
                    onClick={() => viewDiseaseDetails(prediction.id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center mb-3">
                          <span className="text-2xl mr-3">
                            {index === 0 ? '🎯' : index === 1 ? '🔍' : '💡'}
                          </span>
                          <h3 className="text-xl font-bold text-gray-900">{prediction.disease}</h3>
                          <span className={`ml-3 px-3 py-1 rounded-full text-sm font-semibold ${
                            prediction.confidence >= 70 
                              ? 'bg-green-100 text-green-800'
                              : prediction.confidence >= 50
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {prediction.confidence}% match
                          </span>
                        </div>
                        
                        <p className="text-gray-600 mb-4">{prediction.description}</p>
                        
                        <div className="grid md:grid-cols-2 gap-4">
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">Matching Symptoms:</h4>
                            <div className="flex flex-wrap gap-1">
                              {prediction.matching_symptoms.slice(0, 5).map((symptom, idx) => (
                                <span key={idx} className="px-2 py-1 bg-purple-100 text-purple-700 
                                                       rounded text-sm">
                                  {symptom.replace('_', ' ')}
                                </span>
                              ))}
                              {prediction.matching_symptoms.length > 5 && (
                                <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-sm">
                                  +{prediction.matching_symptoms.length - 5} more
                                </span>
                              )}
                            </div>
                          </div>
                          
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">Quick Precautions:</h4>
                            <ul className="text-sm text-gray-600 space-y-1">
                              {prediction.precautions.slice(0, 3).map((precaution, idx) => (
                                <li key={idx} className="flex items-start">
                                  <span className="text-purple-500 mr-2">•</span>
                                  {precaution}
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                      
                      <div className="ml-4 flex flex-col items-center">
                        <div className="text-2xl font-bold text-purple-600">#{index + 1}</div>
                        <button className="mt-2 text-purple-600 hover:text-purple-700 font-medium text-sm">
                          View Details →
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Disease Details View */}
        {currentView === 'details' && selectedDisease && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold text-gray-900">{selectedDisease.disease}</h2>
              <button
                onClick={() => setCurrentView('results')}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 
                         transition-colors font-medium"
              >
                ← Back to Results
              </button>
            </div>

            <div className="grid lg:grid-cols-2 gap-8">
              {/* Description */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  📋 Description
                </h3>
                <p className="text-gray-700 leading-relaxed">{selectedDisease.description}</p>
              </div>

              {/* All Symptoms */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  🩺 All Symptoms
                </h3>
                <div className="flex flex-wrap gap-2">
                  {selectedDisease.symptoms.map((symptom, index) => (
                    <span key={index} className="px-3 py-2 bg-red-50 text-red-700 rounded-lg text-sm font-medium">
                      {symptom.replace('_', ' ')}
                    </span>
                  ))}
                </div>
              </div>

              {/* Precautions */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  ⚠️ Precautions
                </h3>
                <ul className="space-y-3">
                  {selectedDisease.precautions.map((precaution, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-orange-500 mr-3 text-lg">•</span>
                      <span className="text-gray-700">{precaution}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Medicines */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  💊 Common Medicines
                </h3>
                <div className="space-y-2">
                  {selectedDisease.medicines.map((medicine, index) => (
                    <div key={index} className="px-3 py-2 bg-green-50 text-green-700 rounded-lg text-sm font-medium">
                      {medicine}
                    </div>
                  ))}
                </div>
                <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-xs text-yellow-800">
                    ⚠️ Always consult a healthcare professional before taking any medication.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Disease Directory View */}
        {currentView === 'directory' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold text-gray-900">Disease Directory</h2>
              <div className="flex items-center space-x-4">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search diseases..."
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 
                           focus:border-transparent"
                />
                <span className="text-sm text-gray-500">
                  {filteredDiseases.length} diseases
                </span>
              </div>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredDiseases.map((disease) => (
                <div
                  key={disease.id}
                  className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer"
                  onClick={() => viewDiseaseDetails(disease.id)}
                >
                  <h3 className="text-lg font-bold text-gray-900 mb-3">{disease.disease}</h3>
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">Common Symptoms:</h4>
                    <div className="flex flex-wrap gap-1">
                      {disease.symptoms.slice(0, 4).map((symptom, idx) => (
                        <span key={idx} className="px-2 py-1 bg-purple-50 text-purple-700 rounded text-xs">
                          {symptom.replace('_', ' ')}
                        </span>
                      ))}
                      {disease.symptoms.length > 4 && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                          +{disease.symptoms.length - 4} more
                        </span>
                      )}
                    </div>
                  </div>
                  <button className="text-purple-600 hover:text-purple-700 font-medium text-sm">
                    View Details →
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-600">
              © 2025 Curely 2.0 - Smart Medical Assistant | For Educational Purposes Only
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Always consult healthcare professionals for medical advice and treatment
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;