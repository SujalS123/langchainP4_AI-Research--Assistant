"""
Minimal HTTP server using only standard library.
No FastAPI, no Pydantic, just pure Python.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import requests
import re

def perform_web_search(query: str) -> str:
    """
    Simple web search using DuckDuckGo HTML interface.
    This avoids the API issues by scraping the HTML results directly.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Encode the query properly
        encoded_query = urllib.parse.quote(query)
        url = f"https://duckduckgo.com/html/?q={encoded_query}"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Try different parsing approaches
            results = []
            
            # Method 1: Look for result links using regex
            link_pattern = r'<a[^>]*class="result__a"[^>]*>(.*?)</a>'
            links = re.findall(link_pattern, html_content, re.DOTALL)
            
            # Find snippets
            snippet_pattern = r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>'
            snippets = re.findall(snippet_pattern, html_content, re.DOTALL)
            
            # Combine links and snippets
            for i in range(min(len(links), len(snippets), 5)):
                title = re.sub(r'<[^>]+>', '', links[i]).strip()
                snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
                
                if title and len(title) > 5:  # Filter out empty/short titles
                    results.append(f"Title: {title}\nSnippet: {snippet}")
            
            # Method 2: If no results, try simpler approach
            if not results:
                # Look for any text between <a> tags that might be results
                simple_links = re.findall(r'<a[^>]*>([^<]{20,200})</a>', html_content)
                for i, link in enumerate(simple_links[:5]):
                    if 'http' not in link and 'duckduckgo' not in link.lower():
                        results.append(f"Title: {link.strip()}")
            
            if results:
                return "\n\n".join(results)
            else:
                return f"Search completed for '{query}' but no results could be extracted. The search engine interface may have changed."
        else:
            return f"Search failed with HTTP status {response.status_code}. Please try again."
            
    except Exception as e:
        return f"Search error: {str(e)}. The search service is temporarily unavailable."

class SimpleAPIHandler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_json_response({"message": "Simple AI Research Assistant API"})
        elif self.path == '/api/health':
            self.send_json_response({"status": "healthy"})
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/query':
            try:
                # Read the request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parse JSON
                request_data = json.loads(post_data.decode('utf-8'))
                query = request_data.get('query', '')
                
                if not query:
                    self.send_error(400, "Query is required")
                    return
                
                # Perform search
                search_results = perform_web_search(query)
                
                # Create response
                response = {
                    "status": "ok",
                    "summary": search_results,
                    "query": query,
                    "tools_available": ["Search", "Calculator"]
                }
                
                self.send_json_response(response)
                
            except Exception as e:
                self.send_error(500, f"Internal Server Error: {str(e)}")
        else:
            self.send_error(404, "Not Found")
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response_json = json.dumps(data, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to reduce log noise"""
        print(f"[{self.address_string()}] {format % args}")

def run_server():
    """Run the minimal server"""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    
    print("=" * 50)
    print("Simple AI Research Assistant Server")
    print("=" * 50)
    print("Server running at: http://localhost:8000")
    print("API endpoint: http://localhost:8000/api/query")
    print("Health check: http://localhost:8000/api/health")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
