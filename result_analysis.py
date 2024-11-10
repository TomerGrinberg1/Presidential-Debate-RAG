import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Function to load the candidate mapping from the real debate JSON
def load_candidates_from_real_json(file_path):
    candidate_mapping = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        real_debate_data = json.load(file)
        for entry in real_debate_data:
            question = entry.get("question", "")
            candidate = entry.get("candidate", "").lower()
            if question and candidate:
                candidate_mapping[question] = candidate
    return candidate_mapping

# Function to extract similarity scores and associate them with candidates
def extract_scores_by_candidate(file_path, candidate_mapping):
    scores = {'trump': [], 'biden': []}
    with open(file_path, 'r', encoding='utf-8') as file:
        debate_data = json.load(file)
        for entry in debate_data:
            question = entry.get("question", "")
            evaluation = entry.get("evaluation using Llama-3.2-90B-Vision-Instruct") or \
                         entry.get("evaluation using gpt 4o") 

            if evaluation and isinstance(evaluation, dict) and question:
                candidate = candidate_mapping.get(question, "unknown")
                if candidate in scores:
                    for model, eval_content in evaluation.items():
                        try:
                            if eval_content.strip():
                                eval_dict = json.loads(eval_content)
                                score = eval_dict.get("Similarity", None)
                                if score is not None:
                                    scores[candidate].append(score)
                        except json.JSONDecodeError:
                            pass
    return scores

# Function to create a summary DataFrame for plotting
def create_summary_dataframe(all_scores):
    data = []
    for model, methods in all_scores.items():
        for method, scores in methods.items():
            trump_scores = pd.Series(scores['trump'])
            biden_scores = pd.Series(scores['biden'])
            overall_mean = (trump_scores.mean() + biden_scores.mean()) / 2
            data.append({
                'Model': model,
                'Method': method,
                'Trump Mean': trump_scores.mean(),
                'Biden Mean': biden_scores.mean(),
                'Overall Mean': overall_mean
            })
    return pd.DataFrame(data)

# Plot mean scores for all models and methods
def plot_mean_scores(df):
    plt.figure(figsize=(14, 7))
    sns.barplot(x='Method', y='Overall Mean', hue='Model', data=df)
    plt.title('Overall Mean Similarity Scores for Each Model and Method')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plot candidate-specific mean scores for each model and method side by side
def plot_candidate_scores(df):
    for model in df['Model'].unique():
        subset = df[df['Model'] == model]
        
        # Create subplots
        fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=True)
        
        # Plot for Trump
        sns.barplot(x='Method', y='Trump Mean', data=subset, ax=axes[0], color='blue', alpha=0.6)
        axes[0].set_title(f'Trump Mean Similarity Scores - {model}')
        axes[0].set_xlabel('Method')
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)
        axes[0].set_ylabel('Mean Similarity Score')
        
        # Plot for Biden
        sns.barplot(x='Method', y='Biden Mean', data=subset, ax=axes[1], color='orange', alpha=0.6)
        axes[1].set_title(f'Biden Mean Similarity Scores - {model}')
        axes[1].set_xlabel('Method')
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)
        axes[1].set_ylabel('')

        # Adjust layout
        plt.tight_layout()
        plt.show()

# Main function to execute the workflow
def main():
    candidate_mapping = load_candidates_from_real_json('debate_final_json.json')
    json_files = {
        'GPT-4o': [
            'generated_debate_with_RAG_dense_using_gpt4o_evaluator.json',
            'generated_debate_with_RAG_sparse_using_gpt4o_evaluator.json',
            'generated_debate_with_RAG_hybrid_using_gpt4o_evaluator.json',
            'generated_debate_without_RAG_using_gpt4o_evaluator.json'
        ],
        'Llama-3.2-90B-Vision-Instruct': [
            'generated_debate_with_RAG_dense_using_Llama-3.2-90B-Vision-Instruct_evaluator.json',
            'generated_debate_with_RAG_sparse_using_Llama-3.2-90B-Vision-Instruct_evaluator.json',
            'generated_debate_with_RAG_hybrid_using_Llama-3.2-90B-Vision-Instruct_evaluator.json',
            'generated_debate_without_RAG_using_Llama-3.2-90B-Vision-Instruct_evaluator.json'
        ]
    }

    all_scores = {}
    for model, files in json_files.items():
        all_scores[model] = {}
        for file in files:
            method = file.split('_using_')[0].replace('generated_debate_with_', '').replace('generated_debate_without_', 'Without_RAG')
            candidate_scores = extract_scores_by_candidate(file, candidate_mapping)
            all_scores[model][method] = candidate_scores

    # Create a summary DataFrame
    summary_df = create_summary_dataframe(all_scores)

    # Plot the overall mean scores
    plot_mean_scores(summary_df)

    # Plot candidate-specific scores for each model and method side by side
    plot_candidate_scores(summary_df)

if __name__ == "__main__":
    main()
