# AI-Tools Summary

## Table of Contents

- [AI-Tools Summary](#ai-tools-summary)
  - [File Operations](#file-operations)
  - [Document Creation & Reading](#document-creation-&-reading)
  - [Web & Network](#web-&-network)
  - [Database (SQLite)](#database-(sqlite))
  - [Communication](#communication)
  - [Utilities](#utilities)
  - [Recommendations for ComfyUI Development](#recommendations-for-comfyui-development)

# AI-Tools Summary

A comprehensive overview of available ai-tools organized by category.

---

## File Operations

| Tool | Best For |
|------|----------|
| `list_files` | Directory listings, exploring folder structures |
| `read_file` | Reading text/code files |
| `write_file` | Creating/overwriting any text file |
| `search_files` | Finding files by name/pattern (uses Everything on Windows for speed) or searching file contents |

---

## Document Creation & Reading

| Tool | Best For |
|------|----------|
| `write_markdown` | Reports, documentation with optional TOC |
| `write_csv` | Structured data export, spreadsheet-compatible |
| `write_json` | Config files, data interchange |
| `write_pdf` | Formatted documents for distribution |
| `write_word` | .docx files with paragraphs/headers |
| `write_excel` | Spreadsheets with formatting, auto-width columns |
| `read_excel` | Extracting data from .xlsx/.xls files |

---

## Web & Network

| Tool | Best For |
|------|----------|
| `web_search` | Google searches via Serper API (organic results, knowledge graph) |
| `http_request` | API calls (GET/POST/etc), supports auth, headers, JSON |
| `download_file` | Fetching files from URLs with progress tracking |
| `advanced_web_scraper` | Extracting article text, handling paywalls, academic sites |
| `open_browser` | Launching URLs in your default browser |
| `open_search` | Opening a search query directly in browser |

---

## Database (SQLite)

| Tool | Best For |
|------|----------|
| `sqlite_query` | SELECT/INSERT/UPDATE/DELETE on .db files |
| `database_info` | Inspecting table schemas and structure |
| `create_table` | Setting up new tables with typed columns |

---

## Communication

| Tool | Best For |
|------|----------|
| `send_email` | SMTP email delivery |
| `slack_message` | Posting to Slack channels/users |
| `discord_webhook` | Sending Discord messages via webhook |
| `teams_webhook` | Microsoft Teams notifications |

---

## Utilities

| Tool | Best For |
|------|----------|
| `clean_text` | Stripping problematic Unicode before file writes |
| `clipboard` | Copy/paste operations, clipboard history |
| `manage_calendar` | Creating/listing/updating calendar events |

---

## Recommendations for ComfyUI Development

For ComfyUI custom node work, the most relevant tools are:

- **`read_file` / `write_file`** — Editing Python node code
- **`search_files`** — Quickly finding nodes or configs across multiple installations
- **`read_excel` / `write_csv`** — Tracking node metadata or test results
- **`http_request`** — Hitting APIs like LM Studio endpoints
- **`write_json`** — Creating or updating node configuration files

---

*Generated: December 2024*