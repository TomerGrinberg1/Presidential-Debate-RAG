from LLM_API import ChatModelClient
class BaseAgent:
    def __init__(self, system_prompt, model_names):
        self.system_prompt = system_prompt
        self.token = ""
        self.endpoint = "https://models.inference.ai.azure.com"
        self.chat_client = ChatModelClient(self.endpoint, self.token)
        self.model_names = model_names

    def generate_response(self, user_prompt):
        response_dict = {}
        for model_name in self.model_names:
            print(f"\nRunning model: {model_name}")
            try:
                response = self.chat_client.get_response(model_name, self.system_prompt, user_prompt)
                response_dict[model_name] = response
                # print(f"Response :\n{response}")
            except Exception as e:
                print(f"Failed to run {model_name}: {str(e)}")
        return response_dict
    def close(self):
        """Close the client connection."""
        self.chat_client.close()