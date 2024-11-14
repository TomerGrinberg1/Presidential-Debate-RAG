from flask import render_template

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.biden_agent import BidenAgent
from agents.trump_agent import TrumpAgent

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

trump_agent = TrumpAgent()
biden_agent = BidenAgent()


@app.route('/')
def chat():
    return render_template('chat.html')


@app.route('/game')
def game():
    return render_template('game.html')


# Store last answers for each candidate
last_answers = {
    'candidate': '',
    'previous_answer': ''
}


@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    candidate = data.get('candidate')
    usePreviousAnswer = data.get('usePreviousAnswer')

    if not question:
        return jsonify({"error": "Please provide a question"}), 400
    if not candidate:
        return jsonify({"error": "Please specify the candidate"}), 400

    # Construct prompt based on whether to use previous answer
    if usePreviousAnswer and last_answers['candidate']:
        prompt = f"The candidate {last_answers['candidate']} answered {last_answers['previous_answer']} \nThe new question is: {question}"
    else:
        prompt = f"The question: {question}"

    # Generate a response based on the candidate selected
    if candidate == 'trump':
        generated_response = trump_agent.generate_response(prompt)
        print(generated_response)
    else:
        generated_response = biden_agent.generate_response(prompt)

    # Access the single response directly
    answer = next(iter(generated_response.values()))

    # Store the answer for future use
    last_answers['candidate'] = candidate
    last_answers['previous_answer'] = answer

    return jsonify({"answer": answer})


# Load the JSON data when the app start

with open('debate simulations/generated_debate_with_RAG_dense_using_gpt4o_evaluator.json', 'r') as f:
    debate_data = json.load(f)


@app.route('/ask_question_game', methods=['POST'])
def ask_question_game():
    data = request.json
    question_item = data.get('questionItem')
    candidate = data.get('candidate')

    if not question_item:
        return jsonify({"error": "Please provide a question item"}), 400
    if not candidate:
        return jsonify({"error": "Please specify the candidate"}), 400

    # Retrieve 'real_answer' and 'generated_response' from the question item
    real_answer = question_item.get('real_answer')
    generated_responses = question_item.get('generated_response')

    if not real_answer or not generated_responses:
        return jsonify({"error": "Invalid question data"}), 400

    # Get the fake answer from 'generated_response'
    # For this example, we'll select the first model's response
    fake_answer = next(iter(generated_responses.values()))

    return jsonify({"realAnswer": real_answer, "fakeAnswer": fake_answer})


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
