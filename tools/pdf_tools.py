# tools/pdf_tools.py
"""
PDF creation tools - requires reportlab
Note: Install with: pip install reportlab
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from core.base import BaseTool, ToolDefinition, ToolParameter, ToolResult, ToolResultType
from core.registry import registry

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class PDFWriteTool(BaseTool):
    """Write PDF documents - creates new or overwrites existing (requires reportlab)"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="write_pdf",
            description="Write a PDF document with formatted text - creates new or overwrites existing (requires reportlab library)",
            category="document_creation",
            parameters=[
                ToolParameter(
                    name="file_path",
                    description="Path to the PDF file to create",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="title",
                    description="Document title",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="content",
                    description="Document content (supports basic formatting)",
                    param_type="string",
                    required=True
                ),
                ToolParameter(
                    name="author",
                    description="Document author",
                    param_type="string",
                    required=False
                ),
                ToolParameter(
                    name="page_size",
                    description="Page size (letter or A4)",
                    param_type="string",
                    required=False,
                    default="letter"
                )
            ]
        )
    
    async def execute(self, file_path: str, title: str, content: str, 
                     author: Optional[str] = None, page_size: str = "letter") -> ToolResult:
        """Write PDF document - creates new or overwrites existing file"""
        try:
            if not REPORTLAB_AVAILABLE:
                return ToolResult(
                    success=False,
                    result_type=ToolResultType.ERROR,
                    content="PDF writing requires reportlab library. Install with: pip install reportlab",
                    error_message="reportlab library not available"
                )
            
            target_file = Path(file_path)
            if not target_file.suffix:
                target_file = target_file.with_suffix('.pdf')
            
            # Ensure parent directory exists
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists (for informative message)
            file_existed = target_file.exists()
            
            # Set page size
            pagesize = A4 if page_size.lower() == "a4" else letter
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(target_file),
                pagesize=pagesize,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Get styles
            styles = getSampleStyleSheet()
            story = []
            
            # Add title
            title_style = styles['Heading1']
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 12))
            
            # Add author if provided
            if author:
                author_style = styles['Normal']
                story.append(Paragraph(f"<b>Author:</b> {author}", author_style))
                story.append(Spacer(1, 12))
            
            # Add content (split by paragraphs)
            normal_style = styles['Normal']
            paragraphs = content.split('\n\n')
            
            for para in paragraphs:
                if para.strip():
                    # Simple formatting support
                    formatted_para = para.strip()
                    story.append(Paragraph(formatted_para, normal_style))
                    story.append(Spacer(1, 6))
            
            # Build PDF
            doc.build(story)
            
            # Create appropriate success message
            action = "overwrote" if file_existed else "created"
            
            return ToolResult(
                success=True,
                content=f"Successfully {action} PDF file: {target_file}",
                result_type=ToolResultType.TEXT,
                metadata={
                    "tool": "write_pdf",
                    "file_path": str(target_file),
                    "title": title,
                    "page_size": page_size,
                    "author": author,
                    "action": action
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result_type=ToolResultType.ERROR,
                content=f"Error creating PDF file: {str(e)}",
                error_message=f"Error creating PDF file: {str(e)}"
            )

# Only register if reportlab is available
if REPORTLAB_AVAILABLE:
    registry.register(PDFWriteTool)
