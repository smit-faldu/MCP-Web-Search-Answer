"""
Command Line Interface for MCP Web Search Answer
Interactive CLI for testing the web search and answer functionality
"""

import sys
from server import MCPWebSearchServer


def main():
    """
    Interactive CLI for the MCP Web Search Answer application
    """
    print("🌟 MCP Web Search Answer - Interactive CLI")
    print("=" * 50)
    print("Ask any question and get AI-powered answers from web search!")
    print("Type 'quit', 'exit', or 'q' to stop.")
    print("=" * 50)
    
    try:
        # Initialize the server
        server = MCPWebSearchServer()
        print("✅ Server initialized successfully!\n")
        
        while True:
            # Get user input
            try:
                question = input("🤔 Your question: ").strip()
                
                # Check for exit commands
                if question.lower() in ['quit', 'exit', 'q', '']:
                    print("👋 Goodbye!")
                    break
                
                print("\n🔄 Processing your question...")
                print("-" * 30)
                
                # Process the question
                result = server.process_question(question)
                
                # Display the answer
                print(f"💡 Answer: {result['content']}")
                
                # Display metadata if available
                if 'metadata' in result and result['metadata'].get('success'):
                    search_query = result['metadata'].get('search_query', 'N/A')
                    print(f"🔍 Search query used: {search_query}")
                
                print("\n" + "=" * 50)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error processing question: {e}")
                print("Please try again with a different question.\n")
                continue
    
    except Exception as e:
        print(f"❌ Failed to initialize server: {e}")
        print("Please check your .env file and ensure all API keys are set correctly.")
        sys.exit(1)


if __name__ == "__main__":
    main()