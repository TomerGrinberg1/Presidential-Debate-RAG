import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

class ChatModelClient:
    def __init__(self, endpoint, token):
        """
        Initializes the ChatModelClient with the given endpoint and token.
        
        :param endpoint: The Azure endpoint for the chat completions.
        :param token: The API token for authentication.
        """
        self.endpoint = endpoint
        self.token = token
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token),
        )

    def get_response(self, model_name, system_prompt, user_prompt, stream=True):
        """
        Generates a response from the chat model.
        
        :param model_name: The name of the model to use.
        :param system_prompt: The system-level message to set up the context.
        :param user_prompt: The user's message prompt.
        :param stream: Whether to stream the response (default is True).
        :return: The generated response text.
        """
        response = self.client.complete(
            stream=stream,
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=user_prompt),
            ],
            model=model_name,
        )

        result = ""
        for update in response:
            if update.choices:
                result += update.choices[0].delta.content or ""
        
        return result

    def close(self):
        """Closes the client connection."""
        self.client.close()



