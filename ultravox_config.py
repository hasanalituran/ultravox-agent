import random

SYSTEM_PROMPT = """Your name is Steven. You are a receptionist at TURAN Auto & Mobile Mechanics. Your job is as follows:
1. Answer all calls with a friendly, conversational approach. Address our company as us or we.
2. Provide helpful answers to customer inquiries. You MUST use the "retrieveFromVectorStore" tool for any service or company information requests. Do not make answers up!
"""

# AWS EC2 instance public IP address/port
toolsBaseUrl = "3.24.240.119:3005"; 

selected_tools = [
{
    "temporaryTool": {
      "modelToolName": "retrieveFromVectorStore",
      "description": "Retrieve documents from the vector store based on a query. Call this any time when you need information about our company, services and operation.",      
      "dynamicParameters": [
        {
          "name": "query",
          "location": "PARAMETER_LOCATION_BODY",
          "schema": {
            "description": "Query to search for in the vector store.",
            "type": "string",
          },
          "required": True
        },
      ],
      # "client": {},
      "http": {
          "baseUrlPattern": f"{toolsBaseUrl}/retrieve",
          "httpMethod": "POST",
        },
    }
  },
  {
    "tool_name": "hangUp"
  }
]
   
ULTRAVOX_CALL_CONFIG = {
    "systemPrompt": SYSTEM_PROMPT,
    "model": "fixie-ai/ultravox",
    "voice": "Mark",
    "temperature": 0.1,
    "firstSpeaker": "FIRST_SPEAKER_AGENT",
    "medium": {
        "twilio": {}
    },
    "selectedTools": selected_tools
}

AGENT_CONFIG = {
    "name": f"test-agent-{random.randint(1, 1000)}", 
    "callTemplate":{
        "systemPrompt": SYSTEM_PROMPT,
        "model": "fixie-ai/ultravox",
        "voice": "Mark",
        "temperature": 0.1,
        "medium": {
            "twilio": {}
        },
        "selectedTools": selected_tools,
        "maxDuration": "120s",
        "firstSpeakerSettings": {
            "agent": {
                "text": "Hello, this is Steven from TURAN Auto & Mobile Mechanics. How can I help you today?",
                "uninterruptible": True
            }
        },
        "recordingEnabled": False,
    }  
}