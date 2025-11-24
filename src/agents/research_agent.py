import warnings
from typing import List
from llama_index.core.tools import BaseTool
from llama_index.core.llms import LLM

warnings.filterwarnings("ignore", category=DeprecationWarning, module="llama_index.core.agent.react.base")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="deprecated.classic")

from llama_index.core.agent import ReActAgent

RESEARCH_AGENT_PROMPT = """You are a Research Agent. Search the web and summarize findings.

CRITICAL INSTRUCTIONS:
- Use search_web ONCE with a clear query
- Immediately summarize the results with titles and URLs
- Stop after summarizing - DO NOT search multiple times
- Only use additional tools if absolutely critical
- DO NOT give the content back in markdown

Your summary will be used for analysis, so include key points and sources.
"""

def create_research_agent(
    llm: LLM,
    tools: List[BaseTool],
    verbose: bool=True,
    max_iterations: int = 5
) -> ReActAgent:
    """
    Create a research agent with search capabilities.

    Args:
        llm: Language model instance
        tools: List of tools for the agent
        verbose: Whether to print debug info
        max_iterations: Maximum reasoning iterations (default: 5)

    Returns:
        Configured ReActAgent
    """
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=verbose,
        context=RESEARCH_AGENT_PROMPT,
        max_iterations=max_iterations
    )

    return agent