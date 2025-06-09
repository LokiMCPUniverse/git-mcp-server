#!/usr/bin/env python3

import asyncio
import json
from typing import Optional, List
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from git import Repo
from pydantic import BaseModel, Field


class GitStatusArgs(BaseModel):
    path: str = Field(description="Path to the git repository")


class GitLogArgs(BaseModel):
    path: str = Field(description="Path to the git repository")
    limit: Optional[int] = Field(default=10, description="Number of commits to show")


class GitDiffArgs(BaseModel):
    path: str = Field(description="Path to the git repository")
    staged: Optional[bool] = Field(default=False, description="Show staged changes")


class GitCommitArgs(BaseModel):
    path: str = Field(description="Path to the git repository")
    message: str = Field(description="Commit message")
    files: Optional[List[str]] = Field(default=None, description="Specific files to commit")


class GitBranchArgs(BaseModel):
    path: str = Field(description="Path to the git repository")


class GitCheckoutArgs(BaseModel):
    path: str = Field(description="Path to the git repository")
    branch: str = Field(description="Branch name to checkout")
    create: Optional[bool] = Field(default=False, description="Create new branch")


server = Server("git-mcp")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="git_status",
            description="Get git repository status",
            inputSchema=GitStatusArgs.model_json_schema(),
        ),
        types.Tool(
            name="git_log",
            description="Get git commit history",
            inputSchema=GitLogArgs.model_json_schema(),
        ),
        types.Tool(
            name="git_diff",
            description="Show git diff",
            inputSchema=GitDiffArgs.model_json_schema(),
        ),
        types.Tool(
            name="git_commit",
            description="Create a git commit",
            inputSchema=GitCommitArgs.model_json_schema(),
        ),
        types.Tool(
            name="git_branch",
            description="List git branches",
            inputSchema=GitBranchArgs.model_json_schema(),
        ),
        types.Tool(
            name="git_checkout",
            description="Checkout a git branch",
            inputSchema=GitCheckoutArgs.model_json_schema(),
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        if name == "git_status":
            args = GitStatusArgs(**arguments)
            repo = Repo(args.path)
            status = repo.git.status()
            
            return [types.TextContent(type="text", text=status)]
        
        elif name == "git_log":
            args = GitLogArgs(**arguments)
            repo = Repo(args.path)
            
            commits = []
            for commit in repo.iter_commits(max_count=args.limit):
                commits.append({
                    "hash": commit.hexsha,
                    "author": str(commit.author),
                    "date": commit.committed_datetime.isoformat(),
                    "message": commit.message.strip(),
                })
            
            return [types.TextContent(type="text", text=json.dumps(commits, indent=2))]
        
        elif name == "git_diff":
            args = GitDiffArgs(**arguments)
            repo = Repo(args.path)
            
            if args.staged:
                diff = repo.git.diff("--staged")
            else:
                diff = repo.git.diff()
            
            return [types.TextContent(type="text", text=diff or "No changes")]
        
        elif name == "git_commit":
            args = GitCommitArgs(**arguments)
            repo = Repo(args.path)
            
            if args.files:
                repo.index.add(args.files)
            
            commit = repo.index.commit(args.message)
            
            return [types.TextContent(type="text", text=f"Commit created: {commit.hexsha}")]
        
        elif name == "git_branch":
            args = GitBranchArgs(**arguments)
            repo = Repo(args.path)
            
            branches = []
            for branch in repo.branches:
                branches.append({
                    "name": branch.name,
                    "current": branch == repo.active_branch,
                })
            
            return [types.TextContent(type="text", text=json.dumps(branches, indent=2))]
        
        elif name == "git_checkout":
            args = GitCheckoutArgs(**arguments)
            repo = Repo(args.path)
            
            if args.create:
                new_branch = repo.create_head(args.branch)
                new_branch.checkout()
            else:
                repo.git.checkout(args.branch)
            
            return [types.TextContent(type="text", text=f"Checked out branch: {args.branch}")]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="git-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())