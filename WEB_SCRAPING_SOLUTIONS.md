# Web Scraping Solutions Documentation 🕷️

## Overview
Advanced web scraping capabilities with anti-bot protection, academic site optimization, and multiple fallback strategies for reliable content extraction.

## Available Tools

### 1. WebScrapeTool
**Purpose**: Extract content from web pages with intelligent fallback strategies
**Function**: `web_scrape`

#### Parameters:
- `url` (string): Target URL to scrape
- `selector` (string, optional): CSS selector for specific content
- `wait_time` (number, optional): Wait time for dynamic content (seconds)
- `use_archive` (boolean, optional): Fallback to archive.today if blocked
- `extract_text` (boolean, optional): Extract clean text only (default: false)

#### Features:
- 🛡️ **Anti-bot protection** - Realistic browser headers and behavior
- 🎓 **Academic site optimization** - Specialized handling for research sites
- 📚 **Paywall bypass** - Archive.today fallback for blocked content
- 🔄 **Multiple strategies** - Direct, Playwright, archive fallback
- 🧹 **Content cleaning** - Remove ads, navigation, extract main content
- ⚡ **Smart parsing** - Automatic content type detection

## Scraping Strategies

### Strategy 1: Direct HTTP Request
**Best for**: Simple static content, APIs, basic HTML pages
**Speed**: Fastest (100-500ms)
**Reliability**: Good for non-protected sites

```json
{
  "url": "https://example.com/article",
  "extract_text": true
}
```

### Strategy 2: Browser Automation (Playwright)
**Best for**: JavaScript-heavy sites, dynamic content, complex interactions
**Speed**: Slower (2-5 seconds)
**Reliability**: Highest for modern web apps

```json
{
  "url": "https://spa-app.com/data",
  "wait_time": 3,
  "selector": ".main-content"
}
```

### Strategy 3: Archive Fallback
**Best for**: Paywalled content, geo-blocked sites, temporarily unavailable content
**Speed**: Variable (1-10 seconds)
**Reliability**: Good for recent content

```json
{
  "url": "https://paywalled-news.com/article",
  "use_archive": true,
  "extract_text": true
}
```

## Advanced Usage Examples

### 1. News Article Extraction
```json
{
  "url": "https://news.site.com/article/12345",
  "selector": "article, .article-content, .post-content",
  "extract_text": true,
  "use_archive": true
}
```

### 2. Academic Paper Scraping
```json
{
  "url": "https://arxiv.org/abs/2301.12345",
  "selector": ".ltx_abstract, .ltx_title",
  "wait_time": 2
}
```

### 3. E-commerce Product Info
```json
{
  "url": "https://shop.com/product/123",
  "selector": ".product-title, .price, .description",
  "wait_time": 3
}
```

### 4. Social Media Content
```json
{
  "url": "https://twitter.com/user/status/123",
  "wait_time": 5,
  "selector": "[data-testid='tweetText']"
}
```

### 5. Documentation Scraping
```json
{
  "url": "https://docs.example.com/api",
  "selector": ".content, .documentation",
  "extract_text": false
}
```

## CSS Selector Guide

### Basic Selectors
- `.class-name` - Elements with specific class
- `#element-id` - Element with specific ID
- `tag-name` - HTML tag elements
- `[attribute]` - Elements with attribute

### Advanced Selectors
- `.parent .child` - Descendant selector
- `.parent > .child` - Direct child selector
- `.element:first-child` - First child element
- `.element:contains("text")` - Contains text
- `.element:not(.exclude)` - Exclude elements

### Common Content Selectors
- `article, .article, .post` - Article content
- `.content, .main, .body` - Main content areas
- `h1, h2, .title, .headline` - Titles and headlines
- `p, .text, .description` - Text content
- `.price, .cost, .amount` - Pricing information

## Academic Site Optimizations

### Supported Academic Platforms
- **arXiv**: Preprint repository
- **JSTOR**: Academic journals
- **IEEE Xplore**: Engineering papers
- **ACM Digital Library**: Computer science
- **PubMed**: Medical literature
- **Google Scholar**: Citation database

### Academic-Specific Features
```json
{
  "url": "https://arxiv.org/abs/2301.12345",
  "academic_mode": true,
  "extract_citation": true,
  "download_pdf": false
}
```

### Research Paper Extraction
- **Abstracts**: Automatic abstract detection
- **Citations**: Reference extraction
- **Metadata**: Author, publication date, DOI
- **Full text**: When available without paywall

