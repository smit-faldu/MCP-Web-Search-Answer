"""
Search Tool - Performs web search using SerpAPI
Fetches top 5 Google search results and formats them for the answer agent
"""

import os
from typing import Dict, Any, List
from serpapi import GoogleSearch


class SearchTool:
    """
    Tool that performs Google searches using SerpAPI and formats results
    """
    
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_KEY not found in environment variables")
    
    def __call__(self, input_data: str) -> Dict[str, Any]:
        """
        Perform Google search and return formatted results
        
        Args:
            input_data: Search query string
            
        Returns:
            Dict with content key containing formatted search results
        """
        try:
            # Configure search parameters
            search_params = {
                "q": input_data,
                "api_key": self.api_key,
                "engine": "google",
                "num": 5,  # Get top 5 results
                "safe": "active"
            }
            
            # Perform the search
            search = GoogleSearch(search_params)
            results = search.get_dict()
            
            # Format the results
            formatted_results = self._format_results(results)
            
            return {
                "content": formatted_results
            }
            
        except Exception as e:
            return {
                "content": f"Error performing search: {str(e)}"
            }
    
    def _format_results(self, results: Dict) -> str:
        """
        Format search results into readable text
        
        Args:
            results: Raw SerpAPI results dictionary
            
        Returns:
            Formatted string with titles and snippets
        """
        if "organic_results" not in results:
            return "No search results found."
        
        formatted_text = "Search Results:\n\n"
        
        for i, result in enumerate(results["organic_results"][:5], 1):
            title = result.get("title", "No title")
            snippet = result.get("snippet", "No description available")
            link = result.get("link", "")
            
            formatted_text += f"{i}. {title}\n"
            formatted_text += f"   {snippet}\n"
            formatted_text += f"   Source: {link}\n\n"
        
        return formatted_text.strip()
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """
        Alternative method that returns structured results
        
        Args:
            query: Search query string
            
        Returns:
            List of dictionaries with title, snippet, and link
        """
        try:
            search_params = {
                "q": query,
                "api_key": self.api_key,
                "engine": "google",
                "num": 5,
                "safe": "active"
            }
            
            search = GoogleSearch(search_params)
            results = search.get_dict()
            
            if "organic_results" not in results:
                return []
            
            structured_results = []
            for result in results["organic_results"][:5]:
                structured_results.append({
                    "title": result.get("title", "No title"),
                    "snippet": result.get("snippet", "No description available"),
                    "link": result.get("link", "")
                })
            
            return structured_results
            
        except Exception as e:
            return [{"title": "Error", "snippet": f"Search failed: {str(e)}", "link": ""}]