from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import threading
from pathlib import Path
from src.cli import GenesisCLI
from src.deploy_agent import AgentDeployer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server/genesis")

class MergeRequest(BaseModel):
    repository_1: str
    repository_2: str
    agent_name: str
    merge_strategy: Optional[str] = "sequential"

class ActionRequest(BaseModel):
    input_data: Any

class ServerState:
    def __init__(self):
        self.cli = GenesisCLI()
        self.agent_running = False
        self.agent_task = None
        self._stop_event = threading.Event()

    def _run_agent_loop(self, agent_name):
        try:
            logger.info(f"Agent '{agent_name}' is now running.")
            while not self._stop_event.is_set():
                result = self.cli.perform_agent_action(agent_name, "Running periodic task")
                logger.info(f"Periodic Agent Output: {result}")
        except Exception as e:
            logger.error(f"Error in agent loop: {e}")
        finally:
            self.agent_running = False
            logger.info(f"Agent '{agent_name}' stopped.")

    def start_agent_loop(self, agent_name):
        if self.agent_running:
            raise ValueError(f"Agent '{agent_name}' is already running.")
        self.agent_running = True
        self._stop_event.clear()
        self.agent_task = threading.Thread(target=self._run_agent_loop, args=(agent_name,))
        self.agent_task.start()

    def stop_agent_loop(self):
        if self.agent_running:
            self._stop_event.set()
            self.agent_task.join(timeout=5)
            self.agent_running = False

class GenesisServer:
    def __init__(self):
        self.app = FastAPI(title="Genesis Server")
        self.state = ServerState()
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/status")
        async def status():
            return {
                "status": "running",
                "agent_running": self.state.agent_running
            }

        @self.app.get("/agents")
        async def list_agents():
            try:
                agents_dir = Path("./output")
                agents = [f.stem for f in agents_dir.glob("*_merged_agent") if agents_dir.exists()]
                return {"agents": agents}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/agents/merge")
        async def merge_agents(request: MergeRequest):
            try:
                deployer = AgentDeployer(
                    framework1_repo=request.repository_1,
                    framework2_repo=request.repository_2,
                    agent_name=request.agent_name,
                    merge_strategy=request.merge_strategy
                )
                deployer.run(input_data="")
                return {"status": "success", "agent": request.agent_name}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.post("/agents/{agent_name}/deploy")
        async def deploy_agent(agent_name: str):
            try:
                self.state.start_agent_loop(agent_name)
                return {"status": "success", "message": f"Agent '{agent_name}' deployed and running."}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.post("/agents/{agent_name}/stop")
        async def stop_agent(agent_name: str):
            try:
                self.state.stop_agent_loop()
                return {"status": "success", "message": f"Agent '{agent_name}' stopped."}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.get("/agents/{agent_name}/logs")
        async def get_logs(agent_name: str):
            try:
                log_path = Path(f"./logs/{agent_name}.log")
                if log_path.exists():
                    with open(log_path, 'r') as log_file:
                        return {"logs": log_file.read()}
                else:
                    raise HTTPException(status_code=404, detail=f"No logs found for agent '{agent_name}'.")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/agents/{agent_name}/action")
        async def perform_action(agent_name: str, request: ActionRequest):
            try:
                result = self.state.cli.perform_agent_action(agent_name, request.input_data)
                return {"status": "success", "result": result}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

def create_app():
    server = GenesisServer()
    return server.app
