'use client';

import { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

interface OverloadFormProps {
  onSubmit: (input: string) => void;
  loading: boolean;
}

export default function OverloadForm({ onSubmit, loading }: OverloadFormProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
    }
  };

  const quickExamples = [
    { label: '📦 Packing Help', text: 'Zone C needs packing help for afternoon shift' },
    { label: '🚜 Forklift Help', text: 'Zone A dispatch is overloaded, need forklift help' },
    { label: '✅ Quality Inspector', text: 'Zone B is at 90% capacity, need quality inspector' },
  ];

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-900">🚨 Report Overload Situation</h2>
      
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="overload-input" className="block text-sm font-medium text-gray-700 mb-2">
              Describe the overload situation:
            </label>
            <textarea
              id="overload-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Example: Zone A dispatch is overloaded, need forklift help"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-gray-900 placeholder-gray-400"
              rows={4}
              disabled={loading}
            />
            <p className="mt-2 text-sm text-gray-500">
              Describe which zone is overloaded and what skill is needed
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Getting Recommendations...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Get AI Recommendations
                </>
              )}
            </button>

            {input && !loading && (
              <button
                type="button"
                onClick={() => setInput('')}
                className="px-4 py-3 text-gray-600 hover:text-gray-900 transition-colors"
              >
                Clear
              </button>
            )}
          </div>
        </form>

        {/* Quick Examples */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Quick Examples:</h3>
          <div className="flex flex-wrap gap-2">
            {quickExamples.map((example, index) => (
              <button
                key={index}
                onClick={() => setInput(example.text)}
                disabled={loading}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
              >
                {example.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// Made with Bob
