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
        Perform web search using enhanced search service with fallbacks.
        This method uses the new enhanced search service for better reliability.
        """
        try:
            from .enhanced_search_service import enhanced_search_service
            
            # Use the enhanced search service
            search_result = enhanced_search_service.perform_enhanced_search(query)
            
            if search_result["success"]:
                return search_result["results"]
            else:
                # If all providers failed, return a helpful error message
                return f"I am unable to provide you with the latest information because search services are currently unavailable. Error: {search_result.get('error', 'Unknown error')}. Please try again later."
                
        except Exception as e:
            return f"Search service temporarily unavailable: {str(e)}. Please try again later."
    
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
