from typing import TypedDict, Annotated, List, Union
from langchain_core.messages import BaseMessage
import operator

class ClinicState(TypedDict):
    # The messages in the conversation
    messages: Annotated[List[BaseMessage], operator.add]
    # The next agent to route to
    next: str
    # Patient history / context
    patient_id: str
    patient_info: dict
    # Current symptoms / query
    current_issue: str
    # Base64 image data for OCR/Vision
    image_data: str 
    # Flag for doctor review
    needs_review: bool
    # Results from worker agents
    worker_results: dict
