class AgentMapper:
    """
    This class maps recieved call service phone numbers to their respective agent ids.
    This is to be replaced by an actual database in the future.
    The agent ids are currently hardcoded for testing purposes.
    """

    agent_id_service_id_mapping: dict[str, str] = None
    
    def __init__(self):
        if self.agent_id_service_id_mapping is None:
            self.agent_id_service_id_mapping = {
            "+61258503402": "02d42275-2547-4d31-97df-8e986f2c7d67",
            "ACa41b22d9db143b4e67cd27140ccc6157": "02d42275-2547-4d31-97df-8e986f2c7d67",
        }
       
    def get_service_agent_id(self, service_number, account_sid):
        """
        Get the agent id for a given service.
        """

        print(f"Service number: {service_number}")
        print(f"Account sid: {account_sid}")

        result = self.agent_id_service_id_mapping.get(service_number, None) or self.agent_id_service_id_mapping.get(account_sid, None)

        if result is None:
            raise ValueError(f"Agent ID not found for the given service number: {service_number} or account SID: {account_sid}")
        
        return result