const API_BASE_URL = 'http://localhost:8000';

export const sendQuery = async (query, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/query`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ query, options })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
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
    
    // Return a user-friendly error response
    return {
      status: 'error',
      summary: `Unable to connect to the AI service. Please ensure the backend server is running on ${API_BASE_URL}.`,
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
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });
    return response.ok;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};
