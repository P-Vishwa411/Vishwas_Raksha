from backend.core.agent_contract import build_agent_response
from langchain_core.messages import AIMessage


def receptionist_node(state: dict):
    """
    Initial triage, routing queries, and managing global state.
    Always returns standardized agent response.
    """

    issue = state.get("current_issue", "").lower()

    if any(word in issue for word in ["appointment", "book", "schedule"]):
        target = "appointment_agent"
        message = "I'll connect you to the appointment agent."

    elif any(word in issue for word in ["rash", "skin", "mole", "pain"]):
        target = "specialist"
        message = "Routing you to a medical specialist."

    elif any(word in issue for word in ["report", "blood", "lab"]):
        target = "lab_analyst"
        message = "Connecting you to lab analysis."

    elif any(word in issue for word in ["wellness", "exercise", "diet"]):
        target = "wellness_agent"
        message = "Forwarding to wellness advisor."

    elif any(word in issue for word in ["prescription", "pill", "dose"]):
        target = "prescription_analyzer"
        message = "Sending to prescription analyzer."

    elif any(word in issue for word in ["bill", "insurance"]):
        target = "admin_agent"
        message = "Redirecting to administrative support."

    else:
        target = "specialist"
        message = "I'll connect you to a general medical specialist."

    return build_agent_response(
        messages=[AIMessage(content=message)],
        next_agent=target,
        worker_results={"triage_decision": target}
    )