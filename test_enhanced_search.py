"""
Test the enhanced search service
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Set environment variables for testing
os.environ.setdefault('SERPER_API_KEY', '6f3ec71c78475096daa7e0e5fa3592248a028181')

from backend.app.services.enhanced_search_service import enhanced_search_service

def test_enhanced_search():
    """Test the enhanced search service"""
    print("=" * 60)
    print("ENHANCED SEARCH SERVICE TEST")
    print("=" * 60)
    
    test_queries = [
        "latest tech news",
        "Python programming tutorial",
        "AI developments 2024"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}: '{query}' ---")
        
        try:
            result = enhanced_search_service.perform_enhanced_search(query)
            
            print(f"Success: {result['success']}")
            print(f"Provider Used: {result['provider_used']}")
            print(f"Providers Attempted: {', '.join(result['providers_attempted'])}")
            
            if result['success']:
                print(f"Results length: {len(result['results'])} characters")
                print(f"First 300 chars: {result['results'][:300]}...")
                print("✅ SEARCH SUCCESSFUL")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
                print(f"Results: {result['results'][:200]}...")
                print("❌ SEARCH FAILED")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
        
        print("-" * 40)

def test_individual_providers():
    """Test individual search providers"""
    print("\n" + "=" * 60)
    print("INDIVIDUAL PROVIDER TESTS")
    print("=" * 60)
    
    query = "latest tech news"
    
    # Test Serper
    print(f"\n--- Testing Serper API ---")
    try:
        result = enhanced_search_service.search_with_serper(query)
        print(f"Result length: {len(result)} characters")
        if "error" not in result.lower() and "failed" not in result.lower():
            print("✅ SERPER SUCCESS")
            print(f"First 200 chars: {result[:200]}...")
        else:
            print("❌ SERPER FAILED")
            print(f"Result: {result[:200]}...")
    except Exception as e:
        print(f"❌ SERPER EXCEPTION: {e}")
    
    # Test DuckDuckGo
    print(f"\n--- Testing DuckDuckGo Fallback ---")
    try:
        result = enhanced_search_service.search_with_duckduckgo_fallback(query)
        print(f"Result length: {len(result)} characters")
        if "error" not in result.lower() and "failed" not in result.lower() and "unavailable" not in result.lower():
            print("✅ DUCKDUCKGO SUCCESS")
            print(f"First 200 chars: {result[:200]}...")
        else:
            print("❌ DUCKDUCKGO FAILED")
            print(f"Result: {result[:200]}...")
    except Exception as e:
        print(f"❌ DUCKDUCKGO EXCEPTION: {e}")
    
    # Test Wikipedia
    print(f"\n--- Testing Wikipedia Fallback ---")
    try:
        result = enhanced_search_service.search_with_wikipedia_fallback(query)
        print(f"Result length: {len(result)} characters")
        if "error" not in result.lower() and "failed" not in result.lower():
            print("✅ WIKIPEDIA SUCCESS")
            print(f"First 200 chars: {result[:200]}...")
        else:
            print("❌ WIKIPEDIA FAILED")
            print(f"Result: {result[:200]}...")
    except Exception as e:
        print(f"❌ WIKIPEDIA EXCEPTION: {e}")

if __name__ == "__main__":
    print("Testing enhanced search service...")
    
    # Test individual providers first
    test_individual_providers()
    
    # Test the enhanced search service
    test_enhanced_search()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\nIf Serper API works, the search functionality should now be fixed.")
    print("The enhanced service will automatically fall back to DuckDuckGo and Wikipedia")
    print("if Serper fails, providing better reliability than the original implementation.")
