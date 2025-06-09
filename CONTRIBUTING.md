# Contributing to Git MCP Server

First off, thank you for considering contributing to Git MCP Server! It's people like you that make Git MCP Server such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include logs and error messages**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these `beginner` and `help-wanted` issues:

* [Beginner issues](https://github.com/asklokesh/git-mcp-server/labels/beginner) - issues which should only require a few lines of code
* [Help wanted issues](https://github.com/asklokesh/git-mcp-server/labels/help%20wanted) - issues which should be a bit more involved

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code follows the existing style.
6. Issue that pull request!

## Development Process

1. **Setup your environment**
   ```bash
   git clone https://github.com/asklokesh/git-mcp-server.git
   cd git-mcp-server
   pip install -r requirements.txt
   pip install pytest pytest-asyncio pytest-cov
   ```

2. **Make your changes**
   * Write your code
   * Add tests for new functionality
   * Update documentation as needed

3. **Run tests**
   ```bash
   python -m pytest tests/ -v --cov=git_mcp
   ```

4. **Submit your PR**
   * Create a descriptive pull request
   * Link any relevant issues
   * Wait for review and address feedback

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Styleguide

* Follow PEP 8
* Use meaningful variable names
* Add docstrings to all functions and classes
* Keep functions focused and small
* Use type hints where appropriate

### Documentation Styleguide

* Use Markdown
* Reference functions and classes in backticks
* Include code examples where helpful
* Keep explanations clear and concise

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested

## Recognition

Contributors will be recognized in our README and release notes. We appreciate every contribution, no matter how small!

Thank you for contributing!