import os
import sys

# Get the project root directory
current_file = os.path.abspath(__file__)
workers_dir = os.path.dirname(current_file)
agents_dir = os.path.dirname(workers_dir)
backend_dir = os.path.dirname(agents_dir)
project_root = os.path.dirname(backend_dir)

# Add project root to sys.path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from langchain_core.messages import SystemMessage

# Try importing ClinicState
try:
    from backend.agents.state import ClinicState
except ImportError:
    try:
        from agents.state import ClinicState
    except ImportError:
        from state import ClinicState

def receptionist_node(state: ClinicState):
    """
    Initial triage, routing queries, and managing global state.
    """
    # Simple intent extraction (In production, use LLM/Tool extraction)
    issue = state.get("current_issue", "").lower()
    
    if "appointment" in issue or "book" in issue or "schedule" in issue:
        target = "appointment_agent"
    elif "rash" in issue or "skin" in issue or "mole" in issue or "pain" in issue:
        target = "specialist"
    elif "report" in issue or "blood" in issue or "lab" in issue:
        target = "lab_analyst"
    elif "wellness" in issue or "exercise" in issue or "diet" in issue:
        target = "wellness_agent"
    elif "prescription" in issue or "pill" in issue or "dose" in issue:
        target = "prescription_analyzer"
    elif "bill" in issue or "insurance" in issue:
        target = "admin_agent"
    else:
        # Default to Specialist for general medical triage
        target = "specialist"
        
    return {"next": target}
