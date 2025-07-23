"""
LangGraph Workflow Manager
Defines the transition logic between agents and tools in the MCP application
"""

from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from agents.query_agent import QueryAgent
from agents.answer_agent import AnswerAgent
from tools.search_tool import SearchTool


class WorkflowState(TypedDict):
    """State object that flows through the workflow"""
    original_question: str
    search_query: str
    search_results: str
    final_answer: str
    current_step: str


class WebSearchWorkflow:
    """
    LangGraph-based workflow that orchestrates the web search and answer process
    """
    
    def __init__(self):
        # Initialize all agents and tools
        self.query_agent = QueryAgent()
        self.search_tool = SearchTool()
        self.answer_agent = AnswerAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow with proper transitions
        
        Returns:
            Compiled StateGraph workflow
        """
        # Create the state graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes for each step
        workflow.add_node("query_processing", self._process_query)
        workflow.add_node("web_search", self._perform_search)
        workflow.add_node("answer_generation", self._generate_answer)
        
        # Define the flow transitions
        workflow.set_entry_point("query_processing")
        workflow.add_edge("query_processing", "web_search")
        workflow.add_edge("web_search", "answer_generation")
        workflow.add_edge("answer_generation", END)
        
        # Compile the workflow
        return workflow.compile()
    
    def _process_query(self, state: WorkflowState) -> WorkflowState:
        """
        Node function: Process user question into search query
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with search query
        """
        try:
            # Use query agent to generate search query
            result = self.query_agent(state["original_question"])
            search_query = result["content"]
            
            # Update state
            state["search_query"] = search_query
            state["current_step"] = "query_processed"
            
            print(f"🔍 Generated search query: {search_query}")
            
        except Exception as e:
            state["search_query"] = state["original_question"]  # Fallback
            state["current_step"] = f"query_error: {str(e)}"
            print(f"❌ Query processing error: {e}")
        
        return state
    
    def _perform_search(self, state: WorkflowState) -> WorkflowState:
        """
        Node function: Perform web search using the generated query
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with search results
        """
        try:
            # Use search tool to get results
            result = self.search_tool(state["search_query"])
            search_results = result["content"]
            
            # Update state
            state["search_results"] = search_results
            state["current_step"] = "search_completed"
            
            print(f"🌐 Retrieved search results ({len(search_results)} characters)")
            
        except Exception as e:
            state["search_results"] = f"Search failed: {str(e)}"
            state["current_step"] = f"search_error: {str(e)}"
            print(f"❌ Search error: {e}")
        
        return state
    
    def _generate_answer(self, state: WorkflowState) -> WorkflowState:
        """
        Node function: Generate final answer from search results
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with final answer
        """
        try:
            # Use answer agent to synthesize results
            result = self.answer_agent(
                state["search_results"], 
                state["original_question"]
            )
            final_answer = result["content"]
            
            # Update state
            state["final_answer"] = final_answer
            state["current_step"] = "answer_generated"
            
            print(f"✅ Generated final answer ({len(final_answer)} characters)")
            
        except Exception as e:
            state["final_answer"] = f"Answer generation failed: {str(e)}"
            state["current_step"] = f"answer_error: {str(e)}"
            print(f"❌ Answer generation error: {e}")
        
        return state
    
    def run(self, user_question: str) -> Dict[str, Any]:
        """
        Execute the complete workflow for a user question
        
        Args:
            user_question: The user's natural language question
            
        Returns:
            Dict containing the final answer and workflow metadata
        """
        # Initialize state
        initial_state = WorkflowState(
            original_question=user_question,
            search_query="",
            search_results="",
            final_answer="",
            current_step="initialized"
        )
        
        print(f"🚀 Starting workflow for question: {user_question}")
        
        try:
            # Run the workflow
            final_state = self.workflow.invoke(initial_state)
            
            return {
                "content": final_state["final_answer"],
                "metadata": {
                    "search_query": final_state["search_query"],
                    "current_step": final_state["current_step"],
                    "success": "error" not in final_state["current_step"]
                }
            }
            
        except Exception as e:
            print(f"❌ Workflow execution error: {e}")
            return {
                "content": f"Workflow failed: {str(e)}",
                "metadata": {
                    "search_query": "",
                    "current_step": f"workflow_error: {str(e)}",
                    "success": False
                }
            }
    
    def get_workflow_status(self) -> Dict[str, str]:
        """
        Get information about the workflow configuration
        
        Returns:
            Dict with workflow status information
        """
        return {
            "workflow_type": "LangGraph StateGraph",
            "nodes": ["query_processing", "web_search", "answer_generation"],
            "entry_point": "query_processing",
            "agents": ["QueryAgent", "AnswerAgent"],
            "tools": ["SearchTool"],
            "status": "ready"
        }