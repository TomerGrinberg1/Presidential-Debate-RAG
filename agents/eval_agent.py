from base_agent import BaseAgent

class EvalAgent(BaseAgent):
    def __init__(self):
        self.candiate_name = ""
        system_prompt = (
            """
                You are a language model tasked with evaluating the similarity between a real response given by a U.S. presidential candidate, {self.candidate_name}, during a debate, and a generated response. Your goal is to assess how well the generated response mirrors the real response.

                Consider aspects such as the content, style, and reasoning used by the candidate, but do not limit yourself to fixed criteria. Each evaluation may emphasize different dimensions of similarity, depending on what stands out most in the given responses.

                After your analysis, rate the similarity on a scale from 1 to 5:
                - 1: Very dissimilar - Few or no similarities.
                - 2: Somewhat dissimilar - Minimal overlap.
                - 3: Moderately similar - Partial overlap.
                - 4: Very similar - Strong overlap with minor deviations.
                - 5: Extremely similar - Nearly identical.

                Provide your classification in the form of a JSON object, ensuring that your explanation details the relevant aspects of similarity or divergence. Use a chain of thought to arrive at your conclusions, detailing your reasoning step by step.
                Your response should be formatted as follows:
                {
                "Explanation": "string",
                "Similarity": int [1-5]
                }

                """
            )
        model_names = ["gpt-4o"]
        self.evaluate_model = "gpt-4o"
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