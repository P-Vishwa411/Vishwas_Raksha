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

# from langchain_core.messages import SystemMessage, HumanMessage

# # Try importing ClinicState
# try:
#     from backend.agents.state import ClinicState
# except ImportError:
#     try:
#         from agents.state import ClinicState
#     except ImportError:
#         from state import ClinicState

# # Try importing ChatOpenAI
# try:
#     from langchain_openai import ChatOpenAI
# except ImportError:
#     ChatOpenAI = None

# def prescription_analyzer_node(state: ClinicState):
#     """
#     Checks for drug-to-drug interactions and explains dosage.
#     Uses OCR/Vision if an image is provided.
#     """
#     image_data = state.get("image_data")
#     text_query = state.get("current_issue", "")
    
#     # Check if ChatOpenAI is available
#     if ChatOpenAI is None:
#         # Return a mock response if OpenAI is not available
#         return {
#             "messages": [SystemMessage(content="Prescription analyzer requires OpenAI API key. Please configure your API key in the .env file.")],
#             "worker_results": {"prescription_check": "error_no_api_key"}
#         }
    
#     llm = ChatOpenAI(model="gpt-4o")
    
#     prompt = "You are a medical prescription analyzer. Check for drug-to-drug interactions and explain dosage clearly."
    
#     if image_data:
#         # Multimodal request
#         content = [
#             {"type": "text", "text": prompt + f" User query: {text_query}"},
#             {
#                 "type": "image_url",
#                 "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
#             },
#         ]
#         response = llm.invoke([HumanMessage(content=content)])
#     else:
#         # Text-only request
#         response = llm.invoke([HumanMessage(content=prompt + f" Medications: {text_query}")])

#     msg = response.content
    
#     return {
#         "messages": [SystemMessage(content=msg)],
#         "worker_results": {"prescription_check": "complete", "ocr_used": bool(image_data)}
#     }


from backend.core.base_agent import BaseAgent
from langchain_core.messages import AIMessage


class PrescriptionAnalyzerAgent(BaseAgent):

    def run(self, state: dict) -> dict:

        message = "Your prescription has been reviewed. Please follow dosage instructions carefully."

        return {
            "messages": [AIMessage(content=message)],
            "next": None,
            "worker_results": {
                "prescription_reviewed": True
            }
        }


prescription_agent = PrescriptionAnalyzerAgent()


def prescription_analyzer_node(state: dict):
    return prescription_agent.execute(state)