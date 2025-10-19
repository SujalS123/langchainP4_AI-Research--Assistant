"""
Enhanced search service with multiple fallback options
Uses Serper API as primary, with DuckDuckGo and other methods as fallbacks
"""
import os
import requests
import urllib.parse
import re
import json
import time
from typing import Dict, List, Any, Optional
from app.config import settings

class EnhancedSearchService:
    """Enhanced search service with multiple providers and fallbacks"""
    
    def __init__(self):
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.timeout = 10
        self.max_results = settings.MAX_SEARCH_RESULTS
    
    def search_with_serper(self, query: str) -> str:
        """
        Primary search using Serper API (Google Search results)
        """
        if not self.serper_api_key:
            return "Serper API key not configured. Please set SERPER_API_KEY environment variable."
        
        try:
            url = "https://google.serper.dev/search"
            
            payload = json.dumps({
                "q": query,
                "num": self.max_results
            })
            
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, data=payload, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                results = []
                
                # Extract organic results
                if 'organic' in data:
                    for item in data['organic'][:self.max_results]:
                        title = item.get('title', '').strip()
                        snippet = item.get('snippet', '').strip()
                        link = item.get('link', '').strip()
                        
                        if title and snippet:
                            results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}")
                
                # Extract knowledge graph if available
                if 'knowledgeGraph' in data:
                    kg = data['knowledgeGraph']
                    kg_title = kg.get('title', '').strip()
                    kg_desc = kg.get('description', '').strip()
                    
                    if kg_title and kg_desc:
                        results.insert(0, f"Knowledge Graph: {kg_title}\n{kg_desc}")
                
                if results:
                    return "\n\n".join(results)
                else:
                    return f"No results found for '{query}' using Serper API."
            
            elif response.status_code == 401:
                return "Serper API authentication failed. Please check your API key."
            elif response.status_code == 429:
                return "Serper API rate limit exceeded. Please try again later."
            else:
                return f"Serper API error: HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "Serper API request timed out."
        except Exception as e:
            return f"Serper API error: {str(e)}"
    
    def search_with_duckduckgo_fallback(self, query: str) -> str:
        """
        Fallback search using DuckDuckGo with improved handling
        """
        try:
            # Try multiple DuckDuckGo endpoints
            endpoints = [
                "https://duckduckgo.com/html/",
                "https://html.duckduckgo.com/html/",
                "https://duckduckgo.com/lite/"
            ]
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            
            for endpoint in endpoints:
                try:
                    params = {"q": query}
                    response = requests.get(endpoint, params=params, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        return self._parse_duckduckgo_results(response.text, query)
                    elif response.status_code == 202:
                        # Skip this endpoint and try next
                        continue
                    
                except Exception:
                    continue
            
            return "DuckDuckGo search unavailable. All endpoints failed or returned processing status."
            
        except Exception as e:
            return f"DuckDuckGo fallback error: {str(e)}"
    
    def _parse_duckduckgo_results(self, html_content: str, query: str) -> str:
        """Parse DuckDuckGo HTML results with multiple patterns"""
        results = []
        
        # Multiple parsing patterns
        patterns = [
            r'<a[^>]*class="result__a"[^>]*>(.*?)</a>.*?<a[^>]*class="result__snippet"[^>]*>(.*?)</a>',
            r'<a[^>]*href="([^"]*)"[^>]*class="[^"]*result[^"]*"[^>]*>(.*?)</a>.*?(?:<div[^>]*class="[^"]*snippet[^"]*"[^>]*>(.*?)</div>)?',
            r'<h2[^>]*><a[^>]*>(.*?)</a></h2>.*?(?:<div[^>]*>(.*?)</div>)?'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                if len(match) >= 2:
                    title = re.sub(r'<[^>]+>', '', match[0]).strip()
                    snippet = re.sub(r'<[^>]+>', '', match[1]).strip() if len(match) > 1 else ""
                    
                    if title and len(title) > 5 and title.lower() != 'web':
                        result_text = f"Title: {title}"
                        if snippet and len(snippet) > 10:
                            result_text += f"\nSnippet: {snippet}"
                        results.append(result_text)
                        
                        if len(results) >= self.max_results:
                            break
            
            if results:
                break
        
        if results:
            return "\n\n".join(results)
        else:
            return f"DuckDuckGo search completed for '{query}' but no results could be extracted."
    
    def search_with_wikipedia_fallback(self, query: str) -> str:
        """
        Fallback search using Wikipedia API
        """
        try:
            # Search for Wikipedia pages
            search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
            
            response = requests.get(search_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', '').strip()
                extract = data.get('extract', '').strip()
                
                if title and extract:
                    return f"Wikipedia: {title}\n{extract}"
                else:
                    return f"No Wikipedia article found for '{query}'."
            else:
                return f"Wikipedia API error: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Wikipedia fallback error: {str(e)}"
    
    def perform_enhanced_search(self, query: str) -> Dict[str, Any]:
        """
        Perform search with multiple fallbacks and comprehensive error handling
        """
        search_results = {
            "query": query,
            "results": "",
            "provider_used": "",
            "success": False,
            "error": None,
            "providers_attempted": []
        }
        
        # Provider priority: Serper -> DuckDuckGo -> Wikipedia
        providers = [
            ("Serper API", self.search_with_serper),
            ("DuckDuckGo", self.search_with_duckduckgo_fallback),
            ("Wikipedia", self.search_with_wikipedia_fallback)
        ]
        
        for provider_name, search_func in providers:
            search_results["providers_attempted"].append(provider_name)
            
            try:
                result = search_func(query)
                
                # Check if result is successful
                if (not any(error_phrase in result.lower() for error_phrase in [
                    "error", "failed", "timeout", "unavailable", "not configured", 
                    "authentication failed", "rate limit", "no results found"
                ]) and len(result) > 50):
                    
                    search_results["results"] = result
                    search_results["provider_used"] = provider_name
                    search_results["success"] = True
                    break
                else:
                    # Log the failure but continue to next provider
                    print(f"Search provider {provider_name} failed: {result[:100]}...")
                    
            except Exception as e:
                print(f"Search provider {provider_name} exception: {e}")
                continue
        
        if not search_results["success"]:
            search_results["error"] = f"All search providers failed. Attempted: {', '.join(search_results['providers_attempted'])}"
            search_results["results"] = f"I am unable to provide you with the latest information because all search services are currently unavailable. The error indicates that search request processing could not be completed.\n\nTo get the latest information, I recommend checking reputable sources directly or trying again later."
        
        return search_results

# Global service instance
enhanced_search_service = EnhancedSearchService()

def perform_web_search(query: str) -> str:
    """
    Enhanced web search function with fallbacks
    """
    result = enhanced_search_service.perform_enhanced_search(query)
    
    if result["success"]:
        return result["results"]
    else:
        return result["results"]  # This contains the error message
