# Everything Integration Documentation 🔍

## Overview
Ultra-fast file searching using Everything CLI integration. This provides instant system-wide file search capabilities with advanced filtering and sorting options.

## Everything CLI Integration

### Prerequisites
- Everything application installed
- Everything CLI (es.exe) in PATH or at known location
- Everything service running in background

### Current Configuration
- **Everything Path**: `C:\Program Files\ES-1.1.0.30.x64\es.exe`
- **Integration Status**: ✅ Active and tested
- **Search Speed**: Sub-second results for entire system

## Available Tools

### 1. SearchFilesTool
**Purpose**: Lightning-fast file system search
**Function**: `search_files`

#### Parameters:
- `query` (string): Search query using Everything syntax
- `max_results` (number, optional): Maximum results to return (default: 100)
- `sort` (string, optional): Sort order - name, size, date, type
- `path_filter` (string, optional): Limit search to specific directory

#### Features:
- ⚡ **Instant search** - Sub-second results
- 🌐 **System-wide** - Searches entire file system
- 🔍 **Advanced syntax** - Powerful query language
- 📊 **Metadata** - Size, dates, attributes
- 🎯 **Precise filtering** - Extensions, paths, sizes

#### Examples:

**Simple filename search:**
```json
{
  "query": "report.pdf"
}
```

**Extension-based search:**
```json
{
  "query": "*.py",
  "max_results": 50,
  "sort": "date"
}
```

**Path-specific search:**
```json
{
  "query": "config",
  "path_filter": "C:\\Users\\",
  "sort": "name"
}
```

**Size-based search:**
```json
{
  "query": "size:>100mb *.mp4"
}
```

## Everything Search Syntax

### Basic Searches
- `filename.txt` - Exact filename
- `report` - Contains "report" in filename
- `*.pdf` - All PDF files
- `photo*.jpg` - Files starting with "photo" ending in .jpg

### Advanced Syntax
- `ext:py` - Files with .py extension
- `size:>10mb` - Files larger than 10MB
- `dm:today` - Files modified today
- `dc:yesterday` - Files created yesterday
- `path:downloads` - Files in Downloads folder

### Wildcards
- `?` - Single character wildcard
- `*` - Multiple character wildcard
- `**` - Match any number of directories

### Operators
- `AND` / `&` - Both terms must match
- `OR` / `|` - Either term can match
- `NOT` / `!` - Exclude term
- `()` - Group terms

### Date Filters
- `dm:today` - Modified today
- `dm:yesterday` - Modified yesterday
- `dm:2024` - Modified in 2024
- `dm:>2024/01/01` - Modified after date
- `dc:thisweek` - Created this week

### Size Filters
- `size:empty` - Empty files
- `size:<1kb` - Smaller than 1KB
- `size:1mb-10mb` - Between 1MB and 10MB
- `size:gigantic` - Very large files

### Attribute Filters
- `attrib:h` - Hidden files
- `attrib:r` - Read-only files
- `attrib:s` - System files
- `attrib:d` - Directories only

## Advanced Usage Examples

### 1. Development File Search
```json
{
  "query": "ext:py;js;ts;json path:projects",
  "sort": "date",
  "max_results": 200
}
```

### 2. Recent Document Search
```json
{
  "query": "ext:docx;xlsx;pdf dm:thisweek",
  "sort": "date"
}
```

### 3. Large File Cleanup
```json
{
  "query": "size:>500mb !path:\"Program Files\"",
  "sort": "size"
}
```

### 4. Configuration File Hunt
```json
{
  "query": "config.* | *.conf | *.ini | settings.*",
  "path_filter": "C:\\Users\\"
}
```

### 5. Media File Organization
```json
{
  "query": "ext:mp4;avi;mkv;mp3;wav;flac",
  "sort": "size",
  "max_results": 1000
}
```

## Performance Characteristics

### Speed Benchmarks
- **Total files indexed**: ~1,000,000 files
- **Search time**: <100ms for most queries
- **Memory usage**: <50MB for Everything service
- **CPU impact**: Minimal (background indexing)

### Optimization Tips
1. **Use specific extensions** - Faster than wildcards
2. **Limit path scope** - Use path_filter for targeted searches
3. **Appropriate max_results** - Don't request more than needed
4. **Use date filters** - Reduce result set with time bounds

## Integration with Other Tools

### 1. File Operations Pipeline
```python
# Find files, then process them
python_files = await search_files(
    query="*.py path:project",
    sort="date"
)

for file in python_files:
    content = await read_file(file["path"])
    # Process content...
```

### 2. Backup Verification
```python
# Find files missing from backup
source_files = await search_files(
    query="dm:today path:Documents",
    sort="name"
)

backup_files = await search_files(
    query="path:Backup\\Documents",
    sort="name"  
)

# Compare lists to find missing files
```

### 3. Duplicate Detection
```python
# Find potential duplicates by name
duplicates = await search_files(
    query="dupe:",  # Everything's duplicate syntax
    sort="name"
)
```

## Troubleshooting

### Common Issues

#### Everything Not Found
**Error**: `es.exe not found`
**Solutions**:
1. Install Everything from voidtools.com
2. Verify path: `C:\Program Files\ES-1.1.0.30.x64\es.exe`
3. Add Everything to system PATH
4. Check if Everything service is running

#### No Results Returned
**Possible Causes**:
1. Everything database not indexed yet
2. Query syntax error
3. Path restrictions
4. File permissions

**Solutions**:
1. Wait for indexing to complete
2. Test with simple queries first
3. Check Everything application settings
4. Run as administrator if needed

#### Slow Search Performance
**Causes**:
1. Very large result sets
2. Network drives included
3. Complex regex patterns

**Solutions**:
1. Use more specific queries
2. Exclude network paths
3. Limit max_results
4. Use simpler search patterns

### Debugging Queries
Test queries directly in Everything application:
1. Open Everything
2. Enter your query
3. Verify results
4. Adjust syntax as needed

## Best Practices

### Query Construction
1. **Start specific** - Use extensions and path filters
2. **Use operators** - Combine terms effectively
3. **Test iteratively** - Build complex queries step by step
4. **Consider performance** - Balance precision with speed

### Result Handling
1. **Set appropriate limits** - Don't request excessive results
2. **Sort meaningfully** - Choose relevant sort order
3. **Filter results** - Post-process for specific needs
4. **Cache when possible** - Store results for repeated use

### Security Considerations
1. **Respect permissions** - Everything shows all accessible files
2. **Sanitize queries** - Validate user input
3. **Limit scope** - Use path filters to restrict access
4. **Audit searches** - Log sensitive file access

## Everything Application Settings

### Recommended Settings
1. **Index Options**:
   - Enable NTFS indexing
   - Include file content (if needed)
   - Exclude system files (optional)

2. **Performance**:
   - Enable service
   - Set high priority indexing
   - Exclude temporary directories

3. **Search Options**:
   - Match case (disabled)
   - Match whole word (disabled)
   - Regular expressions (enabled)
