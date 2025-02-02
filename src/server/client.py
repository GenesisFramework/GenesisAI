import requests
from typing import Optional, List, Dict, Any

class GenesisClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def get_status(self) -> Dict[str, Any]:
        return self._make_request("GET", "/status")

    def list_merged_agents(self) -> List[str]:
        response = self._make_request("GET", "/agents")
        return response.get("agents", [])

    def merge_frameworks(self, repo1_url: str, repo2_url: str, agent_name: str, merge_strategy: str = "sequential") -> Dict[str, Any]:
        data = {
            "repository_1": repo1_url,
            "repository_2": repo2_url,
            "agent_name": agent_name,
            "merge_strategy": merge_strategy
        }
        return self._make_request("POST", "/agents/merge", json=data)

    def deploy_agent(self, agent_name: str) -> Dict[str, Any]:
        return self._make_request("POST", f"/agents/{agent_name}/deploy")

    def stop_agent(self, agent_name: str) -> Dict[str, Any]:
        return self._make_request("POST", f"/agents/{agent_name}/stop")

    def get_agent_logs(self, agent_name: str) -> Dict[str, Any]:
        return self._make_request("GET", f"/agents/{agent_name}/logs")

    def perform_agent_action(self, agent_name: str, input_data: Any) -> Dict[str, Any]:
        data = {
            "input_data": input_data
        }
        return self._make_request("POST", f"/agents/{agent_name}/action", json=data)
