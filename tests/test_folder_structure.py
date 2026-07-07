import os

def test_repository_layout_folders_exist():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Required top level folders
    required_folders = [
        "config",
        "core",
        "database",
        "events",
        "agents",
        "tests"
    ]
    
    for folder in required_folders:
        folder_path = os.path.join(base_dir, folder)
        assert os.path.exists(folder_path), f"Required folder '{folder}' does not exist."
        assert os.path.isdir(folder_path), f"Path '{folder}' is not a directory."

def test_agents_sandbox_directories_exist():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    agents_dir = os.path.join(base_dir, "agents")
    
    required_agents = [
        "search",
        "audit",
        "niche",
        "scoring",
        "contact",
        "email_validation",
        "prototype",
        "email",
        "followup",
        "crm",
        "reporting",
        "notification"
    ]
    
    for agent in required_agents:
        agent_path = os.path.join(agents_dir, agent)
        assert os.path.exists(agent_path), f"Agent sandbox '{agent}' does not exist."
        assert os.path.isdir(agent_path), f"Agent path '{agent}' is not a directory."
