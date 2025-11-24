# Multi-Agent Research Assistant

A powerful multi-language AI research assistant that uses multiple intelligent agents to search, analyze, and provide detailed answers to your questions. This system combines ultra-fast AI inference from Cerebras, semantic search from Exa, and intelligent orchestration from LlamaIndex.

## What is This Project?

This is a multi-agent AI system that helps you research any topic. Think of it as having two AI assistants working together:

1. **Research Agent**: Searches the internet for relevant information using advanced semantic search
2. **Analysis Agent**: Analyzes the research findings and creates comprehensive summaries and insights

When you ask a question, these agents work together to find accurate information and present it in an easy-to-understand format.

## Key Features

- **Ultra-fast responses**: Uses Cerebras for lightning-fast AI processing (450+ tokens/second)
- **Semantic search**: Powered by Exa to find the most relevant information, not just keyword matches
- **Two usage modes**:
  - Command-line interface (CLI) for terminal users
  - Web API with a modern interface for browser users
- **Real-time streaming**: See results as they are generated via WebSocket
- **Intelligent workflows**: Agents coordinate automatically to provide the best answers

## Prerequisites

Before you begin, make sure you have the following installed on your computer:

### Required Software

1. **Python 3.9 or higher**
   - Check if you have Python installed by opening a terminal and running:
     ```bash
     python --version
     ```
   - If you don't have Python, download it from [python.org](https://www.python.org/downloads/)

