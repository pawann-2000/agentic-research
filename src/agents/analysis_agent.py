import warnings
from typing import List
from llama_index.core.tools import BaseTool
from llama_index.core.llms import LLM

warnings.filterwarnings("ignore", category=DeprecationWarning, module="llama_index.core.agent.react.base")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="deprecated.classic")

from llama_index.core.agent import ReActAgent

ANALYSIS_AGENT_PROMPT = """You are an Analysis Agent. Answer questions based on research data.

CRITICAL INSTRUCTIONS:
- Read the research data provided
- Answer the question directly - NO TOOL USE unless data is overwhelming
- Structure your answer with clear points
- Include source citations

DO NOT overthink. Answer immediately if you have the information.
"""

def create_analysis_agent(
    llm: LLM,
    tools: List[BaseTool],
    verbose: bool = True,
    max_iterations: int = 5
) -> ReActAgent:
    """
    Create an analysis agent for synthesizing research findings.

    Args:
        llm: Language model instance
        tools: List of analysis tools for the agent
        verbose: Whether to print debug info
        max_iterations: Maximum reasoning iterations (default: 5)

    Returns:
        Configured ReActAgent
    """
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=verbose,
        context=ANALYSIS_AGENT_PROMPT,
        max_iterations=max_iterations
    )

    return agent