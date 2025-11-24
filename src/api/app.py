import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from .models import (
    ResearchQuery,
    ResearchResponse,
    ErrorResponse,
    HealthResponse,
    Source,
    StreamChunk
)

from .research_service import ResearchService

load_dotenv()

research_service: ResearchService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global research_service

    try:
        research_service = ResearchService()
        await research_service.initialize()
    except Exception as e:
        raise

    yield

    if research_service:
        await research_service.shutdown()

app = FastAPI (
    title="Multi-Agent Research Assistant API",
    description="Ultra-fast AI-powered research assistant using Cerebras, Exa and Llamaindex",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates_path = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_path)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Multi-Agent Research Assistant",
        "heading": "Multi-Agent Research Assistant",
        "description": "Ultra-fast AI-powered research using Cerebras,Exa and Llamaindex",
        "badges": [
            "450 tokens/sec",
            "Semantic Search",
            "Multi-Agent workflows"
        ],
        "placeholder": "What are the latest developments in quantum computing?",
        "examples": [
            "What are the latest developments in quantum computing?",
            "Compare GPT-5, Claude 4.5 Sonnet and Gemini 3 Pro",
            "What is the future of autonomous vehicles?"
        ],
        "footer_text": "Powered by Cerebras (inference) + Exa (search) + Llamaindex (orchestration)"
    })

@app.get("/api/health", response_model=HealthResponse)
async def healthcheck():
    services = {}

    if research_service and research_service.initialized:
        services["research_service"] = "healthy"
    else:
        services["research_service"] = "unhealthy"

    services["cerebras_api_key"] = "configured" if os.getenv("CEREBRAS_API_KEY") else "missing"
    services["exa_api_key"] = "configured" if os.getenv("EXA_API_KEY") else "missing"

    overall_status = "healthy" if all(
        status in ["healthy", "configured"] for status in services.values()
    ) else "degraded"

    return HealthResponse(
        status=overall_status,
        version="1.0.0",
        services=services
    )

@app.post("/api/research", response_model=ResearchResponse)
async def research_query(query: ResearchQuery):
    
    if not research_service or not research_service.initialized:
        raise HTTPException(
            status_code=503,
            detail="Research service not initialized. Check API configuration."
        )
    
    try:
        start_time = time.time()

        result = await research_service.execute_query(
            query=query.query,
            num_results=query.num_results
        )

        research_time = time.time() - start_time

        sources = []
        if "sources" in result:
            for source in result["sources"]:
                sources.append(Source(
                    title=source.get("title", ""),
                    url=source.get("url", ""),
                    highlights=source.get("highlights", ""),
                    published_date=source.get("published_date"),
                    author=source.get("author")
                ))
        
        return ResearchResponse(
            query=query.query,
            answer=result.get("answer", ""),
            sources=sources,
            research_time_seconds=round(research_time, 2)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research query failed: {str(e)}"
        )
    
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):

    try:
        await websocket.accept()
    except Exception as e:
        raise

    if not research_service or not research_service.initialized:
        await websocket.send_json({
            "type": "error",
            "content": "Research service not initialized. Check API configuration.",
            "timestamp": time.time()
        })
        await websocket.close()
        return

    try:
        data = await websocket.receive_json()
        query = data.get("query", "")
        num_results = data.get("num_results", 5)

        if not query:
            await websocket.send_json({
                "type": "error",
                "content": "Query is required",
                "timestamp": time.time()
            })
            await websocket.close()
            return

        await websocket.send_json({
            "type": "start",
            "content": f"Starting research for: {query}",
            "timestamp": time.time()
        })

        async for chunk in research_service.execute_query_streaming(query, num_results):
            await websocket.send_json({
                "type": chunk.type,
                "content": chunk.content,
                "metadata": chunk.metadata,
                "timestamp": chunk.timestamp.isoformat()
            })

        await websocket.send_json({
            "type": "complete",
            "content": "Research complete",
            "timestamp": time.time()
        })

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "content": str(e),
                "timestamp": time.time()
            })
        except:
            pass
        await websocket.close()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exception):
    return JSONResponse(
        status_code=exception.status_code,
        content=ErrorResponse(
            error=exception.detail,
            detail=str(exception)
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exception)
        ).model_dump()
    )

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )