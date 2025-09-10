# Browser Tools Documentation 🌐

## Overview
Comprehensive browser automation using Playwright for web interaction, testing, and advanced scraping scenarios requiring JavaScript execution and user interaction simulation.

## Available Tools

### 1. OpenBrowserTool
**Purpose**: Launch and control a browser instance
**Function**: `open_browser`

#### Parameters:
- `headless` (boolean, optional): Run browser without GUI (default: false)
- `browser_type` (string, optional): Browser to use - chrome, firefox, safari (default: chrome)
- `viewport` (object, optional): Browser window size
- `user_agent` (string, optional): Custom user agent string

#### Features:
- 🌐 **Multi-browser support** - Chrome, Firefox, Safari
- 👁️ **Headless/headed modes** - Visual or background operation
- 📱 **Device emulation** - Mobile, tablet, desktop viewports
- 🔒 **Stealth mode** - Bypass bot detection
- 🍪 **Session management** - Persistent cookies and storage

#### Examples:

**Basic browser launch:**
```json
{
  "headless": false,
  "browser_type": "chrome"
}
```

**Mobile device emulation:**
```json
{
  "headless": true,
  "viewport": {
    "width": 375,
    "height": 667,
    "deviceScaleFactor": 2
  },
  "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
}
```

### 2. OpenSearchTool
**Purpose**: Perform search on search engines with browser automation
**Function**: `open_search`

#### Parameters:
- `query` (string): Search query
- `search_engine` (string, optional): Search engine - google, bing, duckduckgo (default: google)
- `num_results` (number, optional): Number of results to extract (default: 10)
- `extract_content` (boolean, optional): Extract page content from results (default: false)

#### Features:
- 🔍 **Multi-engine support** - Google, Bing, DuckDuckGo
- 📊 **Result extraction** - Titles, URLs, snippets
- 📄 **Content scraping** - Full page content from results
- 🛡️ **Anti-detection** - Realistic browsing behavior
- 🎯 **Targeted searches** - Advanced search operators

#### Examples:

**Simple search:**
```json
{
  "query": "machine learning tutorials",
  "search_engine": "google",
  "num_results": 5
}
```

**Advanced search with content extraction:**
```json
{
  "query": "site:github.com python web scraping",
  "search_engine": "google",
  "num_results": 10,
  "extract_content": true
}
```

### 3. BrowserInteractTool
**Purpose**: Interact with web pages (click, type, scroll, etc.)
**Function**: `browser_interact`

#### Parameters:
- `action` (string): Action type - click, type, scroll, wait, screenshot
- `selector` (string, optional): CSS selector for target element
- `text` (string, optional): Text to type (for type action)
- `wait_time` (number, optional): Wait time in seconds
- `scroll_direction` (string, optional): up, down, top, bottom

#### Features:
- 🖱️ **Element interaction** - Click, hover, focus
- ⌨️ **Text input** - Type, clear, select text
- 📜 **Page navigation** - Scroll, navigate, reload
- 📸 **Screenshots** - Full page or element capture
- ⏱️ **Smart waiting** - Wait for elements, content, events

## Advanced Browser Automation

### 1. Multi-Step Web Workflows
```python
# Complete form submission workflow
async def submit_contact_form():
    # 1. Open browser
    await open_browser(headless=False)
    
    # 2. Navigate to page
    await browser_interact(
        action="navigate",
        url="https://example.com/contact"
    )
    
    # 3. Fill form fields
    await browser_interact(
        action="type",
        selector="input[name='name']",
        text="John Doe"
    )
    
    await browser_interact(
        action="type",
        selector="input[name='email']",
        text="john@example.com"
    )
    
    await browser_interact(
        action="type",
        selector="textarea[name='message']",
        text="Hello, I'm interested in your services."
    )
    
    # 4. Submit form
    await browser_interact(
        action="click",
        selector="button[type='submit']"
    )
    
    # 5. Wait for confirmation
    await browser_interact(
        action="wait",
        selector=".success-message",
        wait_time=10
    )
    
    # 6. Take screenshot
    await browser_interact(
        action="screenshot",
        filename="form_submitted.png"
    )
```

### 2. E-commerce Testing
```python
# Product purchase simulation
async def test_purchase_flow():
    await open_browser(headless=True)
    
    # Navigate to product page
    await browser_interact(
        action="navigate",
        url="https://shop.example.com/product/123"
    )
    
    # Select options
    await browser_interact(
        action="click",
        selector="select[name='size'] option[value='large']"
    )
    
    # Add to cart
    await browser_interact(
        action="click",
        selector=".add-to-cart-btn"
    )
    
    # Go to checkout
    await browser_interact(
        action="click",
        selector=".checkout-btn"
    )
    
    # Fill shipping info
    await browser_interact(
        action="type",
        selector="input[name='address']",
        text="123 Main St"
    )
    
    # Take screenshot of checkout
    await browser_interact(
        action="screenshot",
        filename="checkout_page.png"
    )
```

### 3. Social Media Automation
```python
# Social media posting
async def post_to_social():
    await open_browser(headless=False)
    
    # Login (assuming already logged in)
    await browser_interact(
        action="navigate",
        url="https://twitter.com/compose/tweet"
    )
    
    # Compose tweet
    await browser_interact(
        action="type",
        selector="div[data-testid='tweetTextarea_0']",
        text="Excited to share our latest project! #AI #Automation"
    )
    
    # Upload image
    await browser_interact(
        action="upload",
        selector="input[type='file']",
        file_path="project_image.png"
    )
    
    # Wait for upload
    await browser_interact(
        action="wait",
        wait_time=3
    )
    
    # Post tweet
    await browser_interact(
        action="click",
        selector="div[data-testid='tweetButtonInline']"
    )
```

