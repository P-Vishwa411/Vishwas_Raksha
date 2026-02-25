from backend.agents.workers.receptionist import receptionist_node
from langchain_core.messages import HumanMessage


def test_receptionist_node_logic():
    state = {
        "messages": [HumanMessage(content="I want appointment")],
        "patient_id": "123",
        "patient_info": {},
        "current_issue": "I want appointment",
        "needs_review": False,
        "worker_results": {}
    }

    result = receptionist_node(state)

    assert isinstance(result, dict)
    assert "next" in result


def test_receptionist_invalid_input():
    state = {
        "messages": [],
        "patient_id": "123",
        "patient_info": {},
        "current_issue": "",
        "needs_review": False,
        "worker_results": {}
    }

    result = receptionist_node(state)

    assert result is not None
    assert isinstance(result, dict)