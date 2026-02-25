# import os
# import sys

# # Get the project root directory
# current_file = os.path.abspath(__file__)
# workers_dir = os.path.dirname(current_file)
# agents_dir = os.path.dirname(workers_dir)
# backend_dir = os.path.dirname(agents_dir)
# project_root = os.path.dirname(backend_dir)

# # Add project root to sys.path if not already there
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)

# if backend_dir not in sys.path:
#     sys.path.insert(0, backend_dir)

# from datetime import datetime, timedelta
# from langchain_core.messages import SystemMessage

# # Try importing ClinicState
# try:
#     from backend.agents.state import ClinicState
# except ImportError:
#     try:
#         from agents.state import ClinicState
#     except ImportError:
#         from state import ClinicState

# def appointment_agent_node(state: ClinicState):
#     """
#     Integrates with Google/Outlook Calendar (Mocked) to book, reschedule.
#     """
#     user_input = state.get("current_issue", "").lower()
    
#     # Mocking availability
#     tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
#     available_slots = ["09:00 AM", "11:30 AM", "02:00 PM"]
    
#     if "book" in user_input or "schedule" in user_input:
#         chosen_slot = available_slots[0]
#         msg = f"I've checked the clinic calendar. We have a slot available at **{chosen_slot}** on **{tomorrow}**. Should I finalize this booking for you?"
#         status = "searching"
#     elif "confirm" in user_input or "yes" in user_input:
#         msg = "Confirmed! I've added the appointment to our system and sent a calendar invite to your email."
#         status = "booked"
#     else:
#         msg = f"I can help you schedule an appointment. Our next available dates start from **{tomorrow}**."
#         status = "intro"
        
#     return {
#         "messages": [SystemMessage(content=msg)],
#         "worker_results": {"appointment_status": status}
#     }
from backend.core.base_agent import BaseAgent
from langchain_core.messages import AIMessage


class AppointmentAgent(BaseAgent):

    def run(self, state: dict) -> dict:

        message = "Your appointment request has been received. Our team will contact you shortly."

        return {
            "messages": [AIMessage(content=message)],
            "next": None,
            "worker_results": {
                "appointment_status": "initiated"
            }
        }


appointment_agent = AppointmentAgent()


def appointment_agent_node(state: dict):
    return appointment_agent.execute(state)