## Browser Configuration

### Chrome Configuration
```json
{
  "browser_type": "chrome",
  "options": {
    "args": [
      "--no-sandbox",
      "--disable-dev-shm-usage",
      "--disable-blink-features=AutomationControlled",
      "--disable-extensions"
    ],
    "ignoreDefaultArgs": ["--enable-automation"],
    "ignoreHTTPSErrors": true
  }
}
```

### Firefox Configuration
```json
{
  "browser_type": "firefox",
  "options": {
    "firefoxUserPrefs": {
      "dom.webdriver.enabled": false,
      "useAutomationExtension": false,
      "general.platform.override": "Win32"
    }
  }
}
```

### Mobile Device Emulation
```json
{
  "browser_type": "chrome",
  "device": "iPhone 12",
  "viewport": {
    "width": 390,
    "height": 844,
    "deviceScaleFactor": 3,
    "isMobile": true,
    "hasTouch": true
  }
}
```

## Stealth and Anti-Detection

### User Agent Rotation
```python
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

await open_browser(
    user_agent=random.choice(user_agents),
    headless=True
)
```

### Realistic Behavior Simulation
```python
# Simulate human-like browsing
async def human_like_interaction():
    # Random delays
    await browser_interact(action="wait", wait_time=random.uniform(1, 3))
    
    # Mouse movements
    await browser_interact(
        action="hover",
        selector=".menu-item"
    )
    
    # Gradual scrolling
    for _ in range(5):
        await browser_interact(
            action="scroll",
            scroll_direction="down",
            scroll_amount=200
        )
        await browser_interact(action="wait", wait_time=0.5)
```

### Proxy Configuration
```json
{
  "proxy": {
    "server": "http://proxy-server:8080",
    "username": "proxy_user",
    "password": "proxy_pass"
  }
}
```

## Testing and Quality Assurance

### Website Testing Checklist
```python
async def website_qa_test():
    tests = [
        {"name": "Homepage loads", "url": "/", "selector": "h1"},
        {"name": "Contact form works", "url": "/contact", "selector": "form"},
        {"name": "Search functions", "url": "/search", "selector": ".search-results"},
        {"name": "Mobile responsive", "device": "iPhone 12", "url": "/"}
    ]
    
    results = []
    for test in tests:
        try:
            await open_browser(
                device=test.get("device"),
                headless=True
            )
            
            await browser_interact(
                action="navigate",
                url=f"https://example.com{test['url']}"
            )
            
            await browser_interact(
                action="wait",
                selector=test["selector"],
                wait_time=10
            )
            
            results.append({"test": test["name"], "status": "PASS"})
        except Exception as e:
            results.append({"test": test["name"], "status": "FAIL", "error": str(e)})
    
    return results
```

### Performance Testing
```python
async def performance_test():
    await open_browser(headless=True)
    
    # Navigate and measure load time
    start_time = time.time()
    await browser_interact(
        action="navigate",
        url="https://example.com"
    )
    
    # Wait for page load
    await browser_interact(
        action="wait",
        selector="body",
        wait_time=30
    )
    
    load_time = time.time() - start_time
    
    # Take performance screenshot
    await browser_interact(
        action="screenshot",
        filename=f"performance_test_{load_time:.2f}s.png"
    )
    
    return {"load_time": load_time}
```

## Error Handling

### Common Issues and Solutions

#### Element Not Found
```python
try:
    await browser_interact(
        action="click",
        selector=".button",
        wait_time=10
    )
except ElementNotFoundError:
    # Try alternative selector
    await browser_interact(
        action="click",
        selector="button[type='submit']"
    )
```

#### Page Load Timeout
```python
try:
    await browser_interact(
        action="navigate",
        url="https://slow-site.com",
        timeout=30000
    )
except TimeoutError:
    # Retry with longer timeout
    await browser_interact(
        action="navigate",
        url="https://slow-site.com",
        timeout=60000
    )
```

#### Browser Crash Recovery
```python
async def robust_browser_action(action_func):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await action_func()
        except BrowserCrashError:
            if attempt < max_retries - 1:
                # Restart browser
                await open_browser(headless=True)
            else:
                raise
```

## Best Practices

### Resource Management
1. **Close browsers** - Always clean up browser instances
2. **Limit concurrent browsers** - Avoid memory exhaustion
3. **Use headless mode** - For better performance
4. **Monitor memory usage** - Watch for memory leaks

### Security Considerations
1. **Validate URLs** - Check URLs before navigation
2. **Sanitize inputs** - Clean user-provided data
3. **Use HTTPS** - Prefer secure connections
4. **Handle credentials safely** - Never log sensitive data

### Performance Optimization
1. **Reuse browser instances** - Avoid frequent launches
2. **Disable unnecessary features** - Images, CSS for faster loading
3. **Use appropriate wait strategies** - Smart waiting vs fixed delays
4. **Optimize selectors** - Use efficient CSS selectors

### Debugging Tips
1. **Enable screenshots** - Visual debugging
2. **Use console logs** - Monitor browser console
3. **Slow down actions** - For debugging complex interactions
4. **Record videos** - For complex workflow debugging
