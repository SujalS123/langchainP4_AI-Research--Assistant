"""
Test script to verify backend functionality
"""
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.langchain_service import run_agent, perform_web_search, call_gemini_api

async def test_gemini_api():
    """Test Gemini API connection"""
    print("Testing Gemini API connection...")
    try:
        response = await call_gemini_api("Hello, can you respond with 'API test successful'?")
        if "API test successful" in response or "successful" in response.lower():
            print("✅ Gemini API working correctly")
            return True
        else:
            print(f"⚠️  Gemini API responded but unexpected: {response[:100]}...")
            return True
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

async def test_search():
    """Test web search functionality"""
    print("\nTesting web search...")
    try:
        result = perform_web_search("Python programming")
        print("✅ Web search completed")
        print(f"Sample result: {result[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Web search failed: {e}")
        return False

async def test_agent():
    """Test full agent functionality"""
    print("\nTesting agent with simple query...")
    try:
        result = await run_agent("What is 2 + 2?")
        print("✅ Agent executed successfully")
        print(f"Agent response: {result.get('summary', 'No summary')}")
        return True
    except Exception as e:
        print(f"❌ Agent execution failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🔍 Backend Testing Suite")
    print("=" * 50)
    
    tests = [
        test_gemini_api(),
        test_search(),
        test_agent()
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    passed = sum(1 for result in results if result is True)
    total = len(tests)
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY environment variable is not set!")
        print("Please set it in your .env file before running tests.")
        sys.exit(1)
    
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
