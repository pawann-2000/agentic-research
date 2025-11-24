import os
from typing import List, Dict, Any, Optional
from exa_py import Exa
from llama_index.core.tools import FunctionTool

class ExaSearchTools:

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("EXA_API_KEY")
        if not self.api_key:
            raise ValueError("EXA_API_KEY not found in the environment variables")
        
        self.client = Exa(api_key=self.api_key)

    def search_web(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        
        try:
            results = self.client.search_and_contents(
                query,
                num_results=num_results,
            )

            formatted_results = {
                "query": query,
                "num_results": len(results.results),
                "results": []
            }

            for result in results.results:
                formatted_results["results"].append({
                    "title": result.title,
                    "url": result.url,
                    "published_date": getattr(result, "published_date", None),
                    "author": getattr(result, "author", None),
                    "highlights": getattr(result, "highlights", []),
                    "text": getattr(result, "text", "")
                })
            
            return formatted_results
        
        except Exception as e:
            return {
                "error": f"Search result failed: {str(e)}",
                "query": query,
                "results": []
            }
    
    def get_content(self, url: str) -> Dict[str, Any]:

        try:
            result = self.client.get_contents([url])

            if result.results:
                content = result.results[0]
                return {
                    "url": url,
                    "title": content.title,
                    "author": getattr(content, "author", None),
                    "published_date": getattr(content, "published_date", None),
                    "success": True
                }
            else:
                return {
                    "url": url,
                    "error": "No content found",
                    "success": False
                }
        except Exception as e:
            return {
                "url": url,
                "error": f"Content fetch failed: {str(e)}",
                "success": False
            }
        
    def find_similar(self, url: str, num_results: int = 5) -> Dict[str, Any]:

        try:
            results = self.client.find_similar(
                url,
                num_results=num_results
            )

            formatted_results = {
                "reference_url": url,
                "num_results": len(results.results),
                "results": []
            }

            for result in results.results:
                formatted_results["results"].append({
                    "title": result.title,
                    "url": result.url,
                    "published_date": getattr(result, "published_date", None)
                })

            return formatted_results
        
        except Exception as e:
            return {
                "error": f"Similarity search failed: {str(e)}",
                "reference_url": url,
                "results": []
            }
    
def create_search_tool(exa_client: ExaSearchTools) -> FunctionTool:

    return FunctionTool.from_defaults(
        fn=exa_client.search_web,
        name="search_web",
        description="""Perform semantic web search to find relevant information.
        Use this when you need to find information on the internet about a topic
        Args:
            query (str): The search query
            num_results (int): Number of results to return (default: 5)
        Returns:
            Dictionary with search results including titles, URLs, highlights and text snippets.
        """
    )

def create_content_tool(exa_client: ExaSearchTools) -> FunctionTool:

    return FunctionTool.from_defaults(
        fn=exa_client.get_content,
        name="get_content",
        description="""Fetch full content fomr a specific URL.
        Use this when you need to read the complete content of a webpage
        Args:
            url (str): The URL to fetch content from
        Returns:
            Dictionary with the full page content, title, author, and publication date.
        """
    )

def create_similar_tool(exa_client: ExaSearchTools) -> FunctionTool:

    return FunctionTool.from_defaults(
        fn=exa_client.find_similar,
        name="find_similar",
        description="""Find webpages similar to a given URL.
        Use this to discover related content and sources.
        Args:
            url (str): The reference URL.
            num_results (int): Number of results to return (default: 5)
        Returns:
            Dictionary with similar search results.
        """
    )
