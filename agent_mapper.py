class AgentMapper:
    """
    This class maps recieved call service phone numbers to their respective agent ids.
    This is to be replaced by an actual database in the future.
    The agent ids are currently hardcoded for testing purposes.
    """

    agent_id_service_number_mapping = None
    agent_id_account_sid_mapping = None
    def __init__(self):
        if self.agent_id_service_number_mapping is None:
            self.agent_id_service_number_mapping = {
            "+61258503402": "3b12b38b-83b4-42d3-ab09-8b59847f87bc",
            # Add more mappings as needed
            }
        if self.agent_id_account_sid_mapping is None:
            self.agent_id_account_sid_mapping = {
            "ACa41b22d9db143b4e67cd27140ccc6157": "3b12b38b-83b4-42d3-ab09-8b59847f87bc",
            # Add more mappings as needed
            }
        

    def get_service_name(self, service_number=None, account_sid=None):
        """
        Get the agent id for a given service.
        """

        print(f"Service number: {service_number}")
        print(f"Account sid: {account_sid}")
        result = self.agent_id_service_number_mapping.get(service_number, None)

        if result is None:
            return self.agent_id_account_sid_mapping.get(account_sid, None)