import requests
import json

def test_cors():
    # Test CORS preflight request
    url = "https://langchainp4-ai-research-assistant.onrender.com/api/query"
    
    # Simulate preflight request
    headers = {
        'Origin': 'https://langchain-p4-ai-research-assistant.vercel.app',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type',
        'Accept': 'application/json'
    }
    
    print("Testing CORS preflight request...")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    
    try:
        response = requests.options(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Check for CORS headers
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Max-Age': response.headers.get('Access-Control-Max-Age')
        }
        
        print(f"CORS Headers: {cors_headers}")
        
        # Test actual POST request
        print("\nTesting actual POST request...")
        post_headers = {
            'Origin': 'https://langchain-p4-ai-research-assistant.vercel.app',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        post_data = {
            'query': 'test query',
            'options': {}
        }
        
        post_response = requests.post(url, headers=post_headers, json=post_data, timeout=10)
        print(f"POST Status Code: {post_response.status_code}")
        print(f"POST Response Headers: {dict(post_response.headers)}")
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_cors()
