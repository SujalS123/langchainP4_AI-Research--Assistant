"""
Test Serper API directly without full app dependencies
"""
import requests
import json
import os

def test_serper_api():
    """Test Serper API directly"""
    print("=" * 60)
    print("SERPER API TEST")
    print("=" * 60)
    
    # Use the Serper API key from the environment
    serper_api_key = "6f3ec71c78475096daa7e0e5fa3592248a028181"
    
    if not serper_api_key:
        print("❌ No Serper API key found")
        return
    
    test_queries = [
        "latest tech news",
        "Python programming tutorial",
        "AI developments 2024"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}: '{query}' ---")
        
        try:
            url = "https://google.serper.dev/search"
            
            payload = json.dumps({
                "q": query,
                "num": 5
            })
            
            headers = {
                'X-API-KEY': serper_api_key,
                'Content-Type': 'application/json'
            }
            
            print(f"Making request to: {url}")
            print(f"Payload: {payload}")
            
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ SUCCESS - Got JSON response")
                
                # Extract and display results
                results = []
                
                if 'organic' in data:
                    print(f"Found {len(data['organic'])} organic results")
                    for j, item in enumerate(data['organic'][:3]):
                        title = item.get('title', '').strip()
                        snippet = item.get('snippet', '').strip()
                        link = item.get('link', '').strip()
                        
                        print(f"  Result {j+1}: {title}")
                        print(f"    Snippet: {snippet[:100]}...")
                        print(f"    Link: {link}")
                        
                        if title and snippet:
                            results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}")
                
                if 'knowledgeGraph' in data:
                    kg = data['knowledgeGraph']
                    kg_title = kg.get('title', '').strip()
                    kg_desc = kg.get('description', '').strip()
                    print(f"Knowledge Graph: {kg_title}")
                    print(f"Description: {kg_desc[:100]}...")
                    
                    if kg_title and kg_desc:
                        results.insert(0, f"Knowledge Graph: {kg_title}\n{kg_desc}")
                
                if results:
                    print(f"\n✅ Successfully extracted {len(results)} results")
                    print(f"First result: {results[0][:200]}...")
                else:
                    print("⚠️  No results could be extracted")
                    
            elif response.status_code == 401:
                print("❌ AUTHENTICATION FAILED - Check API key")
                print(f"Response: {response.text}")
            elif response.status_code == 429:
                print("❌ RATE LIMIT EXCEEDED - Try again later")
                print(f"Response: {response.text}")
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.Timeout:
            print("❌ REQUEST TIMEOUT")
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION ERROR")
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    print("Testing Serper API functionality...")
    test_serper_api()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("If Serper API works:")
    print("✅ The enhanced search service should fix the search issues")
    print("✅ Your AI Research Assistant will be able to provide real-time information")
    print("✅ The 'HTTP 202' errors should be resolved")
    print("\nIf Serper API fails:")
    print("❌ Check if the API key is valid")
    print("❌ Check if there are sufficient credits/quota")
    print("❌ Consider using a different search API")
