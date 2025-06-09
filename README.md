# Git MCP Server

[![Tests](https://github.com/asklokesh/git-mcp-server/actions/workflows/test.yml/badge.svg)](https://github.com/asklokesh/git-mcp-server/actions/workflows/test.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green)](https://modelcontextprotocol.io)
[![Code Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen.svg)](https://github.com/asklokesh/git-mcp-server)

A Model Context Protocol (MCP) server that provides Git operations as tools for AI assistants. This server enables seamless integration of Git functionality into AI workflows.

## Why Git MCP Server?

- **AI-Native Git Integration** - Enable AI assistants to manage Git repositories with natural language
- **Full Git Toolkit** - Status, commits, branches, diffs, and more - all accessible to AI
- **Zero Configuration** - Works out of the box with any Git repository
- **Universal Compatibility** - Integrates with Claude Desktop, OpenAI, Anthropic APIs, and any MCP-compatible client
- **Async Performance** - Built on Python's asyncio for optimal performance
- **Battle-Tested** - 93% code coverage with comprehensive test suite

## Features

Transform your AI assistant into a Git power user with these tools:

| Tool | Description | Use Case |
|------|-------------|----------|
| **git_status** | Get repository status | "What files have I changed?" |
| **git_log** | View commit history | "Show me the last 5 commits" |
| **git_diff** | Show changes | "What did I modify in auth.py?" |
| **git_commit** | Create commits | "Commit my bug fix with a descriptive message" |
| **git_branch** | List branches | "What branches exist?" |
| **git_checkout** | Switch branches | "Switch to the feature branch" |

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/asklokesh/git-mcp-server.git
cd git-mcp-server

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### See It In Action

```python
# Ask your AI assistant:
"What's the status of my project?"
"Show me what changed in the authentication module"
"Create a commit for the bug fix I just made"
"Switch to the development branch"
```

## Usage

### Option 1: With Claude Desktop (Recommended)

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

### Option 2: As Standalone MCP Server

```bash
python git_mcp.py
```

### Option 3: With GenAI APIs (OpenAI, Anthropic, etc.)

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

## Real-World Examples

### Example 1: AI-Powered Code Review
```python
# Ask your AI assistant:
"Check the git status and tell me what files need to be committed"
"Show me the diff for the changes in the API module"
"Create a descriptive commit message based on the changes"
```

### Example 2: Branch Management
```python
# Ask your AI assistant:
"List all branches and tell me which one is active"
"Create a new feature branch for the authentication update"
"Switch to the main branch and show me the latest commits"
```

### Example 3: Project Health Check
```python
# Ask your AI assistant:
"Analyze the last 10 commits and summarize the recent changes"
"Check if there are any uncommitted changes"
"Show me who contributed to this project recently"
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

We love contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Ways to Contribute

- **Report bugs** - Help us identify issues
- **Suggest features** - Share your ideas
- **Improve documentation** - Help others understand the project
- **Add tests** - Increase code coverage
- **Translate** - Make the project accessible globally

## Roadmap

- [ ] Add support for more Git operations (merge, rebase, stash)
- [ ] Implement Git LFS support
- [ ] Add authentication for private repositories
- [ ] Create a web-based dashboard
- [ ] Support for Git hooks integration
- [ ] Multi-repository management
- [ ] Git workflow automation templates

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support & Community

- **Issues**: [GitHub Issue Tracker](https://github.com/asklokesh/git-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/asklokesh/git-mcp-server/discussions)
- **Star this repo** to show your support!

---

<p align="center">
  Made with care by developers, for developers
  <br>
  <a href="https://github.com/asklokesh/git-mcp-server/stargazers">Star us on GitHub</a>
</p>
