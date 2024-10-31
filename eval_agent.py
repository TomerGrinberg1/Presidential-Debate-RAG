from base_agent import BaseAgent

class EvalAgent(BaseAgent):
    def __init__(self):
        self.candiate_name = ""
        system_prompt = (
            "You are a language model evaluating the similarity between a generated response and a real response from a U.S. presidential candidate, "
            f"{self.candidate_name}, in a debate. Evaluate how closely the generated response matches the real response, focusing on:\n"
            "- **Content Relevance**: Does the generated response cover the main points and topics in the real answer?\n"
            "- **Stylistic Similarity**: Does it use similar language, phrasing, or tone characteristic of {self.candidate_name}'s speaking style?\n"
            "- **Argument Alignment**: Does the generated response follow the same line of reasoning and argument strength?\n"
            "\n"
            "Rate each category on a scale from 1 to 5:\n"
            "- 1: Very dissimilar - Few or no similarities.\n"
            "- 2: Somewhat dissimilar - Minimal overlap.\n"
            "- 3: Moderately similar - Partial overlap.\n"
            "- 4: Very similar - Strong overlap with minor deviations.\n"
            "- 5: Extremely similar - Nearly identical.\n"
            "\n"
            "After analyzing the text, provide your classification and explanation for each decision in the following JSON format. "
            "Ensure that every category has both an explanation and a score:\n"
            "\n"
            "{\n"
            '  "Content Relevance Explanation": "string",\n'
            '  "Content Relevance Score": int,\n'
            '  "Stylistic Similarity Explanation": "string",\n'
            '  "Stylistic Similarity Score": int,\n'
            '  "Argument Alignment Explanation": "string",\n'
            '  "Argument Alignment Score": int,\n'
            '  "Overall Similarity Explanation": "string",\n'
            '  "Overall Similarity Score": int\n'
            "}\n"
            "\n"
            "Provide a brief explanation of the score based on these criteria."
            )
        model_names = ["gpt-4o"]
        self.evaluate_model = "Llama-3.2-90B-Vision-Instruct"
        super().__init__(system_prompt, model_names)
        
    def evaluate_response(self, real_response, generated_response):
        """
        Evaluates the generated response compared to the real response for each model
        and provides feedback with a score for each model.
        
        :param real_response: The real response text from the candidate.
        :param generated_response: The generated response to be evaluated.
        :return: A dictionary containing the feedback score and explanation for each model.
        """
        # Construct the user prompt with both responses
        user_prompt = (
            f"Real Response: {real_response}\n"
            f"Generated Response: {generated_response}"
        )

        # Dictionary to store feedback from each model
        eval_response_dict = {}

        # Iterate over all models and generate feedback
        for model_name, response in generated_response.items():
            print(f"\nEvaluating response from: {model_name}")
            try:
                user_prompt = (
            f"Real Response: {real_response}\n"
            f"Generated Response: {response}"
        )
                # Pass user prompt and system prompt to each model
                eval_response = self.chat_client.get_response(self.evaluate_model, self.system_prompt, user_prompt)
                eval_response_dict[model_name] = eval_response
                # print(f"Feedback from {model_name}:\n{eval_response}")
            except Exception as e:
                print(f"Failed to evaluate with {model_name}: {str(e)}")
        
        # Close the client connection after all models have been evaluated
        
        return eval_response_dict