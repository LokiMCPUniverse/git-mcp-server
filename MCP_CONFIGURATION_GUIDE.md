# MCP Server Configuration Guide

## Overview
The Model Context Protocol (MCP) is a standardized protocol by Anthropic that allows Claude Desktop to connect with external tools and services through a uniform interface.

## Configuration File Location
The Claude Desktop configuration file `claude_desktop_config.json` is located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

## Configuration Structure
The configuration file uses JSON format with an `mcpServers` object containing server configurations:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["array", "of", "arguments"],
      "env": {
        "OPTIONAL_ENV_VAR": "value"
      }
    }
  }
}
```

## Example Configurations for git-mcp

### Option 1: Direct Python Execution
```json
{
  "mcpServers": {
    "git-mcp": {
      "command": "python",
      "args": [
        "/Users/lokesh/git/MCP-Servers/git-mcp/git_mcp.py"
      ]
    }
  }
}
```

### Option 2: Using UV (Python Package Manager)
```json
{
  "mcpServers": {
    "git-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/lokesh/git/MCP-Servers/git-mcp",
        "run",
        "git_mcp.py"
      ]
    }
  }
}
```

### Option 3: After Installing as Package
```json
{
  "mcpServers": {
    "git-mcp": {
      "command": "git-mcp"
    }
  }
}
```

## Setting Up the Configuration

1. **Create/Edit the Configuration File**:
   ```bash
   # On macOS
   mkdir -p ~/Library/Application\ Support/Claude
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Copy one of the example configurations above** and paste it into the file

3. **Save the file** and restart Claude Desktop

4. **Verify the Connection**:
   - Open Claude Desktop
   - Look for the MCP icon (puzzle piece) in the text input area
   - Click it to see available tools from your git-mcp server

## Available Git Tools
Once configured, Claude will have access to these Git operations:
- `git_status` - Check repository status
- `git_log` - View commit history
- `git_diff` - Show changes
- `git_commit` - Create commits
- `git_branch` - List branches
- `git_checkout` - Switch branches

## Troubleshooting

1. **Server Not Showing Up**:
   - Ensure Claude Desktop is completely closed and restarted
   - Check that the path to git_mcp.py is absolute and correct
   - Verify Python is installed and accessible from terminal

2. **Permission Issues**:
   - Make sure git_mcp.py has execute permissions:
     ```bash
     chmod +x /Users/lokesh/git/MCP-Servers/git-mcp/git_mcp.py
     ```

3. **View Logs**:
   - Check Claude Desktop developer console for error messages
   - In Claude Desktop: Menu → Settings → Developer → Open DevTools

## Multiple Server Configuration
You can configure multiple MCP servers:

```json
{
  "mcpServers": {
    "git-mcp": {
      "command": "python",
      "args": ["/Users/lokesh/git/MCP-Servers/git-mcp/git_mcp.py"]
    },
    "another-server": {
      "command": "node",
      "args": ["/path/to/another/server.js"]
    }
  }
}
```

## Security Considerations
- MCP servers have access to your system based on their implementation
- Only use trusted MCP servers
- Review the server code before configuring it
- Be cautious with servers that require API keys or credentials