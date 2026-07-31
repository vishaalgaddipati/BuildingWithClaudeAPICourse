from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to a PDF or DOCX file to convert to markdown"),
) -> str:
    """Converts a PDF or DOCX file at the given path to markdown-formatted text.

    Reads the document at the specified file path and converts its contents
    into a markdown string, preserving structural elements such as headings,
    lists, and emphasis where present in the source document.

    When to use:
    - When you have a local file path to a PDF or DOCX document and need its
      contents as markdown text
    - When you want to extract and read the textual content of a document
      already saved on disk

    When not to use:
    - When you only have the document's raw binary data (not a path on disk)
      — use `binary_document_to_markdown` instead

    Examples:
    >>> document_path_to_markdown("tests/fixtures/mcp_docs.pdf")
    '# MCP Docs\\n\\n...'
    """
    md = MarkItDown()
    result = md.convert(file_path)
    return result.text_content
