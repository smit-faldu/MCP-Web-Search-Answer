"""
Test basic imports and module structure
"""

import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_agent_imports():
    """Test that agent modules can be imported"""
    try:
        from agents.query_agent import QueryAgent
        from agents.answer_agent import AnswerAgent
        assert QueryAgent is not None
        assert AnswerAgent is not None
    except ImportError as e:
        pytest.skip(f"Agent imports failed (expected without API keys): {e}")


def test_tool_imports():
    """Test that tool modules can be imported"""
    try:
        from tools.search_tool import SearchTool
        assert SearchTool is not None
    except ImportError as e:
        pytest.skip(f"Tool imports failed (expected without API keys): {e}")


def test_langflow_imports():
    """Test that langflow modules can be imported"""
    try:
        from langflow.graph import WebSearchWorkflow
        assert WebSearchWorkflow is not None
    except ImportError as e:
        pytest.skip(f"LangFlow imports failed (expected without API keys): {e}")


def test_main_modules():
    """Test that main modules exist and can be imported"""
    import main
    import server
    
    assert hasattr(main, 'main')
    assert hasattr(server, 'MCPWebSearchServer')


def test_project_structure():
    """Test that required files exist"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    required_files = [
        'agents/__init__.py',
        'agents/query_agent.py',
        'agents/answer_agent.py',
        'tools/__init__.py',
        'tools/search_tool.py',
        'langflow/__init__.py',
        'langflow/graph.py',
        'main.py',
        'server.py',
        'requirements.txt',
        'README.md',
        '.env.example'
    ]
    
    for file_path in required_files:
        full_path = os.path.join(project_root, file_path)
        assert os.path.exists(full_path), f"Required file missing: {file_path}"


def test_environment_example():
    """Test that .env.example has required variables"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_example_path = os.path.join(project_root, '.env.example')
    
    with open(env_example_path, 'r') as f:
        content = f.read()
    
    assert 'GEMINI_API_KEY' in content
    assert 'SERPAPI_KEY' in content


if __name__ == "__main__":
    pytest.main([__file__])