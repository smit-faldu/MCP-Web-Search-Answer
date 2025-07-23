# Contributing to MCP Web Search Answer

Thank you for your interest in contributing to MCP Web Search Answer! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A Google Gemini API key
- A SerpAPI key

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/mcp_web_search_answer.git
   cd mcp_web_search_answer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Test the setup**
   ```bash
   python main.py
   ```

## 🛠️ Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Project Structure

```
mcp_web_search_answer/
├── agents/          # LLM agents (query, answer)
├── tools/           # External tools (search)
├── langflow/        # Workflow management
├── main.py          # CLI interface
├── server.py        # Main server logic
└── README.md        # Documentation
```

### Adding New Features

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Add new functionality
   - Update documentation
   - Add tests if applicable

3. **Test your changes**
   ```bash
   python main.py
   # Test with various queries
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 🧪 Testing

### Manual Testing

Test the application with various types of queries:

- **Technical questions**: "What's new in Python 3.12?"
- **General knowledge**: "How does AI work?"
- **Current events**: "Latest news about OpenAI"
- **Complex queries**: "Best practices for web development in 2024"

### Error Testing

- Test with invalid API keys
- Test with network connectivity issues
- Test with malformed queries

## 📝 Documentation

When contributing, please:

- Update the README.md if you add new features
- Add docstrings to new functions
- Update the requirements.txt if you add dependencies
- Include examples in your documentation

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Exact steps to reproduce the bug
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**: Python version, OS, etc.
6. **Error messages**: Full error messages and stack traces

## 💡 Feature Requests

When requesting features:

1. **Use case**: Describe why this feature would be useful
2. **Description**: Detailed description of the proposed feature
3. **Examples**: Provide examples of how it would work
4. **Alternatives**: Any alternative solutions you've considered

## 🔧 Areas for Contribution

We welcome contributions in these areas:

### High Priority
- **Error handling improvements**
- **Performance optimizations**
- **Additional LLM providers** (OpenAI, Anthropic, etc.)
- **Alternative search providers** (Bing, DuckDuckGo, etc.)

### Medium Priority
- **Caching mechanisms**
- **Rate limiting improvements**
- **Configuration management**
- **Logging enhancements**

### Low Priority
- **UI improvements**
- **Additional output formats** (JSON, XML, etc.)
- **Internationalization**
- **Docker containerization**

## 📋 Pull Request Process

1. **Ensure your code follows the style guidelines**
2. **Update documentation** as needed
3. **Test your changes** thoroughly
4. **Create a clear PR description** explaining:
   - What changes you made
   - Why you made them
   - How to test them

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested manually
- [ ] Added/updated tests
- [ ] All existing tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## 📞 Getting Help

If you need help:

1. **Check the README.md** for basic setup and usage
2. **Search existing issues** for similar problems
3. **Create a new issue** with detailed information
4. **Join discussions** in existing issues and PRs

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for contributing to MCP Web Search Answer! 🚀