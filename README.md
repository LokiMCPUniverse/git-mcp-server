# Git MCP Server

An MCP (Model Context Protocol) server that provides Git operations as tools for AI assistants.

## Features

The server exposes the following Git tools:

- `git_status` - Get repository status
- `git_log` - View commit history
- `git_diff` - Show changes (staged or unstaged)
- `git_commit` - Create commits
- `git_branch` - List branches
- `git_checkout` - Switch branches

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the server directly:

```bash
python git_mcp.py
```

Or install as a package:

```bash
pip install -e .
git-mcp
```

## Tool Inputs

### git_status
- `path` (string): Path to the git repository

### git_log
- `path` (string): Path to the git repository
- `limit` (number, optional): Number of commits to show (default: 10)

### git_diff
- `path` (string): Path to the git repository
- `staged` (boolean, optional): Show staged changes (default: false)

### git_commit
- `path` (string): Path to the git repository
- `message` (string): Commit message
- `files` (array of strings, optional): Specific files to commit

### git_branch
- `path` (string): Path to the git repository

### git_checkout
- `path` (string): Path to the git repository
- `branch` (string): Branch name to checkout
- `create` (boolean, optional): Create new branch (default: false)

## License

MIT