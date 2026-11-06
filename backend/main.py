from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from .models import (
    GlobalStateResponse,
    GovernanceExecutionRequest,
    GovernanceExecutionResponse,
    ChallengeAnalyzeRequest,
    ChallengeAnalyzeResponse
)
from .state_store import state_manager
from .analyzer import analyze_custom_prompt

app = FastAPI(title="ZeroDog: AI Behavioral FinOps & MCP Governance Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class SelectIncidentRequest(BaseModel):
    incident_id: str

@app.get("/api/state", response_model=GlobalStateResponse)
async def get_state():
    return state_manager.get_state()

@app.post("/api/incident/select")
async def select_incident(req: SelectIncidentRequest):
    inc = state_manager.set_current_incident(req.incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"success": True, "incident": inc}

@app.post("/api/query")
async def query_telemetry(req: QueryRequest):
    return state_manager.query(req.query)

@app.post("/api/governance", response_model=GovernanceExecutionResponse)
async def execute_governance(req: GovernanceExecutionRequest):
    try:
        res = state_manager.execute_governance(req.incident_id, req.mode, req.force_override)
        return res
    except PermissionError as pe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "SAFETY_INTERCEPT_ENFORCED",
                "message": str(pe),
                "incident_id": req.incident_id,
                "intercept_blocked": True,
                "recommended_action": "Switch to REALLOCATE_QUOTA or approve compliance exception"
            }
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

@app.post("/api/challenge/analyze", response_model=ChallengeAnalyzeResponse)
async def analyze_stack_challenge(req: ChallengeAnalyzeRequest):
    return analyze_custom_prompt(
        prompt_text=req.prompt_text,
        target_model=req.target_model or "claude-3-opus",
        mcp_tools_text=req.mcp_tools_text or ""
    )

@app.post("/api/reset")
async def reset_demo_state():
    state_manager.reset()
    return {"success": True, "message": "ZeroDog state successfully restored to initial pre-baked telemetry."}

frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(str(frontend_dir / "index.html"))
