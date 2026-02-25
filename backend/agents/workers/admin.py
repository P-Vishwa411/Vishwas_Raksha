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

def admin_agent_node(state: ClinicState):
    """
    Generates HIPAA-compliant billing summaries and insurance claim drafts.
    """
    # Track actions taken by previous agents to generate bill
    worker_results = state.get("worker_results", {})
    
    bill_items = []
    if "specialist_assessment" in worker_results:
        bill_items.append("Specialist Consultation: $150")
    if "lab_analysis" in worker_results:
        bill_items.append("Lab Interpretation: $75")
    if "wellness_plan" in worker_results:
        bill_items.append("Wellness Program Setup: $50")
    if not bill_items:
        bill_items.append("General Triage/Reception: $25")

    total = sum(int(item.split("$")[1]) for item in bill_items)
    
    summary = "### Admin & Billing Summary (HIPAA-Compliant)\n"
    summary += "\n".join([f"- {item}" for item in bill_items])
    summary += f"\n\n**Total Estimated Cost**: ${total}\n"
    summary += "**Insurance Status**: Draft claim generated for primary provider."
    
    return {
        "messages": [SystemMessage(content=summary)],
        "worker_results": {"billing_summary": summary}
    }
