#!/usr/bin/env python3

import pytest
import json
import tempfile
import os
import shutil
from git import Repo
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from git_mcp import (
    GitStatusArgs, GitLogArgs, GitDiffArgs, GitCommitArgs,
    GitBranchArgs, GitCheckoutArgs, handle_list_tools, handle_call_tool
)


class TestGitMCP:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.test_dir = tempfile.mkdtemp()
        self.repo = Repo.init(self.test_dir)
        
        # Create initial commit
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Initial content")
        self.repo.index.add(["test.txt"])
        self.repo.index.commit("Initial commit")
        
        yield
        
        shutil.rmtree(self.test_dir)
    
    def test_args_models(self):
        """Test argument model validation"""
        # Test GitStatusArgs
        args = GitStatusArgs(path="/tmp/repo")
        assert args.path == "/tmp/repo"
        
        # Test GitLogArgs with defaults
        args = GitLogArgs(path="/tmp/repo")
        assert args.limit == 10
        
        # Test GitDiffArgs
        args = GitDiffArgs(path="/tmp/repo", staged=True)
        assert args.staged is True
        
        # Test GitCommitArgs
        args = GitCommitArgs(path="/tmp/repo", message="Test commit", files=["file1.txt"])
        assert len(args.files) == 1
    
    @pytest.mark.asyncio
    async def test_handle_list_tools(self):
        """Test listing available tools"""
        tools = await handle_list_tools()
        assert len(tools) == 6
        
        tool_names = [tool.name for tool in tools]
        expected_tools = ["git_status", "git_log", "git_diff", "git_commit", "git_branch", "git_checkout"]
        for expected in expected_tools:
            assert expected in tool_names
    
    @pytest.mark.asyncio
    async def test_git_status(self):
        """Test git status functionality"""
        result = await handle_call_tool("git_status", {"path": self.test_dir})
        assert len(result) == 1
        assert result[0].type == "text"
        assert "nothing to commit" in result[0].text.lower()
    
    @pytest.mark.asyncio
    async def test_git_log(self):
        """Test git log functionality"""
        result = await handle_call_tool("git_log", {"path": self.test_dir, "limit": 5})
        assert len(result) == 1
        
        commits = json.loads(result[0].text)
        assert len(commits) == 1
        assert commits[0]["message"] == "Initial commit"
    
    @pytest.mark.asyncio
    async def test_git_branch(self):
        """Test git branch functionality"""
        result = await handle_call_tool("git_branch", {"path": self.test_dir})
        assert len(result) == 1
        
        branches = json.loads(result[0].text)
        assert any(b["name"] == "master" or b["name"] == "main" for b in branches)
        assert any(b["current"] for b in branches)
    
    @pytest.mark.asyncio
    async def test_git_diff(self):
        """Test git diff functionality"""
        # Modify file
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "a") as f:
            f.write("\nModified content")
        
        result = await handle_call_tool("git_diff", {"path": self.test_dir})
        assert len(result) == 1
        assert "Modified content" in result[0].text
    
    @pytest.mark.asyncio
    async def test_git_commit(self):
        """Test git commit functionality"""
        # Create new file
        new_file = os.path.join(self.test_dir, "new.txt")
        with open(new_file, "w") as f:
            f.write("New file content")
        
        self.repo.index.add(["new.txt"])
        
        result = await handle_call_tool("git_commit", {
            "path": self.test_dir,
            "message": "Test commit from unit test"
        })
        
        assert len(result) == 1
        assert "Commit created:" in result[0].text
        
        # Verify commit was created
        commits = list(self.repo.iter_commits())
        assert len(commits) == 2
        assert commits[0].message.strip() == "Test commit from unit test"
    
    @pytest.mark.asyncio
    async def test_git_checkout(self):
        """Test git checkout functionality"""
        # Create new branch
        result = await handle_call_tool("git_checkout", {
            "path": self.test_dir,
            "branch": "test-branch",
            "create": True
        })
        
        assert len(result) == 1
        assert "Checked out branch: test-branch" in result[0].text
        
        # Verify branch was created and checked out
        assert self.repo.active_branch.name == "test-branch"
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling for invalid operations"""
        # Test with non-existent repository
        result = await handle_call_tool("git_status", {"path": "/non/existent/path"})
        assert len(result) == 1
        assert "Error:" in result[0].text
        
        # Test unknown tool
        result = await handle_call_tool("unknown_tool", {})
        assert len(result) == 1
        assert "Error:" in result[0].text