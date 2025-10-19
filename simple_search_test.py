"""
Simple test to diagnose DuckDuckGo search issues
"""
import requests
import urllib.parse
import re
import time

def test_duckduckgo_search():
    """Test DuckDuckGo search directly"""
    print("=" * 60)
    print("DUCKDUCKGO SEARCH TEST")
    print("=" * 60)
    
    # Test with different user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    test_queries = [
        "latest tech news",
        "Python programming tutorial",
        "AI developments 2024"
    ]
    
    for i, user_agent in enumerate(user_agents, 1):
        print(f"\n--- Test {i}: User Agent {i} ---")
        print(f"User-Agent: {user_agent}")
        
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        for j, query in enumerate(test_queries, 1):
            print(f"\n  Query {j}: '{query}'")
            
            try:
                encoded_query = urllib.parse.quote(query)
                url = f"https://duckduckgo.com/html/?q={encoded_query}"
                
                print(f"  URL: {url}")
                
                response = requests.get(url, headers=headers, timeout=15)
                
                print(f"  Status Code: {response.status_code}")
                print(f"  Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
                print(f"  Content Length: {len(response.text)}")
                
                if response.status_code == 200:
                    # Check if we got HTML content
                    if "<html" in response.text.lower():
                        print("  ✅ Got HTML content")
                        
                        # Try to extract results using multiple methods
                        results_found = 0
                        
                        # Method 1: Original pattern
                        link_pattern = r'<a[^>]*class="result__a"[^>]*>(.*?)</a>'
                        links = re.findall(link_pattern, response.text, re.DOTALL)
                        if links:
                            print(f"  ✅ Method 1: Found {len(links)} result links")
                            results_found = len(links)
                        
                        # Method 2: Alternative pattern
                        if not links:
                            alt_pattern = r'<a[^>]*href="([^"]*)"[^>]*class="[^"]*result[^"]*"[^>]*>(.*?)</a>'
                            alt_links = re.findall(alt_pattern, response.text, re.DOTALL)
                            if alt_links:
                                print(f"  ✅ Method 2: Found {len(alt_links)} result links")
                                results_found = len(alt_links)
                        
                        # Method 3: Generic result pattern
                        if not links:
                            generic_pattern = r'<a[^>]*>([^<]{20,200})</a>'
                            generic_links = re.findall(generic_pattern, response.text)
                            # Filter out navigation links
                            filtered_links = [link for link in generic_links if 'http' not in link and len(link.strip()) > 20]
                            if filtered_links:
                                print(f"  ✅ Method 3: Found {len(filtered_links)} potential result links")
                                results_found = len(filtered_links)
                        
                        if results_found > 0:
                            print(f"  ✅ SUCCESS: Found {results_found} results")
                            # Show first few results
                            if links:
                                for k, link in enumerate(links[:2]):
                                    clean_link = re.sub(r'<[^>]+>', '', link).strip()
                                    print(f"    Result {k+1}: {clean_link}")
                        else:
                            print("  ❌ NO RESULTS: Could not extract any results")
                            print(f"  First 500 chars of HTML: {response.text[:500]}")
                    else:
                        print("  ❌ NO HTML: Response doesn't contain HTML")
                        print(f"  Response: {response.text[:200]}")
                else:
                    print(f"  ❌ HTTP ERROR: {response.status_code}")
                    if response.status_code == 202:
                        print("  ⚠️  Status 202: Request accepted for async processing")
                    print(f"  Response: {response.text[:200]}")
                
            except requests.exceptions.Timeout:
                print("  ❌ TIMEOUT: Request timed out")
            except requests.exceptions.ConnectionError:
                print("  ❌ CONNECTION ERROR: Could not connect")
            except Exception as e:
                print(f"  ❌ EXCEPTION: {e}")
            
            # Add delay between requests
            time.sleep(2)
        
        print("-" * 40)

def test_alternative_search_methods():
    """Test alternative search methods"""
    print("\n" + "=" * 60)
    print("ALTERNATIVE SEARCH METHODS TEST")
    print("=" * 60)
    
    # Test 1: DuckDuckGo instant answer API
    print("\n--- DuckDuckGo Instant Answer API ---")
    try:
        query = "latest tech news"
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&pretty=1"
        
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Got JSON response")
            print(f"AbstractText length: {len(data.get('AbstractText', ''))}")
            print(f"RelatedTopics count: {len(data.get('RelatedTopics', []))}")
            
            if data.get('AbstractText'):
                print(f"Abstract: {data['AbstractText'][:200]}...")
            else:
                print("No abstract text found")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: Wikipedia API
    print("\n--- Wikipedia API Test ---")
    try:
        query = "Artificial intelligence"
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Got Wikipedia summary")
            print(f"Title: {data.get('title', 'Unknown')}")
            print(f"Extract length: {len(data.get('extract', ''))}")
            print(f"Extract: {data.get('extract', '')[:200]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("Starting search diagnostics...")
    
    # Test DuckDuckGo HTML search
    test_duckduckgo_search()
    
    # Test alternative methods
    test_alternative_search_methods()
    
    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)
    print("\nIf DuckDuckGo HTML scraping fails:")
    print("1. DuckDuckGo might be blocking automated requests")
    print("2. HTML structure might have changed")
    print("3. Rate limiting might be active")
    print("\nRecommendations:")
    print("1. Use DuckDuckGo Instant Answer API (JSON)")
    print("2. Use Serper API for reliable search results")
    print("3. Implement retry logic with exponential backoff")
    print("4. Add proxy rotation if needed")
