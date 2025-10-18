import React, { useState } from 'react';
import QueryInput from './components/QueryInput';
import AgentTimeline from './components/AgentTimeline';

function App() {
  const [responseData, setResponseData] = useState(null);

  const handleNewResponse = (data) => {
    setResponseData(data);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pastel-pink via-pastel-blue to-pastel-mint">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-light text-gray-800 mb-2">
            AI Research Assistant
          </h1>
          <p className="text-gray-600 text-sm">
            Powered by LangChain & Google Gemini
          </p>
        </header>

        {/* Main Content */}
        <main className="space-y-8">
          <QueryInput onResponse={handleNewResponse} />
          
          {responseData && (
            <div className="animate-fade-in">
              <AgentTimeline
                timeline={responseData.timeline}
                summary={responseData.summary}
                toolsUsed={responseData.tools_used}
                chainUsed={responseData.chain_used}
              />
            </div>
          )}
        </main>

        {/* Footer */}
        <footer className="text-center mt-16 text-xs text-gray-500">
        </footer>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.5s ease-out;
        }
      `}</style>
    </div>
  );
}

export default App;
