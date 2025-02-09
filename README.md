**Genesis Framework**
Genesis is a universal meta-framework that merges two AI frameworks from GitHub repositories, combining their functionalities into a single deployable agent. It automates repository analysis, framework integration, and deployment using customizable merge strategies in a scalable, containerized environment.

**Features**
Merge Any AI Frameworks: Combine functionalities from two GitHub repositories seamlessly.
Customizable Merge Strategies: Choose from sequential, parallel, or custom merge logic.
Automated Deployment: Containerized deployment using Docker for isolated, conflict-free environments.
Developer-Friendly: Simple configuration with YAML and environment variables.
Open Source & Extensible: Easily customizable for new frameworks and use cases.
**Use Cases** 
AI-Powered Content & Research (NLP + Data Analysis)
Autonomous Coding & Debugging (AI Coding + Testing)
Social Media Automation with Market Insights (Twitter AI + Analytics)
Business Process Automation (LLMs + Decision-Making Agents)

**Quick Start**

**1. Install Prerequisites**
Ensure you have the following installed:

python --version    # Python 3.x
git --version       # Git
docker --version    # Docker
pip --version       # Pip

**2. Clone the Repository**
git clone https://github.com/GenesisAI/genesis-framework.git
cd genesis-framework

**3. Install Dependencies**
pip install -r requirements.txt

**4. Configure Environment**
Create a .env file in the root directory:

GITHUB_TOKEN=your_github_personal_access_token
DOCKER_HOST=unix:///var/run/docker.sock
MERGE_STRATEGY=sequential
LOG_LEVEL=INFO
AGENT_OUTPUT_PATH=./output/merged_agent_logs
API_KEY=your_api_key_here

**5. Set Up genesis_config.yaml**
agent_name: "MyMergedAgent"
repositories:
  - url: "https://github.com/user/framework1.git"
  - url: "https://github.com/user/framework2.git"
merge_strategy:
  type: "sequential"
deployment:
  containerization: true
  resources:
    cpu: 2
    memory: 4GB
logging:
  level: "INFO"
  output_path: "./logs/merged_agent.log"
**6. Deploy the Merged Agent**

**Merge Strategies**
Sequential: Framework 1 processes the input, and its output is passed to Framework 2.
Parallel: Both frameworks process the same input simultaneously, and the outputs are combined.
Custom: Define your own logic for merging frameworks in custom_merge.py.

**Example Output**

Agent 'MyMergedAgent' has been deployed successfully.
Container ID: e8d3c3f9d1a4
Run 'docker logs mymergedagent_container' to view agent output.


**Contributing**
Fork the repository.
Create a new branch: git checkout -b feature-branch.
Make your changes and commit: git commit -m "Add new feature".
Push to your fork: git push origin feature-branch.
Submit a pull request.
This project is licensed under the MIT License.