2. **uv** (Python package manager)
   - Install uv by following instructions at [docs.astral.sh/uv](https://docs.astral.sh/uv/)
   - Or install via pip:
     ```bash
     pip install uv
     ```

### Required API Keys

You need two free API keys to use this project:

1. **Cerebras API Key** (for AI processing)
   - Sign up at [cerebras.ai](https://cerebras.ai/)
   - Get your API key from the dashboard

2. **Exa API Key** (for search)
   - Sign up at [exa.ai](https://exa.ai/)
   - Get your API key from the dashboard

## Installation

Follow these steps carefully:

### Step 1: Clone or Download the Project

If you're using git:
```bash
git clone https://github.com/pawann-2000/agentic-research
cd Agentic_RAG
```

Or download and extract the ZIP file, then navigate to the folder in your terminal.

### Step 2: Install Dependencies

Run this command in the project folder:

```bash
uv sync
```

This will install all the required Python packages. It might take a few minutes.

### Step 3: Configure Environment Variables

1. Create a file named `.env` in the project root folder (if it doesn't exist), just like `.env.example`.
2. Open it with a text editor and add your API keys:

```
CEREBRAS_API_KEY=your_cerebras_api_key_here
EXA_API_KEY=your_exa_api_key_here
CEREBRAS_MODEL=gpt-oss-120b
```

**Important**: Replace `your_cerebras_api_key_here` and `your_exa_api_key_here` with your actual API keys.

## How to Run the Project

There are three ways to use this research assistant:

### Option 1: Interactive Mode (Recommended for Beginners)

This mode lets you ask multiple questions in a conversation style.

```bash
uv run python run.py
```

You'll see:
```
INTERACTIVE RESEARCH ASSISTANT
============================================================
Ask me anything! I'll research and provide detailed answers.
Type 'quit' or 'exit' to stop.

Your question:
```

Type your question and press Enter. The system will research and provide an answer. You can keep asking more questions.

### Option 2: Single Query Mode

Ask a single question from the command line:

```bash
uv run python run.py --query "What are the latest developments in quantum computing?"
```

The system will answer your question and exit.

### Option 3: Demo Mode

See example questions and answers:

```bash
uv run python run.py --demo
```

This will run three pre-configured demo queries to show you how the system works.

## Example Usage

```
Your question: What is machine learning?

USER QUERY: What is machine learning?
============================================================

[Research Agent starts searching...]
[Analysis Agent starts analyzing...]

FINAL ANSWER
============================================================

Machine learning is a subset of artificial intelligence (AI) that enables
computers to learn and improve from experience without being explicitly
programmed. The system analyzes data, identifies patterns, and makes
decisions with minimal human intervention...

[Full detailed answer appears here]
```

### API Example

Once the web server is running, you can make API calls:

```bash
curl -X POST "http://localhost:8000/api/research" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is machine learning?", "num_results": 5}'
```

## Project Structure

Here's what each folder contains:

```
Agentic_RAG/
├── src/                          # Source code
│   ├── agents/                   # AI agent definitions
│   │   ├── research_agent.py    # Agent that searches for information
│   │   └── analysis_agent.py    # Agent that analyzes results
│   ├── tools/                    # Tools that agents use
│   │   ├── exa_tools.py         # Search tools (Exa integration)
│   │   └── analysis_tools.py    # Analysis tools
│   ├── research_workflows/       # Workflow orchestration
│   │   └── research_workflows.py # Coordinates agent collaboration
│   ├── api/                      # Web API
│   │   ├── app.py               # FastAPI server
│   │   ├── models.py            # Data models
│   │   └── research_service.py  # Research service logic
│   └── main.py                   # CLI entry point
├── run.py                        # Simple script to run the CLI
├── pyproject.toml               # Project configuration and dependencies
├── .env                         # Your API keys (keep this secret!)
└── README.md                    # This file
```

## Understanding the Components

### What are Agents?

Agents are AI components that can:
- Use tools (like search or analysis functions)
- Make decisions about what to do next
- Work together to solve complex tasks

This project has two agents that collaborate:
1. **Research Agent**: Finds information on the internet
2. **Analysis Agent**: Makes sense of the information

### What is a Workflow?

A workflow coordinates how agents work together. In this project:
1. You ask a question
2. The Research Agent searches for relevant information
3. The Analysis Agent processes the findings
4. You get a comprehensive answer

### What Technologies Are Used?

- **Cerebras**: Provides extremely fast AI model inference
- **Exa**: Semantic search engine (understands meaning, not just keywords)
- **LlamaIndex**: Framework for building AI applications with agents
- **FastAPI**: Modern web framework for building APIs
- **Python**: Programming language everything is written in

## Troubleshooting

### Problem: "CEREBRAS_API_KEY not found in environment variables"

**Solution**: Make sure you created the `.env` file with your API keys in the project root folder.

### Problem: "Module not found" errors

**Solution**: Make sure you ran `uv sync` to install all dependencies.

### Problem: "Connection refused" or API errors

**Solution**:
- Check that your API keys are valid
- Verify you have internet connection
- Make sure you haven't exceeded API rate limits

### Problem: "Port 8000 already in use" (for API mode)

**Solution**: Either:
- Stop the other program using port 8000
- Use a different port:
  ```bash
  uv run python -m uvicorn src.api.app:app --reload --port 8001
  ```

### Problem: Slow responses

**Solution**:
- The first query is slower because the system initializes
- Subsequent queries should be much faster
- Check your internet connection

## Advanced Configuration

### Changing the AI Model

You can use different Cerebras models by editing `.env`:

```
CEREBRAS_MODEL=llama3.3-70b
```

Available models:
- `llama3.3-70b`
- `llama3.1-8b`
- `gpt-oss-120b`
- `qwen-3-32b`

### Adjusting Agent Behavior

Edit `src/main.py` to change:
- `WORKFLOW_TIMEOUT`: Maximum time for a query (default: 300 seconds)
- `RESEARCH_AGENT_MAX_ITERATIONS`: How many search attempts (default: 10)
- `ANALYSIS_AGENT_MAX_ITERATIONS`: How many analysis steps (default: 10)

### Changing Search Results

When using the API, adjust `num_results` in your request:

```json
{
  "query": "Your question here",
  "num_results": 10
}
```

More results give more comprehensive answers but take longer.

## Learning Resources

### Understanding Multi-Agent Systems
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Introduction to AI Agents](https://www.anthropic.com/research)

### Learning Python
- [Python for Beginners](https://www.python.org/about/gettingstarted/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### Understanding APIs
- [What is a REST API?](https://www.redhat.com/en/topics/api/what-is-a-rest-api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all prerequisites are installed correctly
3. Make sure your API keys are valid and properly configured
4. Check that you have an active internet connection

## Next Steps

After you get the system running:
1. Try asking different types of questions
2. Experiment with the web interface
3. Look at the code to understand how agents work
4. Modify the system prompts in the agent files
5. Add your own custom tools for specialized tasks

## Contributing

This is a learning project. Feel free to:
- Experiment with the code
- Add new features
- Improve the documentation
- Share your findings

Remember: The best way to learn is by doing. Start with the interactive mode, ask some questions, and see how the agents work together!
