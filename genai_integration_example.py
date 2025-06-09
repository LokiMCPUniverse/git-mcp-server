#!/usr/bin/env python3
"""
Example integration with various GenAI APIs (OpenAI, Anthropic, Google, etc.)
"""

import asyncio
import json
from typing import Dict, Any, List
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class GitMCPToolkit:
    """Toolkit for integrating Git MCP with GenAI APIs"""
    
    def __init__(self, mcp_server_path: str = "/Users/lokesh/git/MCP-Servers/git-mcp/git_mcp.py"):
        self.server_path = mcp_server_path
        self.tools = self._define_tools()
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define Git tools in OpenAI function calling format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "git_status",
                    "description": "Get the status of a git repository",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the git repository"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_log",
                    "description": "Get commit history of a git repository",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the git repository"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of commits to show",
                                "default": 10
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_diff",
                    "description": "Show changes in a git repository",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the git repository"
                            },
                            "staged": {
                                "type": "boolean",
                                "description": "Show staged changes",
                                "default": False
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_commit",
                    "description": "Create a git commit",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the git repository"
                            },
                            "message": {
                                "type": "string",
                                "description": "Commit message"
                            },
                            "files": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific files to commit"
                            }
                        },
                        "required": ["path", "message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_branch",
                    "description": "List branches in a git repository",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the git repository"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "git_checkout",
                    "description": "Checkout a git branch",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the git repository"
                            },
                            "branch": {
                                "type": "string",
                                "description": "Branch name to checkout"
                            },
                            "create": {
                                "type": "boolean",
                                "description": "Create new branch",
                                "default": False
                            }
                        },
                        "required": ["path", "branch"]
                    }
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Call a Git MCP tool and return the result"""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_path]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text
    
    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Synchronous wrapper for calling tools"""
        return asyncio.run(self.call_tool(tool_name, arguments))


# Example: OpenAI Integration
def openai_example():
    """Example of using Git MCP with OpenAI"""
    from openai import OpenAI
    
    client = OpenAI()
    toolkit = GitMCPToolkit()
    
    # Chat with function calling
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "What's the status of the git repository at /Users/lokesh/git/MCP-Servers/git-mcp?"}
        ],
        tools=toolkit.tools,
        tool_choice="auto"
    )
    
    # Process tool calls
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            # Execute the Git MCP tool
            result = toolkit.execute_tool(function_name, arguments)
            
            # Send result back to OpenAI
            follow_up = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": "What's the status of the git repository?"},
                    response.choices[0].message,
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    }
                ]
            )
            
            print(follow_up.choices[0].message.content)


# Example: Anthropic Integration
def anthropic_example():
    """Example of using Git MCP with Anthropic"""
    import anthropic
    
    client = anthropic.Anthropic()
    toolkit = GitMCPToolkit()
    
    # Convert tools to Anthropic format
    anthropic_tools = [
        {
            "name": tool["function"]["name"],
            "description": tool["function"]["description"],
            "input_schema": tool["function"]["parameters"]
        }
        for tool in toolkit.tools
    ]
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        messages=[
            {"role": "user", "content": "Check the git status of /Users/lokesh/git/MCP-Servers/git-mcp"}
        ],
        tools=anthropic_tools,
        max_tokens=1000
    )
    
    # Process tool use
    for content in response.content:
        if content.type == "tool_use":
            result = toolkit.execute_tool(content.name, content.input)
            print(f"Tool result: {result}")


# Example: Direct function calls for any GenAI
def generic_genai_example():
    """Example for any GenAI that supports function/tool calling"""
    toolkit = GitMCPToolkit()
    
    # Your GenAI API call would return something like:
    # tool_name = "git_status"
    # tool_args = {"path": "/Users/lokesh/git/MCP-Servers/git-mcp"}
    
    # Execute the tool
    result = toolkit.execute_tool("git_status", {"path": "/Users/lokesh/git/MCP-Servers/git-mcp"})
    print(f"Git status result: {result}")
    
    # Use the result in your GenAI response
    # ...


if __name__ == "__main__":
    # Test the toolkit
    toolkit = GitMCPToolkit()
    
    # Example: Get git status
    print("Testing git_status...")
    result = toolkit.execute_tool("git_status", {"path": "/Users/lokesh/git/MCP-Servers/git-mcp"})
    print(result)
    
    # Example: Get git log
    print("\nTesting git_log...")
    result = toolkit.execute_tool("git_log", {"path": "/Users/lokesh/git/MCP-Servers/git-mcp", "limit": 3})
    print(result)