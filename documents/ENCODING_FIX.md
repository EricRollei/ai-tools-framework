# AI Tools Framework - Encoding Fix Documentation

## Problem Fixed
LM Studio was encountering UTF-8 encoding errors when writing files with special Unicode characters like:
- Em dashes (—)
- Smart quotes (" ")  
- Bullets (•)
- Greek letters (β, α, γ)
- Micro symbols (µ)
- Non-breaking spaces
- Emoji characters

## Solution Implemented

### 1. Enhanced `write_file` Tool
- **Automatic content cleaning** - Removes problematic Unicode characters
- **Fallback encoding** - Uses safe encoding options if UTF-8 fails
- **Character replacement** - Converts special chars to ASCII equivalents:
  - `—` → `-` (em dash to hyphen)
  - `"` → `"` (smart quotes to straight quotes)
  - `•` → `*` (bullet to asterisk)
  - `µ` → `u` (micro to 'u')

### 2. New `clean_text` Tool
- **Pre-cleaning text** - Clean problematic content before use
- **Encoding validation** - Checks if text can be safely encoded
- **Statistics** - Reports what was changed
- **ASCII mode** - Optional strict ASCII-only output

## Usage in LM Studio

### For Regular File Writing:
The `write_file` tool now automatically handles encoding issues. Just use it normally:

```
Use the write_file tool with any content - it will automatically clean problematic characters.
```

### For Text Pre-processing:
Use the `clean_text` tool to preview what will be cleaned:

```
Use the clean_text tool to see how text will be processed before writing to file.
```

## Tools Now Available:
1. **web_search** - Web search via Serper.dev
2. **list_files** - Directory listing  
3. **read_file** - File reading
4. **write_file** - File writing (now encoding-safe)
5. **clean_text** - Text cleaning and validation

All tools are now robust and handle encoding issues gracefully!
