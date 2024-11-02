import json
from trump_agent import TrumpAgent
from biden_agent import BidenAgent
from eval_agent import EvalAgent
from RetrievalService import RetrievalService
import time 
# Load debate data from JSON file
def load_debate_data(file_path):
    with open(file_path, 'r') as file:
        debate_data = json.load(file)
    return debate_data

    

def generate_debate(debate_data, trump_agent, biden_agent, eval_agent, retrieval_service=None, retrieval_method=None):
    evaluations = []  # List to store all evaluation results

    try:
        # Iterate through each debate question in the JSON data
        for i, entry in enumerate(debate_data):
            question = entry["question"]
            context = entry.get("context", "")
            real_answer = entry["answer"]
            candidate = entry["candidate"]

            # Check if context contains the phrase "previous response" or "<previous response>"
            if "previous response" in context or "<previous response>" in context:
                if i > 0:  # Ensure there is a previous response to reference
                    previous_candidate = debate_data[i - 1]["candidate"]
                    previous_real_answer = debate_data[i - 1]["answer"]
                    question += f" ## previous response from {previous_candidate}: \n {previous_real_answer}"

            print(f"\nProcessing question {i + 1} for {candidate.capitalize()}...")

            if candidate.lower() == "trump":
                print("Generating response from Trump agent...")
                generated_response = trump_agent.generate_response(
                    f"The question: {question} Context for the question: {context}"
                )
                print("Trump Generated Response:", generated_response)

                # Evaluate Trump's response
                eval_agent.candidate_name = "Donald Trump"
                evaluation = eval_agent.evaluate_response(real_answer, generated_response)
                print("\nEvaluation Feedback for Trump Response:")
                print(evaluation)

                # Append to evaluations list
                evaluations.append({
                    "question": question,
                    "real_answer": real_answer,
                    "generated_response": generated_response,
                    "evaluation": evaluation
                })
                time.sleep(6)

            elif candidate.lower() == "biden":
                print("Generating response from Biden agent...")
                generated_response = biden_agent.generate_response(
                    f"The question: {question} Context for the question: {context}"
                )
                print("Biden Generated Response:", generated_response)

                # Evaluate Biden's response
                eval_agent.candidate_name = "Joe Biden"
                evaluation = eval_agent.evaluate_response(real_answer, generated_response)
                print("\nEvaluation Feedback for Biden Response:")
                print(evaluation)

                # Append to evaluations list
                evaluations.append({
                    "question": question,
                    "real_answer": real_answer,
                    "generated_response": generated_response,
                    "evaluation": evaluation
                })
                time.sleep(6)

    finally:
        # Ensure all agents are closed after the debate processing
        trump_agent.close()
        biden_agent.close()
        eval_agent.close()

        # Save evaluations to JSON file
        with open('generated_debate_without_RAG.json', 'w') as json_file:
            json.dump(evaluations, json_file, indent=4)
        print("Debate results saved to 'generated_debate_without_RAG.json'.")

def main():
    # Load the debate questions and answers
    debate_data = load_debate_data("debate_final_json.json")
    # Replace these with your Pinecone details
    # PINECONE_API_KEY = ''
    # PINECONE_ENVIRONMENT = 'us-east-1'  # e.g., 'us-west1-gcp'
    # PINECONE_INDEX_NAME = 'trumpindex'

# Initialize the retrieval service
    # retrieval_service = RetrievalService(
    #     index_dir='whoosh_index',
    #     pinecone_index_name=PINECONE_INDEX_NAME,
    #     pinecone_api_key=PINECONE_API_KEY,
    #     pinecone_environment=PINECONE_ENVIRONMENT,
    # )

    
    # Initialize the agents
    trump_agent = TrumpAgent()
    biden_agent = BidenAgent()
    eval_agent = EvalAgent()
    retrieval_method = "hybrid"
    # Call the generate_debate function
    generate_debate(debate_data, trump_agent, biden_agent, eval_agent)

if __name__ == "__main__":
    main()





# debate_data = load_debate_data("debate_final_json.json")

# # Initialize the agents and Pinecone index (replace 'index' with your actual Pinecone index instance)
# trump_agent = TrumpAgent()
# biden_agent = BidenAgent()
# eval_agent = EvalAgent()
# # index = initialize_pinecone_index()  # Replace with your index initialization if needed

# try:
#     # Iterate through each debate question in the JSON data
#     for i, entry in enumerate(debate_data):
#         question = entry["question"]
#         context = entry.get("context", "")
#         real_answer = entry["answer"]
#         candidate = entry["candidate"]

#         # Generate the embedding for the question
#         print(f"\nProcessing question {i + 1} for {candidate.capitalize()}...")
#         top_completions = query_index(question, index)

#         # Format the retrieved completions as context
#         retrieved_context = "\n".join(top_completions)

#         # Choose the agent based on the candidate and generate a response
#         if candidate.lower() == "trump":
#             print("Generating response from Trump agent...")
#             generated_response = trump_agent.generate_response(
#                 f"The question: {question}\nContext for the question: {context}\nRetrieved context: {retrieved_context}"
#             )
#             print("Trump Generated Response:", generated_response)

#             # Evaluate Trump's response
#             eval_agent.candidate_name = "Donald Trump"
#             evaluation = eval_agent.evaluate_response(real_answer, generated_response)
#             print("\nEvaluation Feedback for Trump Response:")
#             print(evaluation)

#         elif candidate.lower() == "biden":
#             print("Generating response from Biden agent...")
#             generated_response = biden_agent.generate_response(
#                 f"The question: {question}\nContext for the question: {context}\nRetrieved context: {retrieved_context}"
#             )
#             print("Biden Generated Response:", generated_response)

#             # Evaluate Biden's response
#             eval_agent.candidate_name = "Joe Biden"
#             evaluation = eval_agent.evaluate_response(real_answer, generated_response)
#             print("\nEvaluation Feedback for Biden Response:")
#             print(evaluation)

# finally:
#     # Ensure all agents are closed after the debate processing
#     trump_agent.close()
#     biden_agent.close()
#     eval_agent.close()