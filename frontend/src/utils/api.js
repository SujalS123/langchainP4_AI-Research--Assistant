const API_BASE_URL = 'https://langchainp4-ai-research-assistant.onrender.com';

export const sendQuery = async (query, options = {}) => {
  try {
    // Add timeout to prevent hanging
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    const response = await fetch(`${API_BASE_URL}/api/query`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ query, options }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      let errorMessage = `HTTP error! status: ${response.status}`;
      
      if (response.status === 422) {
        errorMessage = 'Invalid request format. Please try again.';
      } else if (response.status === 500) {
        errorMessage = 'Server error. The AI service might be starting up. Please try again in a moment.';
      } else if (response.status >= 500) {
        errorMessage = 'Service temporarily unavailable. Please try again later.';
      }
      
      throw new Error(errorMessage);
    }

    const data = await response.json();
    
    // Ensure the response has the expected structure
    return {
      status: data.status || 'ok',
      summary: data.summary || 'No response available',
      query: data.query || query,
      tools_used: data.tools_used || [],
      chain_used: data.chain_used || 'Unknown',
      timeline: data.timeline || [],
      error: data.error || null
    };
  } catch (error) {
    console.error('API Error:', error);
    
    let errorMessage = `Unable to connect to the AI service at ${API_BASE_URL}.`;
    
    if (error.name === 'AbortError') {
      errorMessage = 'Request timed out. The AI service might be busy. Please try again.';
    } else if (error.message.includes('Failed to fetch')) {
      errorMessage = 'Network error. Please check your connection and try again.';
    } else if (error.message) {
      errorMessage = error.message;
    }
    
    // Return a user-friendly error response
    return {
      status: 'error',
      summary: errorMessage,
      query: query,
      tools_used: [],
      chain_used: 'Error',
      timeline: [],
      error: error.message
    };
  }
};

export const healthCheck = async () => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      signal: controller.signal
    });

    clearTimeout(timeoutId);
    return response.ok;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};
