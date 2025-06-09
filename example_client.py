#!/usr/bin/env python3
"""
Example of using Git MCP server with a GenAI API
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_git_tool(tool_name: str, arguments: dict):
    """Connect to Git MCP server and run a tool"""
    
    # Define the server connection parameters
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/lokesh/git/MCP-Servers/git-mcp/git_mcp.py"]
    )
    
    # Create client session
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools (optional)
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Call the specific tool
            result = await session.call_tool(tool_name, arguments)
            
            return result


async def main():
    """Example usage of Git MCP tools"""
    
    # Example 1: Get git status
    print("\n=== Git Status ===")
    result = await run_git_tool("git_status", {"path": "/Users/lokesh/git/MCP-Servers/git-mcp"})
    print(result.content[0].text)
    
    # Example 2: Get git log
    print("\n=== Git Log ===")
    result = await run_git_tool("git_log", {"path": "/Users/lokesh/git/MCP-Servers/git-mcp", "limit": 5})
    print(result.content[0].text)
    
    # Example 3: Get git branches
    print("\n=== Git Branches ===")
    result = await run_git_tool("git_branch", {"path": "/Users/lokesh/git/MCP-Servers/git-mcp"})
    print(result.content[0].text)


# Integration with GenAI API
def integrate_with_genai(genai_client):
    """
    Example of how to integrate with a GenAI API
    
    Args:
        genai_client: Your GenAI API client instance
    """
    
    async def git_tool_handler(tool_name: str, arguments: dict):
        """Handler that GenAI can call for Git operations"""
        result = await run_git_tool(tool_name, arguments)
        return result.content[0].text
    
    # Register Git tools with your GenAI system
    git_tools = [
        {
            "name": "git_status",
            "description": "Get git repository status",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to git repository"}
                },
                "required": ["path"]
            },
            "handler": lambda args: asyncio.run(git_tool_handler("git_status", args))
        },
        {
            "name": "git_log",
            "description": "Get git commit history",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to git repository"},
                    "limit": {"type": "integer", "description": "Number of commits", "default": 10}
                },
                "required": ["path"]
            },
            "handler": lambda args: asyncio.run(git_tool_handler("git_log", args))
        },
        {
            "name": "git_commit",
            "description": "Create a git commit",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to git repository"},
                    "message": {"type": "string", "description": "Commit message"},
                    "files": {"type": "array", "items": {"type": "string"}, "description": "Files to commit"}
                },
                "required": ["path", "message"]
            },
            "handler": lambda args: asyncio.run(git_tool_handler("git_commit", args))
        }
    ]
    
    # Register tools with your GenAI API
    # This depends on your specific GenAI API
    # Example:
    # for tool in git_tools:
    #     genai_client.register_tool(tool)
    
    return git_tools


if __name__ == "__main__":
    asyncio.run(main())