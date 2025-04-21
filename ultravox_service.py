import requests
import os, json
from dotenv import load_dotenv
from ultravox_config import ULTRAVOX_CALL_CONFIG, AGENT_CONFIG

load_dotenv()

def create_ultravox_call():
    """
    Create a call using the Ultravox API with default configuration.
    """
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": os.getenv("ULTRAVOX_API_KEY"),
    }
    response = requests.post(os.getenv("ULTRAVOX_API_URL"), headers=headers, json=ULTRAVOX_CALL_CONFIG)
    response.raise_for_status()
    return response.json()

def create_ultravox_call_with_agent(agent_id:str):
    """
    Create a call using the Ultravox API with a specific agent ID.
    """
    request_url = f"https://api.ultravox.ai/api/agents/{agent_id}/calls"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": os.getenv("ULTRAVOX_API_KEY"),
    }
    response = requests.post(request_url, headers=headers)
    response.raise_for_status()

    print("Agent call created successfully")
    print("Response:", response.json())

    return response.json()

def create_agent():
    """
    Create an agent using the Ultravox API.
    """

    base_url = 'https://api.ultravox.ai/api/agents'

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": os.getenv("ULTRAVOX_API_KEY"),
    }
    
    try:
        print("Creating agent with config:", json.dumps(AGENT_CONFIG, indent=2))
        response = requests.post(base_url, headers=headers, json=AGENT_CONFIG)
        response.raise_for_status()

        print("Agent created successfully")
        print("Response:", response.json())

        return response.json()
    except Exception as e:
        print("Error creating agent:", str(e))
        return None
    
def list_agents():
    """
    List all agents using the Ultravox API.
    """
    base_url = 'https://api.ultravox.ai/api/agents'

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": os.getenv("ULTRAVOX_API_KEY"),
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()

        return response.json()
    except Exception as e:
        print("Error listing agents:", str(e))
        return None
   