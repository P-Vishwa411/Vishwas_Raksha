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

def wellness_agent_node(state: ClinicState):
    """
    Generates personalized recovery and wellness plans based on patient profile.
    Tiers: Gym, Music Therapy, Exercise.
    """
    patient_info = state.get("patient_info", {})
    issue = state.get("current_issue", "").lower()
    
    plan = "### Personalized Wellness Plan\n"
    
    if "stress" in issue or "anxiety" in issue:
        plan += "- **Music Therapy**: 20 mins of ambient sounds before bed.\n"
        plan += "- **Exercise**: Light Yoga or 15-min walk.\n"
    elif "recovery" in issue or "surgery" in issue:
        plan += "- **Physiotherapy**: Low-impact movements twice daily.\n"
        plan += "- **Nutrition**: High protein and hydration focus.\n"
    else:
        plan += "- **General**: 30 mins moderate exercise 5 days/week.\n"
        plan += "- **Mental Health**: Mindfulness meditation (5 mins).\n"

    return {
        "messages": [SystemMessage(content=plan)],
        "worker_results": {"wellness_plan": plan}
    }
