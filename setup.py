"""
Setup script for MCP Web Search Answer
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="mcp-web-search-answer",
    version="1.0.0",
    author="MCP Web Search Answer Team",
    author_email="your-email@example.com",
    description="A minimal working Python application using OpenAI's Model Context Protocol (MCP) with web search capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp_web_search_answer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docker": [
            "gunicorn>=21.0.0",
            "uvicorn[standard]>=0.23.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-web-search=main:main",
            "mcp-server=server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.txt", "*.md"],
    },
    keywords="mcp model-context-protocol ai llm web-search gemini langchain langgraph",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mcp_web_search_answer/issues",
        "Source": "https://github.com/yourusername/mcp_web_search_answer",
        "Documentation": "https://github.com/yourusername/mcp_web_search_answer#readme",
    },
)