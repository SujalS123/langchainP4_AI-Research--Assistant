"""
Simple test script to verify the search functionality works.
This bypasses all the complex FastAPI/Pydantic issues.
"""
import requests
import urllib.parse
import json

def simple_search(query: str) -> str:
    """
    Simple web search using DuckDuckGo HTML interface.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Encode the query properly
        encoded_query = urllib.parse.quote(query)
        url = f"https://duckduckgo.com/html/?q={encoded_query}"
        
        print(f"Searching for: {query}")
        print(f"URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Look for search result patterns in the HTML
            results = []
            
            # Try different parsing approaches
            # Method 1: Look for result links
            import re
            
            # Find all links that look like search results
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
                    results.append(f"Result {i+1}: {title}\n{snippet}")
            
            # Method 2: If no results, try simpler approach
            if not results:
                # Look for any text between <a> tags that might be results
                simple_links = re.findall(r'<a[^>]*>([^<]{20,200})</a>', html_content)
                for i, link in enumerate(simple_links[:5]):
                    if 'http' not in link and 'duckduckgo' not in link.lower():
                        results.append(f"Result {i+1}: {link.strip()}")
            
            if results:
                return "\n\n".join(results)
            else:
                return f"Search completed for '{query}' but no results could be extracted."
        else:
            return f"Search failed with HTTP status {response.status_code}."
            
    except Exception as e:
        return f"Search error: {str(e)}"

def test_search():
    """Test the search function with the original query."""
    query = "What are the latest developments in AI for 2025?"
    
    print("=" * 50)
    print("TESTING SEARCH FUNCTIONALITY")
    print("=" * 50)
    
    result = simple_search(query)
    
    print("\nSEARCH RESULTS:")
    print("-" * 30)
    print(result)
    print("-" * 30)
    
    # Simulate the API response format
    api_response = {
        "status": "ok",
        "summary": result,
        "query": query,
        "tools_available": ["Search", "Calculator"]
    }
    
    print("\nSIMULATED API RESPONSE:")
    print("-" * 30)
    print(json.dumps(api_response, indent=2))

if __name__ == "__main__":
    test_search()
