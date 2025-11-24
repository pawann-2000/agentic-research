from typing import Dict, Any, List
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    step,
    Event,
    Context
)
from llama_index.core.agent import ReActAgent
from llama_index.core.llms import ChatMessage

class ResearchEvent(Event):
    query: str

class AnalysisEvent(Event):
    research_data: str
    original_query: str

class ResearchWorkflow(Workflow):

    def __init__(
        self,
        research_agent: ReActAgent,
        analysis_agent: ReActAgent,
        verbose: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs) #IMPORTANT - Fetching research agent, analysis agent and verbosity from the parent class
        self.research_agent = research_agent
        self.analysis_agent = analysis_agent
        self.verbose = verbose

    @step
    async def start(self, ctx: Context, ev: StartEvent) -> ResearchEvent:
        query = ev.get("query", "")

        if self.verbose:
            print(f"\nStarting Research Workflow...")

        await ctx.set("original_query", query)

        return ResearchEvent(query=query)
    
    @step
    async def research_phase(self, ctx: Context, ev:ResearchEvent) -> AnalysisEvent:

        if self.verbose:
            print("Research agent is active...")

        research_task = (
            f"Search for information about: {ev.query}\n\n"
            "Use search_web to find relevant sources and provide a summary with URLs."
        )

        response = await self.research_agent.achat(research_task)

        research_data = str(response)

        sources = []
        if hasattr(response, 'sources') and response.sources:
            for source in response.sources:
                if hasattr(source, 'tool_output'):
                    tool_output = source.tool_output
                    if isinstance(tool_output, dict) and 'results' in tool_output:
                        sources.extend(tool_output['results'])

        await ctx.set("sources", sources)

        if self.verbose:
            print(f"\nResearch Complete. Data collected. Found {len(sources)} sources.")

        return AnalysisEvent(
            research_data=research_data,
            original_query=ev.query
        )
    
    @step
    async def analysis_phase(self, ctx: Context, ev: AnalysisEvent) -> StopEvent:

        if self.verbose:
            print("Analysis agent active...")

        analysis_task = (
            f"Question: {ev.original_query}\n\n"
            f"Research data:\n{ev.research_data}\n\n"
            "Provide a clear answer based on the research data above."
        )

        response = await self.analysis_agent.achat(analysis_task)

        final_answer = str(response)

        sources = await ctx.get("sources", default=[])

        if self.verbose:
            print("Workflow Complete.")

        return StopEvent(result={
            "answer": final_answer,
            "sources": sources
        })
    

async def run_research_query(
    workflow: ResearchWorkflow,
    query: str,
    timeout: int = 300
) -> str:
    """
    Run a research query through the workflow.

    Args:
        workflow: The ResearchWorkflow instance
        query: The research question
        timeout: Timeout in seconds (default: 300 = 5 minutes)

    Returns:
        The final research result
    """
    result = await workflow.run(query=query, timeout=timeout)

    return result