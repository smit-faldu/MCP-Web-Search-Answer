"""
Query Agent - Converts user questions into structured Google search queries
Uses Google Gemini 2.5 Flash Lite wrapped in LangChain for prompt templating
"""

import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser


class SearchQueryParser(BaseOutputParser):
    """Custom parser to extract clean search query from LLM response"""
    
    def parse(self, text: str) -> str:
        # Remove any extra formatting and return clean query
        return text.strip().replace('"', '').replace('\n', ' ')


class QueryAgent:
    """
    Agent that transforms user questions into optimized Google search queries
    """
    
    def __init__(self):
        # Initialize Gemini LLM with LangChain wrapper
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",  # Using Gemini 2.5 Flash Lite equivalent
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.3  # Lower temperature for more focused queries
        )
        
        # Define prompt template for query generation
        self.prompt_template = PromptTemplate(
            input_variables=["user_question"],
            template="""
You are a search query optimizer. Convert the user's question into an effective Google search query.

Rules:
1. Keep it concise (3-6 keywords)
2. Use specific terms that will find recent, relevant results
3. Include time-related keywords if the question implies recency (like "recent", "latest", "new")
4. Remove unnecessary words like "what", "how", "tell me about"
5. Focus on the core topic and context

User Question: {user_question}

Search Query:"""
        )
        
        # Create the chain with output parser
        self.parser = SearchQueryParser()
        self.chain = self.prompt_template | self.llm | self.parser
    
    def __call__(self, input_data: str) -> Dict[str, Any]:
        """
        Process user question and return optimized search query
        
        Args:
            input_data: User's natural language question
            
        Returns:
            Dict with content key containing the search query
        """
        try:
            # Generate search query using the chain
            search_query = self.chain.invoke({"user_question": input_data})
            
            return {
                "content": search_query
            }
            
        except Exception as e:
            return {
                "content": f"Error generating search query: {str(e)}"
            }
    
    def process(self, input_text: str) -> str:
        """
        Alternative method for direct processing
        """
        result = self.__call__(input_text)
        return result["content"]