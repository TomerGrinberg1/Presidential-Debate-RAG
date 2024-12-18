# Presidential Debate Simulation Using Retrieval-Augmented Generation (RAG)

This repository contains the code and resources for simulating the 2024 Trump-Biden presidential debate using Retrieval-Augmented Generation (RAG) techniques to refine chatbot models. This project leverages dense, sparse, and hybrid retrieval methods to improve the relevance and quality of generated responses. The primary goal is to produce generated responses that closely resemble real debate answers, both in content and style.

## Project Overview

### Abstract

This study presents an approach to simulating a U.S. presidential debate by employing Retrieval-Augmented Generation (RAG) to refine chatbot models that emulate debate participants. Data from a variety of public sources, including speeches, interviews, and statements, were collected to create a robust RAG database. We employed dense, sparse, and hybrid retrieval methods to enhance response quality. Evaluations were conducted using an "ask LLM" evaluation framework to compare RAG-augmented models with non-RAG models. Additionally, a web interface enables users to interact with simulated debate participants and assess the authenticity of responses.

### Key Objectives

1. *Data Collection*: Collect a diverse dataset of speeches, interviews, and public statements from the 2024 presidential candidates.
2. *RAG Setup*: Implement dense, sparse, and hybrid retrieval methods to enhance response accuracy and relevance.
3. *Evaluation*: Use an "ask LLM" evaluation framework with chain-of-thought reasoning to compare the effectiveness of RAG-augmented and non-RAG models.
4. *User Interaction*: Provide an interactive web interface for users to engage with the debate simulation.



## Related Works

RAG has emerged as a prominent method for reducing hallucinations in language models by grounding responses in 
reliable information sources. While dense retrieval methods have been commonly used, recent studies suggest the 
superiority of incorporating sparse methods such as BM25 in generating contextually accurate responses. Hybrid retrieval, 
which combines dense and sparse methods, has shown promising results in enhancing response quality.

## Methodology

### 1. Data Collection

Data for this project was collected from public sources such as the Miller Center and the White House. The data was pre-processed to remove noise, normalize format, and ensure high relevance to the debate context.

### 2. Retrieval-Augmented Generation (RAG) Setup

