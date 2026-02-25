from typing import List, Dict, Any, Optional
from langchain_core.messages import BaseMessage


def build_agent_response(
    messages: Optional[List[BaseMessage]] = None,
    next_agent: Optional[str] = None,
    worker_results: Optional[Dict[str, Any]] = None,
    status: str = "success",
    error: Optional[str] = None,
) -> Dict[str, Any]:

    return {
        "messages": messages or [],
        "next": next_agent,
        "worker_results": worker_results or {},
        "status": status,
        "error": error,
    }