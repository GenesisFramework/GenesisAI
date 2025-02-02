import os
import subprocess
from merge_strategy import MergeStrategy
import docker

class AgentDeployer:
    def __init__(self, framework1_repo, framework2_repo, agent_name, merge_strategy='sequential'):
        self.framework1_repo = framework1_repo
        self.framework2_repo = framework2_repo
        self.agent_name = agent_name
        self.merge_strategy = merge_strategy
        self.base_dir = os.getcwd()
        self.agent_dir = os.path.join(self.base_dir, f"{self.agent_name}_merged_agent")
        self.docker_client = docker.from_env()

    def clone_repositories(self):
        subprocess.run(['git', 'clone', self.framework1_repo, 'framework1'], check=True)
        subprocess.run(['git', 'clone', self.framework2_repo, 'framework2'], check=True)

    def merge_frameworks(self, input_data):
        merger = MergeStrategy('framework1.main', 'framework2.main')
        if self.merge_strategy == 'sequential':
            merged_output = merger.sequential_merge(input_data)
        elif self.merge_strategy == 'parallel':
            merged_output = merger.parallel_merge(input_data)
        elif self.merge_strategy == 'custom':
            from custom_merge import custom_logic
            merged_output = merger.custom_merge(input_data, custom_logic)
        else:
            raise ValueError(f"Unknown merge strategy: {self.merge_strategy}")
        return merged_output

    def build_agent(self, merged_output):
        os.makedirs(self.agent_dir, exist_ok=True)
        with open(os.path.join(self.agent_dir, 'output.txt'), 'w') as f:
            f.write(str(merged_output))

        with open(os.path.join(self.agent_dir, 'Dockerfile'), 'w') as f:
            f.write(f"""
            FROM python:3.9
            WORKDIR /app
            COPY . .
            CMD ["python", "-m", "agent"]
            """)

        with open(os.path.join(self.agent_dir, 'agent.py'), 'w') as f:
            f.write(f"""
            def run():
                with open('output.txt', 'r') as f:
                    output = f.read()
                print("Agent Running with Output:", output)

            if __name__ == "__main__":
                run()
            """)

    def deploy_agent(self):
        image_tag = f"{self.agent_name.lower()}_image"
        container_name = f"{self.agent_name.lower()}_container"

        self.docker_client.images.build(path=self.agent_dir, tag=image_tag)
        container = self.docker_client.containers.run(image_tag, name=container_name, detach=True)

        print(f"Agent '{self.agent_name}' has been deployed successfully.")
        print(f"Container ID: {container.id}")
        print(f"Run 'docker logs {container_name}' to view agent output.")

    def run(self, input_data):
        self.clone_repositories()
        merged_output = self.merge_frameworks(input_data)
        self.build_agent(merged_output)
        self.deploy_agent()
