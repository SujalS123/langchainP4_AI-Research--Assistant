"""
Test script to diagnose search functionality issues
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.langchain_service import langchain_service
import asyncio

async def test_search():
    """Test the search functionality with different queries"""
    print("=" * 60)
    print("SEARCH FUNCTIONALITY TEST")
    print("=" * 60)
    
    test_queries = [
        "latest tech news",
        "Python programming",
        "AI developments 2024",
        "simple test query"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}: '{query}' ---")
        
        # Test direct search function
        print("Testing direct search function...")
        try:
            search_result = langchain_service.perform_web_search(query)
            print(f"Search result length: {len(search_result)} characters")
            print(f"First 200 chars: {search_result[:200]}...")
            
            if "Search failed with HTTP status" in search_result:
                print("❌ SEARCH FAILED - HTTP Status Error")
                # Extract status code
                import re
                status_match = re.search(r'HTTP status (\d+)', search_result)
                if status_match:
                    status_code = status_match.group(1)
                    print(f"   Status Code: {status_code}")
                    if status_code == "202":
                        print("   ⚠️  Status 202 indicates async processing - this might be the issue")
            elif "Search error:" in search_result:
                print("❌ SEARCH FAILED - General Error")
                print(f"   Error: {search_result}")
            elif "no results could be extracted" in search_result:
                print("⚠️  SEARCH COMPLETED BUT NO RESULTS EXTRACTED")
            else:
                print("✅ SEARCH SUCCESSFUL")
                
        except Exception as e:
            print(f"❌ SEARCH EXCEPTION: {e}")
        
        # Test full query processing
        print("\nTesting full query processing...")
        try:
            result = await langchain_service.process_query_with_chains(query)
            print(f"Summary length: {len(result.get('summary', ''))} characters")
            print(f"Tools used: {result.get('tools_used', [])}")
            print(f"Chain used: {result.get('chain_used', 'Unknown')}")
            
            if result.get('error'):
                print(f"❌ PROCESSING ERROR: {result['error']}")
            elif "unable to provide you with the latest" in result.get('summary', '').lower():
                print("❌ FALLBACK RESPONSE - Search likely failed")
            else:
                print("✅ PROCESSING SUCCESSFUL")
                
        except Exception as e:
            print(f"❌ PROCESSING EXCEPTION: {e}")
        
        print("-" * 40)

def test_duckduckgo_direct():
    """Test DuckDuckGo directly"""
    print("\n" + "=" * 60)
    print("DIRECT DUCKDUCKGO TEST")
    print("=" * 60)
    
    try:
        import requests
        import urllib.parse
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        query = "latest tech news"
        encoded_query = urllib.parse.quote(query)
        url = f"https://duckduckgo.com/html/?q={encoded_query}"
        
        print(f"Testing URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Content Length: {len(response.text)}")
        
        if response.status_code == 200:
            # Check if we got HTML content
            if "<html" in response.text.lower():
                print("✅ Got HTML content")
                
                # Try to extract some results
                import re
                link_pattern = r'<a[^>]*class="result__a"[^>]*>(.*?)</a>'
                links = re.findall(link_pattern, response.text, re.DOTALL)
                print(f"Found {len(links)} result links")
                
                if links:
                    print("First few results:")
                    for i, link in enumerate(links[:3]):
                        clean_link = re.sub(r'<[^>]+>', '', link).strip()
                        print(f"  {i+1}. {clean_link}")
                else:
                    print("⚠️  No result links found - HTML structure might have changed")
            else:
                print("⚠️  Response doesn't contain HTML - might be blocked")
                print(f"First 500 chars: {response.text[:500]}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Direct test failed: {e}")

if __name__ == "__main__":
    print("Starting search functionality diagnostics...")
    
    # Test direct DuckDuckGo first
    test_duckduckgo_direct()
    
    # Test the application search
    asyncio.run(test_search())
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("If tests show issues, possible causes:")
    print("1. DuckDuckGo blocking/bot detection")
    print("2. Network connectivity issues")
    print("3. HTML structure changes in DuckDuckGo")
    print("4. Rate limiting")
    print("\nRecommendations:")
    print("1. Consider using a proper search API (Serper, Google Custom Search)")
    print("2. Add better error handling and fallbacks")
    print("3. Implement request retries")
    print("4. Add user-agent rotation")
