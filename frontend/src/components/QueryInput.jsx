import React, { useState } from 'react';
import { sendQuery } from '../utils/api';

export default function QueryInput({ onResponse }) {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    setIsLoading(true);
    try {
      const result = await sendQuery(query, { show_chain: true });
      onResponse(result);
    } catch (error) {
      console.error('Error submitting query:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-6 border border-pastel-purple/30">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <input
            type="text"
            placeholder="What would you like to research today?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full px-4 py-3 pr-12 border-2 border-pastel-lavender rounded-xl focus:outline-none focus:border-accent-purple transition-colors bg-white/50 text-gray-700 placeholder-gray-400"
            disabled={isLoading}
          />
          {query && (
            <button
              type="button"
              onClick={() => setQuery('')}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
            >
              ✕
            </button>
          )}
        </div>
        
        <button
          type="submit"
          disabled={!query.trim() || isLoading}
          className="w-full py-3 px-6 bg-gradient-to-r from-accent-purple to-accent-blue text-white font-medium rounded-xl hover:from-accent-blue hover:to-accent-purple transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Researching...
            </span>
          ) : (
            'Start Research'
          )}
        </button>
      </form>

      <div className="mt-4 flex flex-wrap gap-2">
        <span className="text-xs text-gray-500">Try:</span>
        {['What is AI?', 'Calculate 25*4', 'Latest tech news'].map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => setQuery(suggestion)}
            className="text-xs px-3 py-1 bg-pastel-lavender text-gray-700 rounded-full hover:bg-pastel-purple transition-colors"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
}
