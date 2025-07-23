"""
Answer Agent - Summarizes search results into concise answers
Uses Google Gemini 2.5 Flash Lite wrapped in LangChain for response generation
"""

import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser


class AnswerParser(BaseOutputParser):
    """Custom parser to format the final answer response"""
    
    def parse(self, text: str) -> str:
        # Clean up the response and ensure it's well-formatted
        return text.strip()


class AnswerAgent:
    """
    Agent that synthesizes search results into comprehensive, concise answers
    """
    
    def __init__(self):
        # Initialize Gemini LLM with LangChain wrapper
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",  # Using Gemini 2.5 Flash Lite equivalent
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7  # Slightly higher temperature for more natural responses
        )
        
        # Define prompt template for answer generation
        self.prompt_template = PromptTemplate(
            input_variables=["search_results", "original_question"],
            template="""
You are an expert information synthesizer. Based on the search results provided, create a comprehensive yet concise answer to the user's question.

Guidelines:
1. Synthesize information from multiple sources when possible
2. Keep the answer focused and relevant to the original question
3. Include specific details, dates, and facts when available
4. If information is conflicting or unclear, mention this
5. Keep the response conversational but informative
6. Aim for 2-4 sentences unless more detail is clearly needed

Original Question: {original_question}

Search Results:
{search_results}

Answer:"""
        )
        
        # Create the chain with output parser
        self.parser = AnswerParser()
        self.chain = self.prompt_template | self.llm | self.parser
    
    def __call__(self, input_data: str, original_question: str = "") -> Dict[str, Any]:
        """
        Process search results and return a synthesized answer
        
        Args:
            input_data: Formatted search results text
            original_question: The original user question (optional)
            
        Returns:
            Dict with content key containing the final answer
        """
        try:
            # Generate answer using the chain
            answer = self.chain.invoke({
                "search_results": input_data,
                "original_question": original_question or "Please provide a summary of the information."
            })
            
            return {
                "content": answer
            }
            
        except Exception as e:
            return {
                "content": f"Error generating answer: {str(e)}"
            }
    
    def process(self, search_results: str, question: str = "") -> str:
        """
        Alternative method for direct processing
        
        Args:
            search_results: Formatted search results
            question: Original user question
            
        Returns:
            Generated answer string
        """
        result = self.__call__(search_results, question)
        return result["content"]
    
    def summarize_results(self, results_list: list, question: str = "") -> Dict[str, Any]:
        """
        Method to handle structured results list
        
        Args:
            results_list: List of result dictionaries
            question: Original user question
            
        Returns:
            Dict with synthesized answer
        """
        # Convert structured results to text format
        formatted_results = ""
        for i, result in enumerate(results_list, 1):
            formatted_results += f"{i}. {result.get('title', 'No title')}\n"
            formatted_results += f"   {result.get('snippet', 'No description')}\n\n"
        
        return self.__call__(formatted_results, question)