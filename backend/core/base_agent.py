from backend.core.agent_contract import build_agent_response


class BaseAgent:

    def execute(self, state: dict) -> dict:
        try:
            result = self.run(state)

            return build_agent_response(
                messages=result.get("messages"),
                next_agent=result.get("next"),
                worker_results=result.get("worker_results"),
                status="success"
            )

        except Exception as e:
            return build_agent_response(
                messages=[],
                next_agent=None,
                worker_results={},
                status="error",
                error=str(e)
            )

    def run(self, state: dict) -> dict:
        raise NotImplementedError("Agent must implement run() method.")