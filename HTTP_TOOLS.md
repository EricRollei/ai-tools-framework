# HTTP Tools Documentation 🌐

## Overview
The HTTP tools provide powerful web communication capabilities with anti-bot protection, session management, and file download functionality.

## Available Tools

### 1. HTTPRequestTool
**Purpose**: Make HTTP/HTTPS requests with advanced features
**Function**: `http_request`

#### Parameters:
- `url` (string): Target URL 
- `method` (string): HTTP method (GET, POST, PUT, DELETE, etc.)
- `headers` (object, optional): Custom headers
- `data` (object, optional): Request body data
- `params` (object, optional): URL parameters
- `timeout` (number, optional): Request timeout in seconds

#### Features:
- ✅ **Anti-bot protection** - Realistic browser headers
- ✅ **Session management** - Automatic cookie handling
- ✅ **SSL verification** - Secure connections
- ✅ **Error handling** - Comprehensive error reporting
- ✅ **JSON/Form data** - Automatic content-type detection

#### Examples:

**Simple GET request:**
```json
{
  "url": "https://api.example.com/data",
  "method": "GET"
}
```

**POST with data:**
```json
{
  "url": "https://api.example.com/submit",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer your-token"
  },
  "data": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**API call with parameters:**
```json
{
  "url": "https://api.example.com/search",
  "method": "GET",
  "params": {
    "q": "search term",
    "limit": 10,
    "page": 1
  }
}
```

### 2. DownloadFileTool
**Purpose**: Download files from URLs with progress tracking
**Function**: `download_file`

#### Parameters:
- `url` (string): File URL to download
- `filename` (string, optional): Local filename (auto-detected if not provided)
- `chunk_size` (number, optional): Download chunk size (default: 8192)

#### Features:
- ✅ **Progress tracking** - Real-time download progress
- ✅ **Resume capability** - Resume interrupted downloads
- ✅ **Size verification** - Verify file integrity
- ✅ **Auto-naming** - Extract filename from URL
- ✅ **Large file support** - Efficient streaming download

#### Examples:

**Simple download:**
```json
{
  "url": "https://example.com/document.pdf"
}
```

**Download with custom filename:**
```json
{
  "url": "https://example.com/file.zip",
  "filename": "my_download.zip"
}
```

## Advanced Usage

### 1. API Integration
```python
# Multi-step API workflow
# 1. Authenticate
auth_response = await http_request(
    url="https://api.example.com/auth",
    method="POST",
    data={"username": "user", "password": "pass"}
)

# 2. Use token for subsequent requests
token = auth_response["access_token"]
data = await http_request(
    url="https://api.example.com/protected",
    method="GET",
    headers={"Authorization": f"Bearer {token}"}
)
```

### 2. Web Scraping Support
```python
# Get page content for scraping
html = await http_request(
    url="https://news.ycombinator.com",
    method="GET",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
)
```

### 3. File Upload
```python
# Upload file using multipart/form-data
await http_request(
    url="https://upload.example.com",
    method="POST",
    headers={"Content-Type": "multipart/form-data"},
    data={"file": file_content, "description": "My upload"}
)
```

## Error Handling

### Common HTTP Errors:
- **400 Bad Request**: Check URL and parameters
- **401 Unauthorized**: Verify authentication headers
- **403 Forbidden**: Check permissions/API limits
- **404 Not Found**: Verify URL exists
- **429 Too Many Requests**: Implement rate limiting
- **500 Server Error**: Retry with backoff

### Timeout Issues:
```json
{
  "url": "https://slow-api.example.com",
  "method": "GET",
  "timeout": 30
}
```

## Best Practices

### 1. Rate Limiting
- Add delays between requests to avoid being blocked
- Respect `Retry-After` headers
- Monitor response codes for rate limiting

### 2. Headers
- Always include realistic `User-Agent`
- Use appropriate `Accept` headers
- Include `Referer` when necessary

### 3. Error Handling
- Implement retry logic for transient failures
- Log request/response details for debugging
- Handle different content types appropriately

### 4. Security
- Never log sensitive headers (Authorization, API keys)
- Validate URLs before making requests
- Use HTTPS when possible

## Troubleshooting

### Issue: 403 Forbidden
**Cause**: Anti-bot protection
**Solution**: Add more realistic headers:
```json
{
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
  }
}
```

### Issue: SSL Certificate Error
**Solution**: Check certificate validity or disable verification for testing

### Issue: Slow Downloads
**Solution**: Increase chunk size or check network connection
