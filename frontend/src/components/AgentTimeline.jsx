import React from 'react';
import { formatLLMResponse } from '../utils/textFormatter';

export default function AgentTimeline({ timeline = [], summary, toolsUsed = [], chainUsed = '' }) {
  const getToolIcon = (tool) => {
    switch (tool?.toLowerCase()) {
      case 'search':
        return '🔍';
      case 'calculator':
        return '🧮';
      case 'reasoning':
        return '🧠';
      default:
        return '⚡';
    }
  };

  const getToolColor = (tool) => {
    switch (tool?.toLowerCase()) {
      case 'search':
        return 'bg-pastel-blue border-accent-blue';
      case 'calculator':
        return 'bg-pastel-green border-accent-green';
      case 'reasoning':
        return 'bg-pastel-purple border-accent-purple';
      default:
        return 'bg-pastel-lavender border-accent-purple';
    }
  };

  return (
    <div className="space-y-6">
      {/* Processing Info */}
      {(toolsUsed.length > 0 || chainUsed) && (
        <div className="bg-white/70 backdrop-blur-sm rounded-xl p-4 border border-pastel-mint/50">
          <div className="flex flex-wrap items-center gap-4 text-sm">
            {toolsUsed.length > 0 && (
              <div className="flex items-center gap-2">
                <span className="text-gray-600">Tools used:</span>
                <div className="flex gap-2">
                  {toolsUsed.map((tool, idx) => (
                    <span
                      key={idx}
                      className={`px-2 py-1 rounded-full text-xs font-medium border ${getToolColor(tool)}`}
                    >
                      {getToolIcon(tool)} {tool}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {chainUsed && (
              <div className="text-gray-500 text-xs">
                Chain: {chainUsed}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Timeline Steps */}
      {timeline && timeline.length > 0 && (
        <div className="bg-white/70 backdrop-blur-sm rounded-xl p-6 border border-pastel-peach/50">
          <h3 className="text-lg font-light text-gray-800 mb-4">Research Process</h3>
          <div className="space-y-3">
            {timeline.map((step, idx) => (
              <div key={idx} className="flex gap-3 items-start">
                <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-accent-purple to-accent-blue rounded-full flex items-center justify-center text-white text-sm font-medium">
                  {step.step || idx + 1}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium text-gray-800">
                      {step.tool || 'Processing'}
                    </span>
                    <span className="text-xs text-gray-500">
                      {getToolIcon(step.tool)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 leading-relaxed">
                    {formatLLMResponse(step.output_summary || step.output || 'Processing...')}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Final Summary */}
      {summary && (
        <div className="bg-gradient-to-r from-pastel-lavender to-pastel-mint rounded-xl p-6 border border-pastel-purple/30 shadow-lg">
          <h3 className="text-lg font-light text-gray-800 mb-3 flex items-center gap-2">
            <span className="text-2xl">✨</span>
            Research Summary
          </h3>
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {formatLLMResponse(summary)}
            </p>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="flex justify-center gap-3">
        <button
          onClick={() => window.navigator.clipboard.writeText(formatLLMResponse(summary))}
          className="px-4 py-2 bg-pastel-yellow text-gray-700 rounded-lg hover:bg-pastel-orange transition-colors text-sm font-medium"
        >
          📋 Copy Summary
        </button>
        <button
          onClick={() => window.print()}
          className="px-4 py-2 bg-pastel-sky text-gray-700 rounded-lg hover:bg-pastel-blue transition-colors text-sm font-medium"
        >
          🖨️ Print
        </button>
      </div>
    </div>
  );
}
