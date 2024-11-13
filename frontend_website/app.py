from flask import Flask, request, jsonify, render_template, send_from_directory

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from biden_agent import BidenAgent
from trump_agent import TrumpAgent

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
    else:
        generated_response = biden_agent.generate_response(prompt)

    # Access the single response directly
    answer = next(iter(generated_response.values()))

    # Store the answer for future use
    last_answers['candidate'] = candidate
    last_answers['previous_answer'] = answer

    return jsonify({"answer": answer})



# Load the JSON data when the app starts
with open('static/debate_final_json.json', 'r') as file:
    debate_data = json.load(file)


@app.route('/ask_question_game', methods=['POST'])
def ask_question_game():
    data = request.json
    question = data.get('question')
    candidate = data.get('candidate')

    if not question:
        return jsonify({"error": "Please provide a question"}), 400
    if not candidate:
        return jsonify({"error": "Please specify the candidate"}), 400

    # Search for the question and candidate in the JSON data
    for item in debate_data:
        if item['question'] == question and item['candidate'].lower() == candidate.lower():
            real_answer = item['answer']

            prompt = f"The question: {question}"

            # Generate a response based on the candidate selected
            if candidate == 'trump':
                generated_response = trump_agent.generate_response(prompt)
            else:
                generated_response = biden_agent.generate_response(prompt)

            # Access the single response directly
            fake_answer = next(iter(generated_response.values()))

            return jsonify({"realAnswer": real_answer, "fakeAnswer": fake_answer})

    # If no matching question or candidate is found
    return jsonify({"error": "Question or candidate not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
