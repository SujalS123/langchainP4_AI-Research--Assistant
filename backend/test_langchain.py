"""
Test script for LangChain implementation with Gemini 2.5 Flash
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from app.services.langchain_service import langchain_service

async def test_langchain_chains():
    """Test different LangChain chains"""
    
    print("🔗 Testing LangChain Chains with Gemini 2.5 Flash")
    print("=" * 60)
    
    # Test 1: Simple Q&A
    print("\n1. Testing Q&A Chain:")
    print("-" * 30)
    qa_result = await langchain_service.process_query_with_chains("What is artificial intelligence?")
    print(f"Chain used: {qa_result.get('chain_used', 'Unknown')}")
    print(f"Response: {qa_result['summary'][:200]}...")
    
    # Test 2: Math Chain
    print("\n2. Testing Math Chain:")
    print("-" * 30)
    math_result = await langchain_service.process_query_with_chains("Calculate 25 * 4 + 10")
    print(f"Chain used: {math_result.get('chain_used', 'Unknown')}")
    print(f"Response: {math_result['summary']}")
    
    # Test 3: Reasoning Chain
    print("\n3. Testing Reasoning Chain:")
    print("-" * 30)
    reasoning_result = await langchain_service.process_query_with_chains("Explain why machine learning is important for modern technology")
    print(f"Chain used: {reasoning_result.get('chain_used', 'Unknown')}")
    print(f"Response: {reasoning_result['summary'][:200]}...")
    
    # Test 4: Search Chain (if needed)
    print("\n4. Testing Search Chain:")
    print("-" * 30)
    search_result = await langchain_service.process_query_with_chains("What are the latest developments in quantum computing?")
    print(f"Chain used: {search_result.get('chain_used', 'Unknown')}")
    print(f"Tools used: {search_result.get('tools_used', [])}")
    print(f"Response: {search_result['summary'][:200]}...")
    
    # Test 5: Parallel Chains
    print("\n5. Testing Parallel Chains:")
    print("-" * 30)
    parallel_result = await langchain_service.run_parallel_chains("What are the benefits of renewable energy?")
    print(f"Chain used: {parallel_result.get('chain_used', 'Unknown')}")
    print(f"Response: {parallel_result['summary'][:300]}...")
    
    print("\n✅ All tests completed!")

async def test_direct_model():
    """Test direct model access"""
    print("\n🤖 Testing Direct Model Access:")
    print("-" * 40)
    
    from app.services.llm_config import llm_config
    
    try:
        model = llm_config.get_gemini_flash_model()
        response = await model.ainvoke("Hello! Can you tell me about LangChain?")
        print(f"Model response: {response.content}")
        print("✅ Direct model access successful!")
    except Exception as e:
        print(f"❌ Error testing direct model: {str(e)}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY environment variable is not set!")
        print("Please set it in your .env file and try again.")
    else:
        asyncio.run(test_langchain_chains())
        asyncio.run(test_direct_model())
