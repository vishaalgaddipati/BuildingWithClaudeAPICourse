# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Python package implementing document-related tools (conversion, processing) exposed through an MCP (Model Context Protocol) server, for use by AI assistants.

## Setup & commands

```bash
# Create a virtual env and activate it
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the package in development mode
uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test file / test
uv run pytest tests/test_document.py
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

Note: `uv` resolves the venv via the `VIRTUAL_ENV` env var if set, which can point at a *different* project's `.venv` in a multi-project shell session. If `uv pip install`/`uv run` reports installing into an unexpected path, `unset VIRTUAL_ENV` first.

## Architecture

- `main.py` — MCP server entrypoint. Creates the `FastMCP` server instance and registers tool functions with it. This is the only place tools get wired up; defining a function in `tools/` does not expose it until it's registered here.
- `tools/` — plain Python functions implementing tool logic, decoupled from MCP registration. Each function is independently unit-testable without an MCP server running.
  - `tools/math.py` — arithmetic tools (e.g. `add`).
  - `tools/document.py` — document conversion tools (e.g. `binary_document_to_markdown`, which wraps `markitdown` to convert binary DOCX/PDF/etc. data to markdown text via `MarkItDown().convert()` with a `StreamInfo` for the file extension).
- `tests/` — pytest tests against the `tools/` functions directly (not through MCP). `tests/fixtures/` holds binary sample files (`.docx`, `.pdf`) used by document conversion tests.

## Defining MCP tools

Tools are plain Python functions, registered with the MCP server separately in `main.py`:

```python
mcp.tool()(my_function)
```

Tool docstrings double as the tool description shown to the LLM, so they must be written for that audience. Docstrings should:

- Begin with a one-line summary
- Provide a detailed explanation of functionality
- Explain when to use (and not use) the tool
- Include usage examples with expected input/output (see `tools/math.py:add` for the pattern: a "When to use" section plus `>>>` doctest-style examples)

Parameters must use `pydantic.Field` for their descriptions, since these also surface to the LLM:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """Comprehensive docstring here"""
    # Implementation
```

New tool functions should live in `tools/` (grouped by domain, e.g. `math.py`, `document.py`) and must be explicitly registered in `main.py` via `mcp.tool()(...)` to actually be exposed by the server.

Always type-annotate function arguments and return values. FastMCP derives the tool's input schema from these annotations, so missing or wrong types produce an incorrect schema for the LLM, not just a static-analysis warning.
