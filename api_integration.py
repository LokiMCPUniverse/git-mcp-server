#!/usr/bin/env python3
"""
REST API wrapper for Git MCP Server
Provides HTTP endpoints for Git operations
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

app = FastAPI(title="Git MCP API", version="0.1.0")

# Request models
class GitStatusRequest(BaseModel):
    path: str

class GitLogRequest(BaseModel):
    path: str
    limit: Optional[int] = 10

class GitDiffRequest(BaseModel):
    path: str
    staged: Optional[bool] = False

class GitCommitRequest(BaseModel):
    path: str
    message: str
    files: Optional[List[str]] = None

class GitBranchRequest(BaseModel):
    path: str

class GitCheckoutRequest(BaseModel):
    path: str
    branch: str
    create: Optional[bool] = False


async def call_git_tool(tool_name: str, arguments: dict):
    """Call Git MCP server tool"""
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/lokesh/git/MCP-Servers/git-mcp/git_mcp.py"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return {"success": True, "data": result.content[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """API information"""
    return {
        "name": "Git MCP API",
        "version": "0.1.0",
        "endpoints": [
            "/git/status",
            "/git/log",
            "/git/diff",
            "/git/commit",
            "/git/branch",
            "/git/checkout"
        ]
    }


@app.post("/git/status")
async def git_status(request: GitStatusRequest):
    """Get git repository status"""
    return await call_git_tool("git_status", request.dict())


@app.post("/git/log")
async def git_log(request: GitLogRequest):
    """Get git commit history"""
    return await call_git_tool("git_log", request.dict())


@app.post("/git/diff")
async def git_diff(request: GitDiffRequest):
    """Show git diff"""
    return await call_git_tool("git_diff", request.dict())


@app.post("/git/commit")
async def git_commit(request: GitCommitRequest):
    """Create a git commit"""
    return await call_git_tool("git_commit", request.dict())


@app.post("/git/branch")
async def git_branch(request: GitBranchRequest):
    """List git branches"""
    return await call_git_tool("git_branch", request.dict())


@app.post("/git/checkout")
async def git_checkout(request: GitCheckoutRequest):
    """Checkout a git branch"""
    return await call_git_tool("git_checkout", request.dict())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)