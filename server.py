"""
FastMCP Server - Main application entry point
Orchestrates the web search and answer workflow using MCP framework
"""

import os
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import MCP components
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("⚠️  FastMCP not available, using alternative implementation")
    FastMCP = None

# Import our agents and tools
from agents.query_agent import QueryAgent
from agents.answer_agent import AnswerAgent
from tools.search_tool import SearchTool
from langflow.graph import WebSearchWorkflow


class MCPWebSearchServer:
    """
    Main server class that handles web search and answer generation
    """
    
    def __init__(self):
        # Validate environment variables
        self._validate_environment()
        
        # Initialize components
        self.query_agent = QueryAgent()
        self.search_tool = SearchTool()
        self.answer_agent = AnswerAgent()
        self.workflow = WebSearchWorkflow()
        
        print("✅ MCP Web Search Server initialized successfully")
    
    def _validate_environment(self):
        """Validate that required environment variables are set"""
        required_vars = ["GEMINI_API_KEY", "SERPAPI_KEY"]
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var) or os.getenv(var) == f"your_{var.lower()}":
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            print("Please update your .env file with valid API keys")
            raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    def process_question(self, user_question: str) -> Dict[str, Any]:
        """
        Process a user question through the complete workflow
        
        Args:
            user_question: The user's natural language question
            
        Returns:
            Dict with the final answer and metadata
        """
        print(f"\n📝 Processing question: {user_question}")
        
        # Use LangGraph workflow for orchestration
        result = self.workflow.run(user_question)
        
        return result
    
    def process_step_by_step(self, user_question: str) -> Dict[str, Any]:
        """
        Alternative method that processes each step individually
        Useful for debugging or when LangGraph is not available
        
        Args:
            user_question: The user's natural language question
            
        Returns:
            Dict with the final answer and step-by-step results
        """
        print(f"\n🔧 Processing step-by-step: {user_question}")
        
        try:
            # Step 1: Generate search query
            print("Step 1: Generating search query...")
            query_result = self.query_agent(user_question)
            search_query = query_result["content"]
            print(f"🔍 Search query: {search_query}")
            
            # Step 2: Perform web search
            print("Step 2: Performing web search...")
            search_result = self.search_tool(search_query)
            search_results = search_result["content"]
            print(f"🌐 Found {len(search_results)} characters of results")
            
            # Step 3: Generate final answer
            print("Step 3: Generating answer...")
            answer_result = self.answer_agent(search_results, user_question)
            final_answer = answer_result["content"]
            print(f"✅ Generated answer: {final_answer[:100]}...")
            
            return {
                "content": final_answer,
                "metadata": {
                    "search_query": search_query,
                    "search_results_length": len(search_results),
                    "processing_method": "step_by_step",
                    "success": True
                }
            }
            
        except Exception as e:
            print(f"❌ Step-by-step processing error: {e}")
            return {
                "content": f"Processing failed: {str(e)}",
                "metadata": {
                    "processing_method": "step_by_step",
                    "success": False,
                    "error": str(e)
                }
            }


# Initialize the server
server = MCPWebSearchServer()

# FastMCP integration (if available)
if FastMCP:
    try:
        app = FastMCP.from_file(
            __name__,
            path="participants.yaml",
            participants={
                "query_agent": server.query_agent,
                "search_tool": server.search_tool,
                "answer_agent": server.answer_agent,
            }
        )
        print("✅ FastMCP application created successfully")
    except Exception as e:
        print(f"⚠️  FastMCP setup failed: {e}")
        app = None
else:
    app = None


def main():
    """
    Main function for testing the application
    """
    print("🌟 MCP Web Search Answer Application")
    print("=" * 50)
    
    # Test questions
    test_questions = [
        "What's new with OpenAI this month?",
        "Latest developments in AI safety research",
        "Recent updates to Python programming language"
    ]
    
    for question in test_questions:
        print(f"\n🤔 Question: {question}")
        print("-" * 30)
        
        # Process using LangGraph workflow
        try:
            result = server.process_question(question)
            print(f"💡 Answer: {result['content']}")
            
            if 'metadata' in result:
                print(f"🔍 Search Query Used: {result['metadata'].get('search_query', 'N/A')}")
                print(f"✅ Success: {result['metadata'].get('success', False)}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            
            # Fallback to step-by-step processing
            print("🔄 Trying step-by-step processing...")
            try:
                result = server.process_step_by_step(question)
                print(f"💡 Answer: {result['content']}")
            except Exception as e2:
                print(f"❌ Step-by-step also failed: {e2}")
        
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()