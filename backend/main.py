from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import json
import uuid
from typing import Dict
from pydantic import Field

# Get the project root directory
current_file = os.path.abspath(__file__)
backend_dir = os.path.dirname(current_file)
project_root = os.path.dirname(backend_dir)

# Add project root to sys.path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Also add backend directory for 'backend.agents' imports
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from backend.agents.graph import app as graph_app
    from backend.agents.state import ClinicState
    # Import individual nodes for REST endpoints
    from backend.agents.workers.receptionist import receptionist_node
    from backend.agents.workers.appointment import appointment_agent_node
    from backend.agents.workers.lab_analyst import lab_analyst_node
    from backend.agents.workers.specialists import specialist_node
    from backend.agents.workers.wellness import wellness_agent_node
    from backend.agents.workers.prescription import prescription_analyzer_node
    from backend.agents.workers.admin import admin_agent_node
except ImportError:
    # Fallback: try relative imports from backend directory
    try:
        from agents.graph import app as graph_app
        from agents.state import ClinicState
        from agents.workers.receptionist import receptionist_node
        from agents.workers.appointment import appointment_agent_node
        from agents.workers.lab_analyst import lab_analyst_node
        from agents.workers.specialists import specialist_node
        from agents.workers.wellness import wellness_agent_node
        from agents.workers.prescription import prescription_analyzer_node
        from agents.workers.admin import admin_agent_node
    except ImportError as e:
        # Last resort: direct imports
        from backend.agents.graph import app as graph_app
        from backend.agents.state import ClinicState
        from backend.agents.workers.receptionist import receptionist_node
        from backend.agents.workers.appointment import appointment_agent_node
        from backend.agents.workers.lab_analyst import lab_analyst_node
        from backend.agents.workers.specialists import specialist_node
        from backend.agents.workers.wellness import wellness_agent_node
        from backend.agents.workers.prescription import prescription_analyzer_node
        from backend.agents.workers.admin import admin_agent_node

from langchain_core.messages import HumanMessage, BaseMessage

app = FastAPI(title="HMS Multi-Agent Backend")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    message: str
    patient_id: str = "anonymous"
    patient_info: Dict = Field(default_factory=dict)

@app.get("/")
async def root():
    return {
        "message": "ADHILAXMI Hospital Multi-Agent Backend is running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.1.0"}

# --- Orchestrated WebSocket Endpoint ---

@app.websocket("/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        while True:
            data = await websocket.receive_text()
            input_payload = json.loads(data)
            user_text = input_payload.get("message", "")
            
            state = {
                "messages": [HumanMessage(content=user_text)],
                "patient_id": input_payload.get("patient_id", "anonymous"),
                "patient_info": input_payload.get("patient_info", {}),
                "current_issue": user_text,
                "needs_review": False,
                "worker_results": {}
            }
            
            async for event in graph_app.astream(state, config):
                for node_name, node_output in event.items():
                    if not isinstance(node_output, dict):
                        continue
                        last_msg = node_output["messages"][-1]
                        content = last_msg.content if isinstance(last_msg, BaseMessage) else last_msg.get("content", "")
                        await websocket.send_json({
                            "node": node_name,
                            "content": content,
                            "role": "assistant"
                        })
            
            await websocket.send_json({"status": "done"})
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})

# --- Individual Worker REST Endpoints ---

def run_agent_sync(node_func, request: AgentRequest):
    state = {
        "messages": [HumanMessage(content=request.message)],
        "patient_id": request.patient_id,
        "patient_info": request.patient_info,
        "current_issue": request.message,
        "needs_review": False,
        "worker_results": {}
    }

    try:
        result = node_func(state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    message = ""
    if "messages" in result:
        last_msg = result["messages"][-1]
        message = (
            last_msg.content
            if isinstance(last_msg, BaseMessage)
            else last_msg.get("content", "")
        )

    return {
        "response": message,
        "worker_results": result.get("worker_results", {}),
        "next_step": result.get("next", "receptionist")
    }
@app.post("/agent/receptionist")
async def receptionist_endpoint(request: AgentRequest):
    return run_agent_sync(receptionist_node, request)

@app.post("/agent/appointment")
async def appointment_endpoint(request: AgentRequest):
    return run_agent_sync(appointment_agent_node, request)

@app.post("/agent/lab_analyst")
async def lab_endpoint(request: AgentRequest):
    return run_agent_sync(lab_analyst_node, request)

@app.post("/agent/specialist")
async def specialist_endpoint(request: AgentRequest):
    return run_agent_sync(specialist_node, request)

@app.post("/agent/wellness")
async def wellness_endpoint(request: AgentRequest):
    return run_agent_sync(wellness_agent_node, request)

@app.post("/agent/prescription")
async def prescription_endpoint(request: AgentRequest):
    return run_agent_sync(prescription_analyzer_node, request)

@app.post("/agent/admin")
async def admin_endpoint(request: AgentRequest):
    return run_agent_sync(admin_agent_node, request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
