# tools/web_scraper_tools.py
"""
Advanced web scraping tools with anti-bot detection features
"""

import aiohttp
import asyncio
import json
import re
from typing import Optional, Dict, Any
from urllib.parse import urljoin, urlparse
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

class AdvancedWebScraperTool(BaseTool):
    """Advanced web scraper with anti-bot detection and academic site support"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="advanced_web_scraper",
            description="Advanced web scraper that can handle academic sites, paywalls, and anti-bot protection",
            category="web",
            parameters=[
                ToolParameter(
                    name="url",
                    description="URL to scrape",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="extraction_mode",
                    description="What to extract: 'text' (clean text), 'html' (raw HTML), 'article' (article content), 'title_and_abstract' (for academic papers)",
                    param_type="string",
                    required=False,
                    default="article"
                ),
                ToolParameter(
                    name="max_length",
                    description="Maximum characters to return (0 = no limit)",
                    param_type="number",
                    required=False,
                    default=20000
                ),
                ToolParameter(
                    name="bypass_paywall",
                    description="Attempt to bypass academic paywalls using common techniques",
                    param_type="boolean",
                    required=False,
                    default=True
                ),
                ToolParameter(
                    name="delay_seconds",
                    description="Delay between requests to avoid rate limiting",
                    param_type="number",
                    required=False,
                    default=2
                )
            ]
        )
    
    async def execute(self, url: str, extraction_mode: str = "article", 
                     max_length: int = 20000, bypass_paywall: bool = True,
                     delay_seconds: float = 2) -> ToolResult:
        """Execute advanced web scraping"""
        try:
            # Add delay to avoid rate limiting
            if delay_seconds > 0:
                await asyncio.sleep(delay_seconds)
            
            content = await self._scrape_with_multiple_strategies(url, extraction_mode, bypass_paywall)
            
            if not content:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="Failed to extract content from the webpage",
                    error_message="No content could be extracted"
                )
            
            # Apply length limit if specified
            if max_length > 0 and len(content) > max_length:
                content = content[:max_length] + "...\n\n[Content truncated]"
            
            return ToolResult(
                success=True,
                result_type=ToolResultType.TEXT,
                content=content,
                metadata={
                    "url": url,
                    "extraction_mode": extraction_mode,
                    "content_length": len(content),
                    "truncated": max_length > 0 and len(content) > max_length
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Web scraping failed: {str(e)}",
                error_message=str(e)
            )
    
    async def _scrape_with_multiple_strategies(self, url: str, extraction_mode: str, bypass_paywall: bool) -> str:
        """Try multiple scraping strategies"""
        
        strategies = [
            self._strategy_browser_headers,
            self._strategy_academic_site,
            self._strategy_simple_request
        ]
        
        if bypass_paywall:
            strategies.insert(0, self._strategy_bypass_paywall)
        
        for strategy in strategies:
            try:
                content = await strategy(url, extraction_mode)
                if content and len(content.strip()) > 100:  # Minimum content threshold
                    return content
            except Exception as e:
                print(f"Strategy {strategy.__name__} failed: {e}")
                continue
        
        return ""
    
    async def _strategy_browser_headers(self, url: str, extraction_mode: str) -> str:
        """Strategy 1: Use realistic browser headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        return await self._fetch_and_extract(url, headers, extraction_mode)
    
    async def _strategy_academic_site(self, url: str, extraction_mode: str) -> str:
        """Strategy 2: Optimized for academic sites like ScienceDirect, PubMed"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Try different URL variations for academic sites
        urls_to_try = [url]
        
        # For ScienceDirect, try different access patterns
        if 'sciencedirect.com' in url:
            if '?via%3Dihub' not in url:
                urls_to_try.append(url + '?via%3Dihub')
            # Try the open access version
            if '/pii/' in url:
                pii_match = re.search(r'/pii/([A-Z0-9]+)', url)
                if pii_match:
                    pii = pii_match.group(1)
                    urls_to_try.append(f"https://www.sciencedirect.com/science/article/pii/{pii}?dgcid=rss_sd_all")
        
        # For PMC articles, try direct PMC link
        if 'pmc.ncbi.nlm.nih.gov' in url:
            # Already a good URL
            pass
        
        for test_url in urls_to_try:
            try:
                content = await self._fetch_and_extract(test_url, headers, extraction_mode)
                if content and len(content.strip()) > 100:
                    return content
            except:
                continue
        
        return ""
    
    async def _strategy_bypass_paywall(self, url: str, extraction_mode: str) -> str:
        """Strategy 3: Try common paywall bypass techniques"""
        
        # Try archive.today first
        archive_urls = [
            f"https://archive.today/{url}",
            f"https://web.archive.org/web/newest/{url}",
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for archive_url in archive_urls:
            try:
                content = await self._fetch_and_extract(archive_url, headers, extraction_mode)
                if content and len(content.strip()) > 100:
                    return content
            except:
                continue
        
        # Try removing tracking parameters
        clean_url = url.split('?')[0]
        if clean_url != url:
            try:
                content = await self._fetch_and_extract(clean_url, headers, extraction_mode)
                if content and len(content.strip()) > 100:
                    return content
            except:
                pass
        
        return ""
    
    async def _strategy_simple_request(self, url: str, extraction_mode: str) -> str:
        """Strategy 4: Simple request as fallback"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Research Bot)'
        }
        
        return await self._fetch_and_extract(url, headers, extraction_mode)
    
    async def _fetch_and_extract(self, url: str, headers: Dict[str, str], extraction_mode: str) -> str:
        """Fetch URL and extract content based on mode"""
        
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(verify_ssl=False)  # Bypass SSL issues
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            async with session.get(url, headers=headers) as response:
                if response.status not in [200, 201]:
                    raise Exception(f"HTTP {response.status}: {response.reason}")
                
                html = await response.text()
                
                # Extract content based on mode
                if extraction_mode == "html":
                    return html
                elif extraction_mode == "text":
                    return self._html_to_text(html)
                elif extraction_mode == "article":
                    return self._extract_article_content(html, url)
                elif extraction_mode == "title_and_abstract":
                    return self._extract_title_and_abstract(html)
                else:
                    return self._extract_article_content(html, url)
    
    def _html_to_text(self, html: str) -> str:
        """Convert HTML to clean text"""
        # Remove scripts and styles
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def _extract_article_content(self, html: str, url: str) -> str:
        """Extract article content using multiple selectors"""
        
        # Common article content selectors
        content_selectors = [
            # ScienceDirect
            r'<div[^>]*class="[^"]*Body[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*id="article-body"[^>]*>(.*?)</div>',
            
            # PMC/PubMed
            r'<div[^>]*class="[^"]*article[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
            
            # Generic article selectors
            r'<article[^>]*>(.*?)</article>',
            r'<main[^>]*>(.*?)</main>',
            r'<div[^>]*class="[^"]*text[^"]*"[^>]*>(.*?)</div>',
        ]
        
        # Try to extract abstract first
        abstract = self._extract_abstract(html)
        
        # Try content selectors
        content = ""
        for selector in content_selectors:
            matches = re.findall(selector, html, flags=re.DOTALL | re.IGNORECASE)
            if matches:
                content = ' '.join(matches)
                break
        
        # If no content found, get the body
        if not content:
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, flags=re.DOTALL | re.IGNORECASE)
            if body_match:
                content = body_match.group(1)
        
        # Clean and format
        if content:
            text = self._html_to_text(content)
            
            # Add abstract at the beginning if found
            if abstract:
                text = f"ABSTRACT:\n{abstract}\n\n" + text
            
            return text
        
        return self._html_to_text(html)
    
    def _extract_abstract(self, html: str) -> str:
        """Extract abstract from academic papers"""
        abstract_patterns = [
            r'<div[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</div>',
            r'<section[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</section>',
            r'<p[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</p>',
            r'<div[^>]*id="abstract"[^>]*>(.*?)</div>',
        ]
        
        for pattern in abstract_patterns:
            matches = re.findall(pattern, html, flags=re.DOTALL | re.IGNORECASE)
            if matches:
                abstract_html = matches[0]
                return self._html_to_text(abstract_html)
        
        return ""
    
    def _extract_title_and_abstract(self, html: str) -> str:
        """Extract just title and abstract"""
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, flags=re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "No title found"
        
        # Extract abstract
        abstract = self._extract_abstract(html)
        
        result = f"TITLE: {title}\n\n"
        if abstract:
            result += f"ABSTRACT: {abstract}"
        else:
            result += "ABSTRACT: No abstract found"
        
        return result

# Register the tool
registry.register(AdvancedWebScraperTool)
