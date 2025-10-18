"""
LLM Configuration for AI Research Assistant
Configures Google Gemini models using LangChain
"""
import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseLanguageModel
from dotenv import load_dotenv

load_dotenv()

class LLMConfig:
    """Configuration class for LLM models"""
    
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    def get_gemini_flash_model(self, temperature: float = 0.2, max_tokens: int = 1000) -> BaseLanguageModel:
        """
        Get Gemini 2.5 Flash model instance
        
        Args:
            temperature: Controls randomness (0.0 = deterministic, 1.0 = maximum randomness)
            max_tokens: Maximum number of tokens in response
            
        Returns:
            Configured Gemini model instance
        """
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",  # Using Gemini 2.0 Flash Experimental model
            google_api_key=self.google_api_key,
            temperature=temperature,
            max_output_tokens=max_tokens,
            convert_system_message_to_human=True  # Required for Gemini
        )
    
    def get_gemini_pro_model(self, temperature: float = 0.3, max_tokens: int = 2000) -> BaseLanguageModel:
        """
        Get Gemini Pro model instance for more complex tasks
        
        Args:
            temperature: Controls randomness
            max_tokens: Maximum number of tokens in response
            
        Returns:
            Configured Gemini Pro model instance
        """
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",  # Using the same flash model for consistency
            google_api_key=self.google_api_key,
            temperature=temperature,
            max_output_tokens=max_tokens,
            convert_system_message_to_human=True
        )

# Global LLM configuration instance
llm_config = LLMConfig()
