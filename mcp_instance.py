"""
Shared FastMCP instance.

Tool/resource modules import `mcp` from here (instead of from `server.py`) to
avoid circular imports: server.py imports the tool modules for their
registration side effects, so the tool modules can't import back from server.py.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("supermarket-products-tools", stateless_http=True)
