"""
AI Tools Framework: serper_search.py
Description: AI Tools Framework component
Author: Eric Hiss (GitHub: EricRollei)
Contact: [eric@historic.camera, eric@rollei.us]
Version: 1.0.0
Date: 2025-09-09
License: Dual License (Non-Commercial and Commercial Use)
Copyright (c) 2025 Eric Hiss. All rights reserved.

Dual License:
1. Non-Commercial Use: This software is licensed under the terms of the
   Creative Commons Attribution-NonCommercial 4.0 International License.
   To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/
   
2. Commercial Use: For commercial use, a separate license is required.
   Please contact Eric Hiss at [eric@historic.camera, eric@rollei.us] for licensing options.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT.

Dependencies:
This code depends on several third-party libraries, each with its own license.
See LICENSE file for complete dependency information.

serper_search.py - Part of AI Tools Framework
A comprehensive productivity framework with 27 tools for Claude Desktop and LM Studio
"""

# tools/serper_search.py
import httpx
import json
from typing import Dict, Any, Optional, List
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from config.settings import settings

class SerperSearchTool(BaseTool):
    """Web search tool using Serper.dev API"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.api_key = self.config.get('api_key') if self.config else settings.serper_api_key
        
        if not self.api_key:
            raise ValueError("Serper API key is required. Set SERPER_API_KEY environment variable or pass api_key in config.")
        
        self.base_url = "https://google.serper.dev"
        self.timeout = self.config.get('timeout', settings.timeout_seconds)  # ← Use self.config instead of config
        
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="web_search",
            description="Search the web using Google via Serper.dev API. Returns organic search results, knowledge graph, and related information.",
            category="search",
            parameters=[
                ToolParameter(
                    name="query",
                    param_type="string",
                    description="The search query to execute",
                    required=True
                ),
                ToolParameter(
                    name="num_results",
                    param_type="number",
                    description="Number of search results to return (1-100)",
                    required=False,
                    default=10
                ),
                ToolParameter(
                    name="country",
                    param_type="string",
                    description="Country code for localized results (e.g., 'us', 'uk', 'ca')",
                    required=False,
                    default="us"
                ),
                ToolParameter(
                    name="language",
                    param_type="string", 
                    description="Language code for results (e.g., 'en', 'es', 'fr')",
                    required=False,
                    default="en"
                ),
                ToolParameter(
                    name="search_type",
                    param_type="string",
                    description="Type of search to perform",
                    required=False,
                    default="search",
                    enum_values=["search", "images", "videos", "news", "shopping", "scholar"]
                )
            ]
        )
    
    async def execute(self, **kwargs) -> ToolResult:
        """Execute web search using Serper API"""
        try:
            # Validate parameters
            params = self.validate_parameters(kwargs)
            
            # Prepare API request
            endpoint = f"/{params.get('search_type', 'search')}"
            url = f"{self.base_url}{endpoint}"
            
            payload = {
                "q": params["query"],
                "num": min(params.get("num_results", 10), 100),
                "gl": params.get("country", "us"),
                "hl": params.get("language", "en")
            }
            
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            self.logger.info(f"Executing search: {params['query']}")
            
            # Make API request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url, 
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                
            result_data = response.json()
            
            # Process and structure the results
            processed_results = self._process_search_results(result_data, params)
            
            return ToolResult(
                success=True,
                result_type="json",
                content=processed_results,
                metadata={
                    "query": params["query"],
                    "search_type": params.get("search_type", "search"),
                    "num_results": len(processed_results.get("organic", [])),
                    "api_response_time": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else None
                }
            )
            
        except httpx.HTTPStatusError as e:
            error_msg = f"Serper API error ({e.response.status_code}): {e.response.text}"
            self.logger.error(error_msg)
            return ToolResult(
                success=False,
                result_type="error",
                content=None,
                error_message=error_msg
            )
            
        except Exception as e:
            error_msg = f"Search execution failed: {str(e)}"
            self.logger.error(error_msg)
            return ToolResult(
                success=False,
                result_type="error",
                content=None,
                error_message=error_msg
            )
    
    def _process_search_results(self, raw_data: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Process and clean up search results"""
        processed = {
            "query": params["query"],
            "search_type": params.get("search_type", "search"),
            "organic": [],
            "knowledge_graph": None,
            "answer_box": None,
            "related_searches": [],
            "metadata": {}
        }
        
        # Process organic results
        if "organic" in raw_data:
            for result in raw_data["organic"]:
                processed_result = {
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "position": result.get("position", 0)
                }
                
                # Add optional fields if present
                if "sitelinks" in result:
                    processed_result["sitelinks"] = result["sitelinks"]
                if "date" in result:
                    processed_result["date"] = result["date"]
                    
                processed["organic"].append(processed_result)
        
        # Process knowledge graph
        if "knowledgeGraph" in raw_data:
            kg = raw_data["knowledgeGraph"]
            processed["knowledge_graph"] = {
                "title": kg.get("title", ""),
                "type": kg.get("type", ""),
                "description": kg.get("description", ""),
                "url": kg.get("website", ""),
                "image_url": kg.get("imageUrl", ""),
                "attributes": kg.get("attributes", {})
            }
        
        # Process answer box
        if "answerBox" in raw_data:
            ab = raw_data["answerBox"]
            processed["answer_box"] = {
                "answer": ab.get("answer", ""),
                "title": ab.get("title", ""),
                "url": ab.get("link", "")
            }
        
        # Process related searches
        if "relatedSearches" in raw_data:
            processed["related_searches"] = [
                search.get("query", "") for search in raw_data["relatedSearches"]
            ]
        
        # Add metadata
        processed["metadata"] = {
            "total_results": len(processed["organic"]),
            "has_knowledge_graph": processed["knowledge_graph"] is not None,
            "has_answer_box": processed["answer_box"] is not None,
            "search_parameters": raw_data.get("searchParameters", {})
        }
        
        return processed

# tools/__init__.py
from .serper_search import SerperSearchTool

# Auto-register tools
from core.registry import registry

registry.register(SerperSearchTool)

__all__ = ["SerperSearchTool"]
