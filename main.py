import json
from agents.trump_agent import TrumpAgent
from agents.biden_agent import BidenAgent
from agents.eval_agent import EvalAgent
from RetrievalService import RetrievalService
import time 

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:

        debate_data = json.load(file)
    return debate_data

    
def create_rag_prompt(question, previous_response ,context, retrieved_context, candidate):
    return f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>

        Using the provided passages—sourced from interviews,
        statements, speeches, and addresses by the candidate—formulate a response to the specific debate question below.
        The response should be crafted by drawing upon {candidate}s words and ideas <|eot_id|><|start_header_id|>user<|end_header_id|>

        ## Passages:
        passage 1: {retrieved_context[0]}

        passage 2: {retrieved_context[1]}

        passage 3: {retrieved_context[2]}

        ## Context: {context}

        {previous_response}

        ## Question: {question}  <|eot_id|>

        ## Answer:
        """


def generate_debate(debate_data, trump_agent, biden_agent, eval_agent, trump_retrieval_service, biden_retrieval_service, retrieval_method=None):
    evaluations = []
    try:
        for i, entry in enumerate(debate_data):
            question = entry["question"]
            context = entry.get("context", "")
            real_answer = entry["answer"]
            candidate = entry["candidate"]
            previous_response = ""
            if "previous response" in context or "<previous response>" in context:
                if i > 0: 
                    previous_candidate = debate_data[i - 1]["candidate"]
                    previous_real_answer = debate_data[i - 1]["answer"]
                    previous_response = f" ## previous response from {previous_candidate}: \n {previous_real_answer}"
                
            print(f"\nProcessing question {i + 1} for {candidate.capitalize()}...")
            
            if candidate.lower() == "trump":
                # retrieved_passages = trump_retrieval_service.retrieve_relevant_documents(question, search_method=retrieval_method)
                print("Generating response from Trump agent...")
                generated_response = trump_agent.generate_response(
                    # create_rag_prompt(question, previous_response, context, retrieved_passages, "Donald Trump")
                    f"The question: {question} {previous_response} Context for the question: {context} "
                )
                eval_agent.candidate_name = "Donald Trump"
                evaluation = eval_agent.evaluate_response(real_answer, generated_response)

            elif candidate.lower() == "biden":
                # retrieved_passages = biden_retrieval_service.retrieve_relevant_documents(question, search_method=retrieval_method)
                print("Generating response from Biden agent...")
                generated_response = biden_agent.generate_response(
                    # create_rag_prompt(question, previous_response, context, retrieved_passages, "Joe Biden")
                    f"The question: {question} {previous_response} Context for the question: {context} "
                )
                eval_agent.candidate_name = "Joe Biden"
                evaluation = eval_agent.evaluate_response(real_answer, generated_response)

            # Append the evaluation result
            evaluations.append({
                "question": question,
                "real_answer": real_answer,
                "generated_response": generated_response,
                "evaluation using Llama-3.2-90B-Vision-Instruct": evaluation ############################TODO change here when changing the model
                # "evaluation using Llama-3.2-90B-Vision-Instruct": evaluation
            })

            ###############################TODO change here when changing the model
            # Save to JSON after each evaluation
            # with open(f'generated_debate_with_RAG_{retrieval_method}_using_Llama-3.2-90B-Vision-Instruct_evaluator.json', 'w') as json_file:
                # json.dump(evaluations, json_file, indent=4)
            # with open(f'generated_debate_with_RAG_{retrieval_method}_using_gpt4o_evaluator.json', 'w') as json_file: 
                # json.dump(evaluations, json_file, indent=4)
            with open(f'generated_debate_without_RAG_using_Llama-3.2-90B-Vision-Instruct_evaluator.json', 'w') as json_file:
                json.dump(evaluations, json_file, indent=4)
            print(f"Saved progress after question {i + 1}.")
            time.sleep(6)

    finally:
        trump_agent.close()
        biden_agent.close()
        eval_agent.close()
        ###############################TODO change here when changing the model

        print(f"Debate results saved to 'generated_debate_without_RAG_using_Llama-3.2-90B-Vision-Instruct_evaluator.json'.")

def main():
    debate_data = load_json_data("chunked data/debate_final_json.json")
  
    PINECONE_API_KEY = ''
    PINECONE_ENVIRONMENT = 'us-east-1' 
    PINECONE_INDEX_NAME_TRUMP = 'trumpe5index'
    PINECONE_INDEX_NAME_BIDEN = 'bidene5index'

    retrieval_service_trump = RetrievalService(
        index_dir='whoosh_index_trump',
        pinecone_index_name=PINECONE_INDEX_NAME_TRUMP,
        pinecone_api_key=PINECONE_API_KEY,
        pinecone_environment=PINECONE_ENVIRONMENT,
    )

    retrieval_service_biden = RetrievalService(
        index_dir='whoosh_index_biden',
        pinecone_index_name=PINECONE_INDEX_NAME_BIDEN,
        pinecone_api_key=PINECONE_API_KEY,
        pinecone_environment=PINECONE_ENVIRONMENT,
    )

    trump_agent = TrumpAgent()
    biden_agent = BidenAgent()
    eval_agent = EvalAgent()
    ###############################TODO change here when changing the model

    retrieval_method = "sparse"

    generate_debate(debate_data, trump_agent, biden_agent, eval_agent,retrieval_service_trump,retrieval_service_biden,retrieval_method )

if __name__ == "__main__":
    main()





