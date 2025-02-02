import json
import random
import time
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from src.connection_manager import ConnectionManager
from src.helpers import print_h_bar
from src.action_handler import execute_action
from datetime import datetime

REQUIRED_FIELDS = ["name", "description", "traits", "examples", "loop_delay", "config", "tasks"]

logger = logging.getLogger("genesis_agent")

class GenesisAgent:
    def __init__(self, agent_name: str):
        try:
            agent_path = Path("output") / f"{agent_name}_merged_agent.json"
            with open(agent_path, "r") as file:
                agent_dict = json.load(file)

            missing_fields = [field for field in REQUIRED_FIELDS if field not in agent_dict]
            if missing_fields:
                raise KeyError(f"Missing required fields: {', '.join(missing_fields)}")

            self.name = agent_dict["name"]
            self.description = agent_dict["description"]
            self.traits = agent_dict["traits"]
            self.examples = agent_dict["examples"]
            self.loop_delay = agent_dict["loop_delay"]
            self.connection_manager = ConnectionManager(agent_dict["config"])
            self.use_time_based_weights = agent_dict.get("use_time_based_weights", False)
            self.time_based_multipliers = agent_dict.get("time_based_multipliers", {})

            self.tasks = agent_dict.get("tasks", [])
            self.task_weights = [task.get("weight", 1) for task in self.tasks]

            self.logger = logging.getLogger(f"agent_{self.name}")
            self.state = {}

        except Exception as e:
            logger.error(f"Could not load Genesis agent: {e}")
            raise e

    def _setup_framework_connections(self):
        """Setup connections to merged frameworks"""
        self.framework_providers = self.connection_manager.get_framework_providers()
        if not self.framework_providers:
            raise ValueError("No configured framework providers found")

    def _construct_system_prompt(self) -> str:
        """Construct the system prompt from agent configuration"""
        if not hasattr(self, '_system_prompt'):
            prompt_parts = [self.description]

            if self.traits:
                prompt_parts.append("\nKey traits:")
                prompt_parts.extend(f"- {trait}" for trait in self.traits)

            if self.examples:
                prompt_parts.append("\nExamples of expected behavior:")
                prompt_parts.extend(f"- {example}" for example in self.examples)

            self._system_prompt = "\n".join(prompt_parts)

        return self._system_prompt

    def _adjust_weights_for_time(self, current_hour: int, task_weights: list) -> list:
        weights = task_weights.copy()

        if 1 <= current_hour <= 5:
            weights = [
                weight * self.time_based_multipliers.get("night_multiplier", 0.5)
                for weight in weights
            ]
        if 8 <= current_hour <= 20:
            weights = [
                weight * self.time_based_multipliers.get("day_multiplier", 1.5)
                for weight in weights
            ]
        return weights

    def perform_action(self, connection: str, action: str, **kwargs) -> None:
        return self.connection_manager.perform_action(connection, action, **kwargs)

    def select_action(self, use_time_based_weights: bool = False) -> dict:
        task_weights = self.task_weights.copy()

        if use_time_based_weights:
            current_hour = datetime.now().hour
 
