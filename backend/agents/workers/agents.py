from langchain_core.messages import SystemMessage
from backend.agents.state import ClinicState

def receptionist_node(state: ClinicState):
    """Supervisor agent that routes to workers based on intent."""
    # In a real app, this would use an LLM to extract intent
    return {"next": "appointment_agent"} # Default for now

def appointment_agent_node(state: ClinicState):
    """Agent for booking and managing appointments."""
    return {
        "messages": [SystemMessage(content="I've checked the clinic schedule. We have an opening tomorrow at 10 AM. Would you like to book it?")],
        "worker_results": {"appointment": "pending_confirmation"}
    }

def lab_analyst_node(state: ClinicState):
    """Agent for interpreting lab reports using RAG."""
    return {
        "messages": [SystemMessage(content="Your blood report looks normal. The hemoglobin levels are within the healthy range.")],
        "worker_results": {"lab_analysis": "normal"}
    }

def specialist_node(state: ClinicState):
    """Agent for preliminary specialist assessment."""
    return {
        "messages": [SystemMessage(content="Based on your description of the rash, it looks like contact dermatitis. I recommend a soothing cream.")],
        "worker_results": {"specialist_triage": "skin_specialist"}
    }
