import os
import sys

# Get the project root directory
current_file = os.path.abspath(__file__)
agents_dir = os.path.dirname(current_file)
backend_dir = os.path.dirname(agents_dir)
project_root = os.path.dirname(backend_dir)

# Add project root to sys.path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from langgraph.graph import StateGraph, END

# Try importing ClinicState
try:
    from backend.agents.state import ClinicState
except ImportError:
    try:
        from agents.state import ClinicState
    except ImportError:
        from state import ClinicState

# Try importing node functions
try:
    from backend.agents.workers.receptionist import receptionist_node
    from backend.agents.workers.appointment import appointment_agent_node
    from backend.agents.workers.lab_analyst import lab_analyst_node
    from backend.agents.workers.specialists import specialist_node
    from backend.agents.workers.wellness import wellness_agent_node
    from backend.agents.workers.prescription import prescription_analyzer_node
    from backend.agents.workers.admin import admin_agent_node
except ImportError:
    try:
        from agents.workers.receptionist import receptionist_node
        from agents.workers.appointment import appointment_agent_node
        from agents.workers.lab_analyst import lab_analyst_node
        from agents.workers.specialists import specialist_node
        from agents.workers.wellness import wellness_agent_node
        from agents.workers.prescription import prescription_analyzer_node
        from agents.workers.admin import admin_agent_node
    except ImportError:
        from workers.receptionist import receptionist_node
        from workers.appointment import appointment_agent_node
        from workers.lab_analyst import lab_analyst_node
        from workers.specialists import specialist_node
        from workers.wellness import wellness_agent_node
        from workers.prescription import prescription_analyzer_node
        from workers.admin import admin_agent_node

# Create the graph
workflow = StateGraph(ClinicState)

# Add nodes
workflow.add_node("receptionist", receptionist_node)
workflow.add_node("appointment_agent", appointment_agent_node)
workflow.add_node("lab_analyst", lab_analyst_node)
workflow.add_node("specialist", specialist_node)
workflow.add_node("wellness_agent", wellness_agent_node)
workflow.add_node("prescription_analyzer", prescription_analyzer_node)
workflow.add_node("admin_agent", admin_agent_node)

# Define entry point
workflow.set_entry_point("receptionist")

# Conditional routing logic
def router(state):
    return state.get("next", END)

workflow.add_conditional_edges(
    "receptionist",
    router,
    {
        "appointment_agent": "appointment_agent",
        "lab_analyst": "lab_analyst",
        "specialist": "specialist",
        "wellness_agent": "wellness_agent",
        "prescription_analyzer": "prescription_analyzer",
        "admin_agent": "admin_agent",
        "human": END
    }
)

# Routing after workers
workflow.add_edge("appointment_agent", END)
workflow.add_edge("lab_analyst", END)
workflow.add_edge("specialist", END)
workflow.add_edge("wellness_agent", END)
workflow.add_edge("prescription_analyzer", "admin_agent") # Interaction check -> Billing
workflow.add_edge("admin_agent", END)

# Compile
# Note: interrupt_before=["admin_agent"] for HITL
app = workflow.compile(interrupt_before=["admin_agent"])