## Anti-Bot Protection

### Header Rotation
The scraper automatically rotates between realistic browser headers:
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
```

### Behavioral Mimicking
- Random delays between requests
- Mouse movement simulation
- Scroll behavior emulation
- Realistic viewport sizes

### IP Protection
- Request spacing to avoid rate limits
- Session management
- Cookie handling
- Referer header management

## Content Cleaning

### Automatic Removal
- **Navigation menus** - Site navigation elements
- **Advertisements** - Ad blocks and sponsored content  
- **Sidebars** - Supplementary content areas
- **Footer content** - Site footer information
- **Pop-ups** - Modal dialogs and overlays

### Text Extraction Features
- **Paragraph preservation** - Maintains text structure
- **Link extraction** - Preserves important links
- **Image alt text** - Includes accessible descriptions
- **List formatting** - Maintains bullet points and numbering

## Error Handling & Fallbacks

### Common Errors and Solutions

#### 403 Forbidden / Bot Detection
**Strategy**: Automatic fallback sequence
1. Retry with different headers
2. Switch to Playwright browser
3. Use archive.today fallback
4. Report failure with suggestions

#### 404 Not Found
**Strategy**: Archive lookup
1. Check archive.today for cached version
2. Try common URL variations
3. Report unavailable content

#### Timeout / Slow Loading
**Strategy**: Progressive timeouts
1. Start with 5-second timeout
2. Increase to 15 seconds for complex sites
3. Use Playwright for dynamic content
4. Report timeout with partial results

#### Paywall / Premium Content
**Strategy**: Archive fallback
1. Attempt archive.today lookup
2. Extract preview content if available
3. Report paywall detection
4. Suggest alternative sources

## Performance Optimization

### Speed Strategies
1. **Concurrent requests** - Process multiple URLs
2. **Smart caching** - Cache successful responses
3. **Selective parsing** - Only extract needed content
4. **Compression** - Use gzip encoding

### Resource Management
1. **Browser pooling** - Reuse Playwright instances
2. **Memory cleanup** - Clear large responses
3. **Connection limits** - Respect server resources
4. **Timeout handling** - Prevent hanging requests

## Legal and Ethical Considerations

### Best Practices
1. **Respect robots.txt** - Check site scraping policies
2. **Rate limiting** - Don't overwhelm servers
3. **Attribution** - Credit sources when required
4. **Copyright** - Respect intellectual property
5. **Terms of service** - Follow site ToS

### Responsible Scraping
- Use reasonable delays between requests
- Scrape during off-peak hours when possible
- Cache results to minimize repeated requests
- Focus on publicly available content
- Respect site bandwidth limitations

## Troubleshooting Guide

### Issue: Empty Results
**Causes**:
- Incorrect CSS selector
- Dynamic content not loaded
- Anti-bot blocking

**Solutions**:
```json
{
  "url": "https://example.com",
  "wait_time": 5,
  "selector": "body",
  "use_archive": true
}
```

### Issue: Partial Content
**Causes**:
- JavaScript-rendered content
- Lazy loading
- Authentication required

**Solutions**:
- Increase wait_time
- Use more specific selectors
- Try archive fallback

### Issue: Rate Limiting
**Causes**:
- Too many requests
- IP blocking
- User-agent detection

**Solutions**:
- Add delays between requests
- Rotate user agents
- Use archive.today

## Integration Examples

### 1. Research Workflow
```python
# Scrape multiple academic sources
sources = [
    "https://arxiv.org/abs/2301.12345",
    "https://scholar.google.com/citations?user=abc123",
    "https://pubmed.ncbi.nlm.nih.gov/12345678"
]

research_data = []
for url in sources:
    content = await web_scrape(
        url=url,
        extract_text=True,
        use_archive=True
    )
    research_data.append(content)
```

### 2. Content Monitoring
```python
# Monitor news sites for specific topics
news_sites = [
    "https://news.site.com/technology",
    "https://tech.blog.com/latest"
]

for site in news_sites:
    articles = await web_scrape(
        url=site,
        selector=".article-link",
        extract_text=False
    )
    # Process article links...
```

### 3. Price Monitoring
```python
# Track product prices across sites
products = [
    {"url": "https://shop1.com/product/123", "selector": ".price"},
    {"url": "https://shop2.com/item/456", "selector": ".cost"}
]

for product in products:
    price_data = await web_scrape(
        url=product["url"],
        selector=product["selector"],
        extract_text=True
    )
    # Compare prices...
```
