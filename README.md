# Git MCP Server

An MCP (Model Context Protocol) server that provides Git operations as tools for AI assistants.

## Features

The server exposes the following Git tools:

- **git_status** - Get repository status
- **git_log** - View commit history  
- **git_diff** - Show changes (staged or unstaged)
- **git_commit** - Create commits
- **git_branch** - List branches
- **git_checkout** - Switch branches

## Installation

```bash
# Clone the repository
git clone https://github.com/asklokesh/git-mcp-server.git
cd git-mcp-server

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

## Usage

### As MCP Server

Run the server directly:

```bash
python git_mcp.py
```

### With Claude Desktop

1. Edit Claude Desktop config:
   ```bash
   # macOS
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   notepad %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add configuration:
   ```json
   {
     "mcpServers": {
       "git-mcp": {
         "command": "python",
         "args": [
           "/path/to/git-mcp-server/git_mcp.py"
         ]
       }
     }
   }
   ```

3. Restart Claude Desktop

### With GenAI APIs

See the [examples directory](examples/) for integration examples:

- **[example_client.py](examples/example_client.py)** - Direct MCP client usage
- **[api_integration.py](examples/api_integration.py)** - REST API wrapper
- **[genai_integration_example.py](examples/genai_integration_example.py)** - OpenAI/Anthropic integration

Quick example:

```python
from examples.genai_integration_example import GitMCPToolkit

toolkit = GitMCPToolkit()
result = toolkit.execute_tool("git_status", {"path": "/path/to/repo"})
print(result)
```

## Tool Reference

### git_status
Get the status of a git repository.

**Parameters:**
- `path` (string, required): Path to the git repository

**Example:**
```json
{
  "tool": "git_status",
  "arguments": {
    "path": "/Users/john/my-project"
  }
}
```

### git_log
View commit history of a repository.

**Parameters:**
- `path` (string, required): Path to the git repository
- `limit` (integer, optional): Number of commits to show (default: 10)

**Example:**
```json
{
  "tool": "git_log",
  "arguments": {
    "path": "/Users/john/my-project",
    "limit": 5
  }
}
```

### git_diff
Show changes in a repository.

**Parameters:**
- `path` (string, required): Path to the git repository
- `staged` (boolean, optional): Show staged changes (default: false)

**Example:**
```json
{
  "tool": "git_diff",
  "arguments": {
    "path": "/Users/john/my-project",
    "staged": true
  }
}
```

### git_commit
Create a git commit.

**Parameters:**
- `path` (string, required): Path to the git repository
- `message` (string, required): Commit message
- `files` (array[string], optional): Specific files to commit

**Example:**
```json
{
  "tool": "git_commit",
  "arguments": {
    "path": "/Users/john/my-project",
    "message": "Fix bug in authentication",
    "files": ["auth.py", "tests/test_auth.py"]
  }
}
```

### git_branch
List branches in a repository.

**Parameters:**
- `path` (string, required): Path to the git repository

**Example:**
```json
{
  "tool": "git_branch",
  "arguments": {
    "path": "/Users/john/my-project"
  }
}
```

### git_checkout
Switch to a different branch.

**Parameters:**
- `path` (string, required): Path to the git repository
- `branch` (string, required): Branch name to checkout
- `create` (boolean, optional): Create new branch (default: false)

**Example:**
```json
{
  "tool": "git_checkout",
  "arguments": {
    "path": "/Users/john/my-project",
    "branch": "feature/new-feature",
    "create": true
  }
}
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=git_mcp --cov-report=html
```

### Project Structure

```
git-mcp-server/
├── git_mcp.py              # Main MCP server
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Package configuration
├── tests/                 # Unit tests
│   ├── __init__.py
│   └── test_git_mcp.py
├── examples/              # Integration examples
│   ├── example_client.py
│   ├── api_integration.py
│   ├── genai_integration_example.py
│   └── ...
└── .github/
    └── workflows/
        └── test.yml       # CI/CD pipeline
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/asklokesh/git-mcp-server/issues).