We implemented three RAG methods:
- *Dense Retrieval*: Uses Pinecone’s vector database with embeddings generated by e5 (https://huggingface.co/embaas/sentence-transformers-e5-large-v2).
- *Sparse Retrieval*: Based on the BM25 model, which scores document relevance based on term frequency and document length normalization.
- *Hybrid Retrieval*: Combines BM25 for exact lexical matching with Pinecone’s dense vector search to capture semantic similarity, providing a comprehensive relevance score.

### 3. Evaluation

Each question-response pair was parsed into JSON format, and LangChain semantic chunking was used to segment the data. Dense, sparse, and hybrid retrieval methods were applied, and results were evaluated through an "ask LLM" framework, prompting the model to compare generated and real responses using a chain-of-thought reasoning approach.

---

### BM25 Ranking Function

The BM25 score for a document \( d \) with respect to a query \( q \) is computed as:

$$
BM25(q, d) = \sum_{t \in q} IDF(t) \cdot \frac{TF(t, d) \cdot (k_1 + 1)}{TF(t, d) + k_1 \cdot (1 - b + b \cdot \frac{|d|}{avgdl})}
$$

Where:
- \( $$t$$ \): Terms in the query \( q \).
- \( $$IDF(t)$$ \): Inverse Document Frequency for term \( t \).
- \( $$TF(t, d)$$ \): Term Frequency of term \( t \) in document \( d \).
- \($$ |d|$$ \): Length of document \( d \).
- \( $$avgdl$$ \): Average document length across all documents.
- \( $$k_1 $$\) and \( b \): Hyperparameters controlling term frequency scaling and document length normalization, typically set to \( k_1 = 1.2 \) and \( b = 0.75 \).

### Hybrid Score Calculation

To balance lexical relevance (BM25) and semantic similarity (dense retrieval), we calculate a hybrid score as follows:

$$
HybridScore(q, d) = (1 - \alpha) \cdot BM25(q, d) + \alpha \cdot Dense(q, d)
$$

Where:
- \($$\alpha $$\): Weight parameter between 0 and 1, controlling the balance between BM25 and dense vector scores.
- \($$BM25(q, d)$$ \): Normalized BM25 score.
- \($$Dense(q, d)$$ \): Normalized dense retrieval score from a vector search.



---




## Evaluation

We assessed generated responses by comparing them to real debate answers from the candidates, using similarity scoring with an "ask LLM" evaluation approach. The evaluation measured dimensions like overlap in reasoning, style, and factual content. A chain-of-thought reasoning approach was employed to prompt the model to explain its similarity rating, improving the transparency and interpretability of the evaluation.

### Statistical Analysis

To further analyze the effectiveness of RAG augmentation, statistical tests were conducted:
- Paired t-tests were applied to compare scores across RAG and non-RAG setups.
- Difference scores were calculated for each method (RAG Hybrid, RAG Dense, RAG Sparse) versus the non-RAG setup for individual questions.

---

## Results

The experiments indicated that:
- RAG-augmented models showed a moderate increase in similarity scores over non-RAG models.
- Hybrid retrieval yielded the highest similarity scores, followed by sparse and dense retrieval methods.

## Future Work

This project demonstrates the potential of RAG for enhancing conversational AI in complex scenarios like debate simulations. Future work may involve:
1. Exploring larger pre-trained models and fine-tuning strategies.
2. Refining data collection and expanding to additional debate topics.
3. Implementing improved evaluation metrics for rhetorical analysis.

---

## Installation

1. Clone the repository:
   bash
   git clone https://github.com/TomerGrinberg1/Presidential-Debate-RAG.git
   
2. Navigate to the project directory:
   bash
   cd Presidential-Debate-RAG
   
3. Install dependencies:
   bash
   pip install -r requirements.txt
   

Here's an updated *Usage* section with details for running the RAG simulation and using the web interface, as well as specific instructions for setting up the debate generation process and accessing the Flask-based web interface.

---

## Usage

1. *Run the RAG Simulation*: Use the main script to initiate debate simulations with specified retrieval methods.
2. *Web Interface*: Access the interactive web interface to engage with simulated debate participants.
3. *Evaluate*: Use evaluation scripts to compare generated and real responses.


### Generating a Debate

To generate a debate, follow these steps:

1. *Enter your OpenAI API key*:
   - Open base_agent.py and enter your API key for GPT models.
   - The API key can be generated [here](https://github.com/settings/tokens?type=beta).

2. *Select models for candidate agents*:
   - Choose the models for the candidate agents (Trump and Biden) by updating trump_agent.py and biden_agent.py.

3. *Select the evaluation model*:
   - Specify the model to use for evaluation in eval_agent.py.

4. *Set Pinecone API information*:
   - Obtain the Pinecone API key from the project creators to access the dense index.
   - Add the Pinecone API information in main.py to enable dense retrieval.

5. *Choose a retrieval method*:
   - Select a retrieval method (dense, sparse, or hybrid) in main.py to determine how documents will be retrieved.

6. *Set the output JSON filename*:
   - In main.py, specify the filename where the generated debate JSON will be saved.

7. *Run the simulation*:
   - Go to the terminal and run the following command to start generating the debate:
     bash
     python main.py
     

### Web Interface Setup

1. *Install Flask*:
   - Make sure Flask is installed:
     bash
     pip install flask
     

2. *Run Flask*:
   - Start the Flask server to access the web interface:
     bash
     flask run
     
3. *Access the Web Interface*:
   - Open a web browser and go to http://127.0.0.1:5000 to interact with the simulated debate participants in real-time.

---

### 4. User Interaction

### 4.1 Chat Mode
- Accessible via chat.html.
- Users select a candidate (Trump or Biden) and ask a question.
- The question is sent to the server, is processed by the right agent, and a response is returned.
- Candidate responses are displayed, creating a simulated debate environment.

### 4.2 Game Mode
- Accessible via game.html.
- Users select a candidate (Trump or Biden) and a question.
- The question is sent to the server, is being searched in the file debate_final_json.json.
- If the question is found, the real answer is kept then we send the question to the right agent.
- The server returns two answers, one is the real answer and the other is a fake answer.
- Users guess the real answer between two candidates.
- Points are awarded for correct answers, with a final score displayed at the end of each round.

## User Interaction Setup
1. In the file base_agent.py, enter your token in the __init__ function of the BaseAgent class.

self.token = 'YOUR_TOKEN_HERE'


2) Navigate to the frontend_website directory:
bash
cd frontend_website


3) From there, you can run the app:
bash
python app.py

4) In order to change the simulation used for the game, add the JSON to the static folder, and apply changes in app.py and templates/game.html


Access the app at http://localhost:5001.

## Usage

- Navigate to the home page and select Chat or Game mode from the top navigation bar.
- In Chat mode, select a candidate and enter a question to view responses.
- In Game mode, select a candidate and try to guess the authentic answer among options presented.

---

Thak you all for reading 
Tomer Grinberg, Hadar Sugarman and Meital Abadi
