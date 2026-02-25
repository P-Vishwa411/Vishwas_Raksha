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

def specialist_node(state: ClinicState):
    """
    Visual (multimodal) and text-based preliminary assessment.
    Tiers: Skin Specialist, General Surgeon.
    """
    issue = state.get("current_issue", "").lower()
    
    if "rash" in issue or "skin" in issue or "mole" in issue:
        specialty = "Skin Specialist"
        assessment = "Based on the description, this looks like contact dermatitis or a localized reaction. Avoid scratching and apply a mild hydrocortisone cream if needed."
    elif "pain" in issue or "appendicitis" in issue or "surgery" in issue:
        specialty = "General Surgeon"
        assessment = "Preliminary notes suggest checking for rebound tenderness. If pain is acute in the lower right abdomen, seek ER for possible appendectomy evaluation."
    else:
        specialty = "General Triage"
        assessment = "Symptoms are broad. A physical examination is recommended to determine the best course of action."

    response = f"### {specialty} Assessment\n{assessment}"
    
    return {
        "messages": [SystemMessage(content=response)],
        "worker_results": {"specialist_assessment": response}
    }
