import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from LLM_API import ChatModelClient
def run_models_for_prompt(model_names, system_prompt, user_prompt):
    """
    Runs the given system and user prompt on all models listed in the array and prints the results.
    
    :param model_names: A list of model names.
    :param system_prompt: The system-level message.
    :param user_prompt: The user input prompt.
    """
    # Initialize the ChatModelClient
    token = ""
    endpoint = "https://models.inference.ai.azure.com"
    chat_client = ChatModelClient(endpoint, token)

    # Iterate over all model names and run the prompt
    for model_name in model_names:
        print(f"\nRunning model: {model_name}")
        try:
            response = chat_client.get_response(model_name, system_prompt, user_prompt)
            print(f"Response from {model_name}:\n{response}")
        except Exception as e:
            print(f"Failed to run {model_name}: {str(e)}")

    # Close the client connection
    chat_client.close()

    # Example Usage
if __name__ == "__main__":

    model_names=["gpt-4o"]
    # Define the system and user prompts
    system_prompt = "You are responding as Donald Trump in a simulated U.S. presidential debate. Answer the following question in Trump’s authentic style. Focus on:\
Content and Stance: Reflect Trump's political stance and viewpoints, particularly emphasizing [insert relevant topics, e.g., American jobs, economy, border security].\
Speaking Style and Tone: Use bold and assertive language, with phrases that are memorable and direct. Maintain a confident tone, using strong, decisive statements that\
      convey Trump's typical confidence and conviction.\
Rhetorical Approach: Incorporate repetition for emphasis, highlight achievements, and contrast with opponents.\
      Use plain language that is accessible, with a tone that conveys strength and resilience.\
Debate Question: [Insert the debate question here]\
Response:\
"
    user_prompt = "And please welcome the 45th president of the United States, Donald Trump. Gentlemen, thanks so much for being here. Let's begin the debate. And let's start with the issue that voters consistently say is their top concern, the economy. President Biden, inflation has slowed, but prices remain high. Since you took office, the price of essentials has increased. For example, a basket of groceries that cost $100, then, now costs more than $120. And typical home prices have jumped more than 30 percent. What do you say to voters who feel they are worse off under your presidency than they were under President Trump?																									"

    # Path to the JSON file containing model names
    real_response="We had the greatest economy in the history of our country. We have never done so well. Every – everybody was amazed by it. Other countries were copying us. We got hit with COVID. And when we did, we spent the money necessary so we wouldn't end up in a Great Depression, the likes of which we had in 1929. By the time we finished – so we did a great job. We got a lot of credit for the economy, a lot of credit for the military, and no wars and so many other things. Everything was rocking good. But the thing we never got the credit for, and we should have, is getting us out of that COVID mess. He created mandates – that was a disaster for our country. But other than that, we had – we had given them back a – a country where the stock market actually was higher than pre-COVID. And nobody thought that was even possible. The only jobs he created are for illegal immigrants and bounce-back jobs, they're bounced back from the COVID. He has not done a good job. He has done a poor job. And inflation's killing our country. It is absolutely killing us."
    generated_resopnse="Well, folks, let me tell you something very important. Under my administration, we built the greatest economy this country has ever seen. **The greatest!** We had record low unemployment, we were bringing jobs back to America, and we made sure that people kept more of their hard-earned money. We cut taxes big league, and we got rid of job-killing regulations. **We were winning!** Now look at what's happening under Biden. Prices are out of control! **Out of control!** People are paying more at the grocery store, at the gas pump, for their homes. It's a disaster, folks, an absolute disaster. And you know what? It didn’t have to be this way. We were energy independent, and we had a strong, strong border. **Now? Not so much.** We need to put America first, folks, not last. **America first!** Bring jobs back, stop inflation, secure our borders. That's how you fix the economy. That's how you take care of the American people. I did it once, and I can do it again. No doubt about it. **No doubt.**"
    evaluation_prompt= "You are a language model evaluating the similarity between a generated response and a real response from a U.S. presidential candidate, Donald Trump, in a debate.\
          Evaluate how closely the generated response matches the real response, focusing on:\
              Content Relevance: Does the generated response cover the main points and topics in the real answer?\
                  Stylistic Similarity: Does it use similar language, phrasing, or tone characteristic of Donald Trump's speaking style?\
                      Argument Alignment: Does the generated response follow the same line of reasoning and argument strength?\
                          Rate the similarity on a scale from 1 to 5,\
    where: 1: Very dissimilar - Few or no similarities in content, style, or argument.\
          2: Somewhat dissimilar - Minimal overlap in key points, tone, or style.\
              3: Moderately similar - Some similarities, with partial overlap in key points or style.\
                  4: Very similar - Strong overlap in both content and style, with minor deviations.\
                      5: Extremely similar – Nearly identical in content, style, and argumentation.\
                          Provide a brief explanation of the score based on these criteria. \
                            Real Response: [Insert the generated response here]\
                            Generated Response: [Insert the generated response here]\
    "
    model_names_json = "Model_names.json"
    user_prompt_for_eval= f"    Real Response: {real_response}\
                            Generated Response: {generated_resopnse}"

    # Run the models with the given prompt
    run_models_for_prompt(model_names_json, evaluation_prompt, user_prompt_for_eval)
