"""
LangChain-based AI service for AI Research Assistant.
Uses LangChain chains with Google Gemini models for enhanced functionality.
"""
import os
import asyncio
import json
import re
from typing import Dict, List, Any, Optional
from app.config import settings
from .chains import research_chains, tool_chains
from .llm_config import llm_config
import requests

class LangChainService:
    """Main service class using LangChain chains"""
    
    def __init__(self):
        self.research_chains = research_chains
        self.tool_chains = tool_chains
        self.llm = llm_config.get_gemini_flash_model()
    
    def perform_web_search(self, query: str) -> str:
        """
        Perform web search using DuckDuckGo HTML interface.
        This method is kept for compatibility with existing tools.
        """
        try:
            import urllib.parse
            
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
                for i in range(min(len(links), len(snippets), settings.MAX_SEARCH_RESULTS)):
                    title = re.sub(r'<[^>]+>', '', links[i]).strip()
                    snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
                    
                    if title and len(title) > 5:  # Filter out empty/short titles
                        results.append(f"Title: {title}\nSnippet: {snippet}")
                
                # Method 2: If no results, try simpler approach
                if not results:
                    # Look for any text between <a> tags that might be results
                    simple_links = re.findall(r'<a[^>]*>([^<]{20,200})</a>', html_content)
                    for i, link in enumerate(simple_links[:settings.MAX_SEARCH_RESULTS]):
                        if 'http' not in link and 'duckduckgo' not in link.lower():
                            results.append(f"Title: {link.strip()}")
                
                if results:
                    return "\n\n".join(results)
                else:
                    return f"Search completed for '{query}' but no results could be extracted."
            else:
                return f"Search failed with HTTP status {response.status_code}."
                
        except Exception as e:
            return f"Search error: {str(e)}. The search service is temporarily unavailable."
    
    def calculate_math(self, expression: str) -> str:
        """Simple math calculation using LangChain math chain"""
        try:
            # Use the math chain for calculation
            math_chain = self.research_chains.get_math_chain()
            result = asyncio.run(math_chain.ainvoke({"math_expression": expression}))
            return result
        except Exception as e:
            # Fallback to simple eval if chain fails
            try:
                eval_result = eval(expression)
                return f"The result of {expression} is {eval_result}"
            except:
                return f"Error calculating {expression}: {str(e)}"
    
    async def process_query_with_chains(self, query: str, options: dict = None) -> Dict[str, Any]:
        """
        Process query using appropriate LangChain chains
        
        Args:
            query: User's research question
            options: Optional configuration parameters
            
        Returns:
            dict: Response containing summary and execution timeline
        """
        if options is None:
            options = {}
        
        try:
            # Determine query type and select appropriate chain
            query_lower = query.lower()
            tools_used = []
            context = ""
            
            # Check if search is needed
            needs_search = any(keyword in query_lower for keyword in [
                'search', 'find', 'latest', 'current', 'news', 'what is', 'who is', 
                'when was', 'recent', 'today', 'update'
            ])
            
            # Check if math calculation is needed
            needs_math = any(char in query for char in ['+', '-', '*', '/', '=', 'calculate', 'math']) or \
                        any(keyword in query_lower for keyword in ['calculate', 'solve', 'compute'])
            
            # Check if complex reasoning is needed
            needs_reasoning = any(keyword in query_lower for keyword in [
                'analyze', 'compare', 'explain', 'why', 'how', 'step by step', 'break down'
            ])
            
            # Use tools if needed
            if needs_search:
                search_result = self.perform_web_search(query)
                context += f"Search Results:\n{search_result}\n\n"
                tools_used.append("Search")
            
            if needs_math:
                # Extract math expression
                math_match = re.search(r'([\d+\-*/().\s]+)', query)
                if math_match:
                    math_result = self.calculate_math(math_match.group(1))
                    context += f"Math Calculation:\n{math_result}\n\n"
                    tools_used.append("Calculator")
            
            # Select and execute appropriate chain
            if context and needs_search:
                # Use research chain with search context
                chain = self.research_chains.get_research_chain()
                response = await chain.ainvoke({
                    "search_context": context.strip(),
                    "question": query
                })
            elif needs_reasoning:
                # Use reasoning chain for complex queries
                chain = self.research_chains.get_reasoning_chain()
                response = await chain.ainvoke({"question": query})
            elif needs_math and not needs_search:
                # Use math chain for pure math queries
                chain = self.research_chains.get_math_chain()
                math_expr = re.search(r'([\d+\-*/().\s]+)', query)
                response = await chain.ainvoke({
                    "math_expression": math_expr.group(1) if math_expr else query
                })
            else:
                # Use simple Q&A chain
                chain = self.research_chains.get_qa_chain()
                response = await chain.ainvoke({"question": query})
            
            return {
                "summary": response,
                "query": query,
                "tools_available": ["Search", "Calculator", "Reasoning"],
                "tools_used": tools_used,
                "chain_used": self._get_chain_name(needs_search, needs_math, needs_reasoning)
            }
            
        except Exception as e:
            return {
                "summary": f"Error processing query with LangChain: {str(e)}",
                "query": query,
                "error": str(e),
                "tools_available": ["Search", "Calculator", "Reasoning"],
                "tools_used": []
            }
    
    def _get_chain_name(self, needs_search: bool, needs_math: bool, needs_reasoning: bool) -> str:
        """Determine which chain was used based on query analysis"""
        if needs_search:
            return "Research Chain (with context)"
        elif needs_reasoning:
            return "Reasoning Chain"
        elif needs_math:
            return "Math Chain"
        else:
            return "Q&A Chain"
    
    async def run_parallel_chains(self, query: str) -> Dict[str, Any]:
        """
        Run multiple chains in parallel for comprehensive analysis
        
        Args:
            query: User's research question
            
        Returns:
            dict: Combined results from multiple chains
        """
        try:
            # Create parallel chains
            parallel_chain = self.research_chains.get_parallel_chain({
                "qa_result": self.research_chains.get_qa_chain(),
                "reasoning_result": self.research_chains.get_reasoning_chain()
            })
            
            # Execute parallel chains
            results = await parallel_chain.ainvoke({"question": query})
            
            # Combine results
            combined_summary = f"""Direct Answer:
{results['qa_result']}

Detailed Analysis:
{results['reasoning_result']}"""
            
            return {
                "summary": combined_summary,
                "query": query,
                "chain_used": "Parallel Chains (Q&A + Reasoning)",
                "tools_available": ["Search", "Calculator", "Reasoning"],
                "tools_used": []
            }
            
        except Exception as e:
            return {
                "summary": f"Error in parallel chain execution: {str(e)}",
                "query": query,
                "error": str(e),
                "tools_available": ["Search", "Calculator", "Reasoning"],
                "tools_used": []
            }

# Global service instance
langchain_service = LangChainService()

# Backward compatibility functions
async def run_agent(query: str, options: dict = None):
    """
    Legacy function for backward compatibility.
    Uses the new LangChain service.
    """
    return await langchain_service.process_query_with_chains(query, options)

def perform_web_search(query: str) -> str:
    """Legacy function for backward compatibility"""
    return langchain_service.perform_web_search(query)

def calculate_math(expression: str) -> str:
    """Legacy function for backward compatibility"""
    return langchain_service.calculate_math(expression)
