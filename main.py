import argparse
from src.cli import GenesisCLI
from src.deploy_agent import AgentDeployer
import yaml

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Genesis - Universal AI Framework Merger')
    parser.add_argument('--server', action='store_true', help='Run Genesis in server mode')
    parser.add_argument('--host', default='0.0.0.0', help='Server host (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    parser.add_argument('--config', type=str, default='genesis_config.yaml', help='Path to the Genesis configuration file')
    parser.add_argument('--deploy', action='store_true', help='Merge frameworks and deploy the agent based on the config file')
    args = parser.parse_args()

    if args.server:
        try:
            from src.server import start_server
            start_server(host=args.host, port=args.port)
        except ImportError:
            print("Server dependencies not installed. Please run: pip install -r requirements.txt")
            exit(1)
    elif args.deploy:
        config = load_config(args.config)
        deployer = AgentDeployer(
            framework1_repo=config['repositories'][0]['url'],
            framework2_repo=config['repositories'][1]['url'],
            agent_name=config['agent_name'],
            merge_strategy=config['merge_strategy']['type']
        )
        input_data = config.get('input_data', {}).get('text', "")
        deployer.run(input_data)
    else:
        cli = GenesisCLI(config_path=args.config)
        cli.main_loop()
