'use client';

import { useState, useEffect } from 'react';
import { workersApi, Worker } from '@/lib/api';
import WorkforceOverview from '@/components/WorkforceOverview';
import WorkerTable from '@/components/WorkerTable';
import OverloadForm from '@/components/OverloadForm';
import RecommendationDisplay from '@/components/RecommendationDisplay';
import { AlertCircle, Loader2 } from 'lucide-react';

export default function Home() {
  const [workers, setWorkers] = useState<Worker[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<string | null>(null);
  const [recommendationLoading, setRecommendationLoading] = useState(false);

  useEffect(() => {
    loadWorkers();
  }, []);

  const loadWorkers = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await workersApi.getAll();
      setWorkers(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load workers. Make sure the backend is running.');
      console.error('Error loading workers:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGetRecommendations = async (input: string) => {
    try {
      setRecommendationLoading(true);
      setError(null);
      const response = await workersApi.getRecommendations(input);
      setRecommendations(response.data.recommendations);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get recommendations');
      console.error('Error getting recommendations:', err);
    } finally {
      setRecommendationLoading(false);
    }
  };

  const handleClearRecommendations = () => {
    setRecommendations(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-xl text-gray-600">Loading SmartShift...</p>
        </div>
      </div>
    );
  }

  if (error && workers.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md border border-red-200">
          <div className="flex items-center gap-3 mb-4">
            <AlertCircle className="w-8 h-8 text-red-500" />
            <h2 className="text-xl font-bold text-gray-900">Connection Error</h2>
          </div>
          <p className="text-gray-600 mb-4">{error}</p>
          <div className="bg-gray-50 p-4 rounded-lg mb-4">
            <p className="text-sm text-gray-700 mb-2"><strong>Make sure:</strong></p>
            <ul className="text-sm text-gray-600 space-y-1 list-disc list-inside">
              <li>Backend is running on port 8000</li>
              <li>Run: <code className="bg-gray-200 px-1 rounded">python api.py</code></li>
              <li>Check .env.local has correct API_URL</li>
            </ul>
          </div>
          <button
            onClick={loadWorkers}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🏭 SmartShift</h1>
          <p className="text-lg text-gray-600">AI-Powered Warehouse Workforce Rebalancing System</p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-red-800">Error</p>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        )}

        {/* Workforce Overview */}
        <div className="mb-8">
          <WorkforceOverview workers={workers} />
        </div>

        {/* Worker Table */}
        <div className="mb-8">
          <WorkerTable workers={workers} />
        </div>

        {/* Overload Form */}
        <div className="mb-8">
          <OverloadForm 
            onSubmit={handleGetRecommendations} 
            loading={recommendationLoading} 
          />
        </div>

        {/* Recommendations */}
        {recommendations && (
          <div className="mb-8">
            <RecommendationDisplay 
              recommendations={recommendations}
              onClear={handleClearRecommendations}
            />
          </div>
        )}

        {/* Footer */}
        <div className="mt-12 pt-8 border-t border-gray-200 text-center text-sm text-gray-500">
          <p>SmartShift v2.0 - Built with Next.js, FastAPI, and OpenRouter</p>
          <p className="mt-1">Powered by AI for efficient warehouse operations</p>
        </div>
      </div>
    </main>
  );
}

// Made with Bob
