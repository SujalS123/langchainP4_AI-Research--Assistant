"""
LangChain Chains for AI Research Assistant
Implements various chains for different types of queries and tasks
"""
from typing import Dict, List, Any, Optional
# LLMChain is deprecated in newer versions, using the new LCEL approach
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, Runnable
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .llm_config import llm_config

class ResearchChains:
    """Collection of LangChain chains for research tasks"""
    
    def __init__(self):
        self.llm = llm_config.get_gemini_flash_model()
        self.pro_llm = llm_config.get_gemini_pro_model()
        self._setup_chains()
    
    def _setup_chains(self):
        """Initialize all chain templates"""
        
        # Simple Q&A Chain
        self.qa_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI research assistant. Provide accurate, informative, and well-structured responses to user questions."),
            ("human", "{question}")
        ])
        
        # Research with context Chain
        self.research_template = ChatPromptTemplate.from_messages([
            ("system", """You are a research assistant. Using the provided search results and context, 
            answer the user's question comprehensively. If the search results don't contain enough information, 
            acknowledge this and provide the best possible answer based on the available data."""),
            ("human", """Search Results:
{search_context}

User Question: {question}

Please provide a comprehensive answer based on the search results above.""")
        ])
        
        # Math calculation Chain
        self.math_template = ChatPromptTemplate.from_messages([
            ("system", "You are a mathematical assistant. Solve the given math problem and show your work."),
            ("human", "Solve this math problem: {math_expression}")
        ])
        
        # Summary Chain
        self.summary_template = ChatPromptTemplate.from_messages([
            ("system", "You are a research assistant. Create a concise and informative summary of the provided content."),
            ("human", "Content to summarize: {content}\n\nProvide a clear and concise summary:")
        ])
        
        # Multi-step reasoning Chain
        self.reasoning_template = ChatPromptTemplate.from_messages([
            ("system", """You are an analytical research assistant. Break down complex questions into steps 
            and provide detailed reasoning for your conclusions."""),
            ("human", """Question: {question}
            
            Please analyze this step by step:
            1. Identify the key components of the question
            2. Break down the problem into smaller parts
            3. Address each part systematically
            4. Provide a comprehensive conclusion""")
        ])
    
    def get_qa_chain(self) -> Runnable:
        """Get simple Q&A chain"""
        return self.qa_template | self.llm | StrOutputParser()
    
    def get_research_chain(self) -> Runnable:
        """Get research chain with search context"""
        return self.research_template | self.pro_llm | StrOutputParser()
    
    def get_math_chain(self) -> Runnable:
        """Get math calculation chain"""
        return self.math_template | self.llm | StrOutputParser()
    
    def get_summary_chain(self) -> Runnable:
        """Get content summarization chain"""
        return self.summary_template | self.llm | StrOutputParser()
    
    def get_reasoning_chain(self) -> Runnable:
        """Get multi-step reasoning chain"""
        return self.reasoning_template | self.pro_llm | StrOutputParser()
    
    def get_parallel_chain(self, chains: Dict[str, Any]) -> RunnableParallel:
        """
        Create a parallel chain that runs multiple chains simultaneously
        
        Args:
            chains: Dictionary of chain names to chain instances
            
        Returns:
            RunnableParallel instance
        """
        return RunnableParallel(**chains)
    
    def get_sequential_chain(self, chains: List[Runnable]) -> Runnable:
        """
        Create a sequential chain that runs chains one after another
        
        Args:
            chains: List of chains to run in sequence
            
        Returns:
            Sequential chain instance
        """
        # For LangChain v0.1, we can chain them using the pipe operator
        sequential_chain = chains[0]
        for chain in chains[1:]:
            sequential_chain = sequential_chain | chain
        return sequential_chain

class ToolChains:
    """Chains specifically for tool-based operations"""
    
    def __init__(self):
        self.llm = llm_config.get_gemini_flash_model()
        self._setup_tool_chains()
    
    def _setup_tool_chains(self):
        """Setup tool-specific chain templates"""
        
        # Tool selection chain
        self.tool_selection_template = ChatPromptTemplate.from_messages([
            ("system", """You are a tool selection assistant. Based on the user's query, determine which tools are needed.
            Available tools: [search, calculator, scraper]
            Respond with a JSON object containing the tools needed."""),
            ("human", "Query: {query}\n\nWhich tools are needed for this query?")
        ])
        
        # Search result processing chain
        self.search_processing_template = ChatPromptTemplate.from_messages([
            ("system", "You are a search result processor. Extract and organize relevant information from search results."),
            ("human", """Search Results:
{search_results}

User Query: {query}

Please extract and organize the most relevant information:""")
        ])
    
    def get_tool_selection_chain(self) -> Runnable:
        """Get tool selection chain"""
        return self.tool_selection_template | self.llm | StrOutputParser()
    
    def get_search_processing_chain(self) -> Runnable:
        """Get search result processing chain"""
        return self.search_processing_template | self.llm | StrOutputParser()

# Global chain instances
research_chains = ResearchChains()
tool_chains = ToolChains()
