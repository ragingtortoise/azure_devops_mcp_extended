"""
MCP Server entry point: python -m devops_extended.mcp
"""

from .mcp_server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
