# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Added
- Initial release of MCP Web Search Answer
- Google Gemini 2.5 Flash integration via LangChain
- SerpAPI web search functionality
- LangGraph workflow management
- FastMCP orchestration support
- Interactive CLI interface (`main.py`)
- Server-based processing (`server.py`)
- Comprehensive documentation and setup guides
- GitHub Actions CI/CD pipeline
- Security scanning and code quality checks
- Issue and PR templates
- MIT License

### Features
- **Query Agent**: Converts natural language to search queries
- **Search Tool**: Real-time web search via SerpAPI
- **Answer Agent**: Synthesizes search results into concise answers
- **Workflow Management**: LangGraph-based flow control
- **Error Handling**: Graceful error handling and fallbacks
- **Environment Configuration**: Secure API key management

### Technical Details
- Python 3.8+ support
- MCP (Model Context Protocol) compliance
- LangChain integration for prompt management
- Type hints and comprehensive documentation
- Modular architecture for easy extension

### Documentation
- Comprehensive README with setup instructions
- Contributing guidelines
- Code of conduct
- API documentation
- Example usage and demos

### Security
- Environment variable-based API key storage
- No hardcoded secrets
- Input validation and sanitization
- Security scanning in CI pipeline