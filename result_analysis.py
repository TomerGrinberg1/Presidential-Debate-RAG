import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats


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

# Function to extract similarity scores and calculate differences for each model with debug
def extract_scores_by_candidate(debate_data, candidate_mapping, model_type, method):
    scores = {'trump': [], 'biden': []}
    print(model_type, method)
    for entry in debate_data:
        question = entry.get("question", "")
        evaluation = entry.get(f"evaluation using {model_type}")

        if not question:
            print("Warning: Entry without a question found.")
            continue

        if evaluation:
            print(f"Processing entry with question: {question[:50]}...")
            candidate = candidate_mapping.get(question, "unknown")
            if candidate not in scores:
                print(f"Warning: Candidate '{candidate}' not recognized.")
                continue

            if isinstance(evaluation, dict):
                for model, eval_content in evaluation.items():
                    try:
                        if eval_content.strip():
                            eval_dict = json.loads(eval_content)
                            score = eval_dict.get("Similarity", None)
                            if score is not None:
                                scores[candidate].append(score)
                                print(f"Score for candidate '{candidate}' added: {score}")
                            else:
                                print(f"No 'Similarity' score found for {model}.")
                        else:
                            print(f"Empty evaluation content for {model}.")
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON for {model} in entry '{question[:50]}': {e}")
        else:
            print(f"No evaluation found for model '{model_type}' in entry with question '{question[:50]}'.")
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


# Plot mean similarity score for each method in each model
def plot_mean_similarity_scores(summary_df):
    # Separate data by model
    for model in summary_df['Model'].unique():
        plt.figure(figsize=(10, 6))
        model_data = summary_df[summary_df['Model'] == model]
        
        # Plot mean similarity scores for each method in this model
        sns.barplot(x='Method', y='Overall Mean', data=model_data)
        plt.title(f'Mean Similarity Scores for {model}')
        plt.xlabel('Retrieval Method')
        plt.ylabel('Mean Similarity Score')
        plt.ylim(0, 5)  # Assuming similarity scores are on a 1-5 scale
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Plot mean similarity score per candidate for each model and method
def plot_candidate_mean_scores(summary_df):
    for model in summary_df['Model'].unique():
        model_data = summary_df[summary_df['Model'] == model]
        
        fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=True)
        
        # Plot for Trump
        sns.barplot(x='Method', y='Trump Mean', data=model_data, ax=axes[0], color='skyblue', alpha=0.7)
        axes[0].set_title(f'Trump Mean Similarity Scores - {model}')
        axes[0].set_xlabel('Retrieval Method')
        axes[0].set_ylabel('Mean Similarity Score')
        axes[0].set_ylim(0, 5)  # Assuming scores are on a 1-5 scale
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)

        # Plot for Biden
        sns.barplot(x='Method', y='Biden Mean', data=model_data, ax=axes[1], color='orange', alpha=0.7)
        axes[1].set_title(f'Biden Mean Similarity Scores - {model}')
        axes[1].set_xlabel('Retrieval Method')
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)

        plt.suptitle(f'Mean Similarity Scores per Candidate for {model}')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
# import json
# import numpy as np
# from scipy import stats
# import matplotlib.pyplot as plt

# Function to load JSON data
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
# Function to extract scores and method for continuous histogram plotting
def extract_all_scores(file_without_rag, file_with_rag_list, candidate_mapping, model_type):
    all_scores = []
    
    # Load "Without RAG" scores
    data_without_rag = load_json(file_without_rag)
    scores_without_rag = extract_scores_by_candidate(data_without_rag, candidate_mapping, model_type)
    for candidate, scores in scores_without_rag.items():
        all_scores.extend([{'Method': 'Without RAG', 'Candidate': candidate, 'Score': score} for score in scores])

    # Load each RAG method scores
    for method, file_with_rag in file_with_rag_list.items():
        data_with_rag = load_json(file_with_rag)
        scores_with_rag = extract_scores_by_candidate(data_with_rag, candidate_mapping, model_type)
        for candidate, scores in scores_with_rag.items():
            all_scores.extend([{'Method': method, 'Candidate': candidate, 'Score': score} for score in scores])
    
    return pd.DataFrame(all_scores)

# Plotting function for continuous histogram of similarity scores for each method
def plot_histogram_by_method(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Score', hue='Method', kde=True, bins=10, palette='Set2')
    plt.title('Similarity Score Distribution by Retrieval Method')
    plt.xlabel('Similarity Score')
    plt.ylabel('Frequency')
    plt.legend(title='Method')
    plt.show()

# Plotting function for continuous histogram of similarity scores for each candidate within each method
def plot_histogram_by_candidate_and_method(df):
    methods = df['Method'].unique()
    for method in methods:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df[df['Method'] == method], x='Score', hue='Candidate', kde=True, bins=10, palette='Set1')
        plt.title(f'Similarity Score Distribution for {method}')
        plt.xlabel('Similarity Score')
        plt.ylabel('Frequency')
        plt.legend(title='Candidate')
        plt.show()




def scores_to_dataframe(all_scores):
    data = []
    for model, methods in all_scores.items():
        for method, candidate_scores in methods.items():
            for candidate, scores in candidate_scores.items():
                for score in scores:
                    data.append({
                        'Model': model,
                        'Method': method,
                        'Candidate': candidate,
                        'Score': score
                    })
    return pd.DataFrame(data)
# # Function to extract scores and calculate differences
def extract_score_differences(file_without_rag, file_with_rag_list, candidate_mapping, model_type):
    score_diffs = {method: [] for method in file_with_rag_list}
    
    data_without_rag = load_json(file_without_rag)
    scores_without_rag = extract_scores_by_candidate(data_without_rag, candidate_mapping, model_type)

    for method, file_with_rag in file_with_rag_list.items():
        data_with_rag = load_json(file_with_rag)
        scores_with_rag = extract_scores_by_candidate(data_with_rag, candidate_mapping, model_type)
        
        for candidate in scores_without_rag:
            for score_no_rag, score_with_rag in zip(scores_without_rag[candidate], scores_with_rag[candidate]):
                score_diffs[method].append(score_with_rag - score_no_rag)
    
    return score_diffs


# Function to perform paired t-tests and display results
def paired_t_test(score_diffs, model_name):
    print(f"--- Paired T-Test Results for {model_name} ---")
    for method, differences in score_diffs.items():
        mean_diff = np.mean(differences)
        t_stat, p_value = stats.ttest_rel(differences, [0] * len(differences))  # Testing against no difference
        print(f"Method: {method}")
        print(f"  Mean Difference: {mean_diff:.2f}")
        print(f"  T-statistic: {t_stat:.2f}, P-value: {p_value:.4f}")
        print("  Significance:", "Yes" if p_value < 0.05 else "No")
        print()
def calculate_score_differences_and_t_tests(all_scores):
    results = {}

    for model, methods in all_scores.items():
        print(f"--- Paired T-Test Results for {model} ---")
        results[model] = {}
        
        # Get the 'Without RAG' scores as the baseline
        scores_without_rag = methods['Without RAG']

        for method in ['RAG_dense', 'RAG_sparse', 'RAG_hybrid']:
            results[model][method] = {} 

            # Calculate differences for Trump
            trump_diffs = [
                with_rag - no_rag for with_rag, no_rag in zip(methods[method]['trump'], scores_without_rag['trump'])
            ]
            
            # Calculate differences for Biden
            biden_diffs = [
                with_rag - no_rag for with_rag, no_rag in zip(methods[method]['biden'], scores_without_rag['biden'])
            ]
            
            # Perform paired t-test for Trump
            t_stat_trump, p_value_trump = stats.ttest_rel(trump_diffs, [0] * len(trump_diffs))
            results[model][method]['Trump'] = {'Mean Difference': np.mean(trump_diffs), 'T-statistic': t_stat_trump, 'P-value': p_value_trump}
            
            # Perform paired t-test for Biden
            t_stat_biden, p_value_biden = stats.ttest_rel(biden_diffs, [0] * len(biden_diffs))
            results[model][method]['Biden'] = {'Mean Difference': np.mean(biden_diffs), 'T-statistic': t_stat_biden, 'P-value': p_value_biden}

            # Display results
            print(f"Method: {method}")
            print(f"  Trump - Mean Difference: {np.mean(trump_diffs):.2f}, T-statistic: {t_stat_trump:.2f}, P-value: {p_value_trump:.4f}")
            print("    Significance:", "Yes" if p_value_trump < 0.05 else "No")
            print(f"  Biden - Mean Difference: {np.mean(biden_diffs):.2f}, T-statistic: {t_stat_biden:.2f}, P-value: {p_value_biden:.4f}")
            print("    Significance:", "Yes" if p_value_biden < 0.05 else "No")
            print()
    
    return results


# Function to plot similarity distributions
def plot_similarity_distributions(all_scores):
    for model, methods in all_scores.items():
        fig, axes = plt.subplots(1, 4, figsize=(20, 5), sharey=True)
        fig.suptitle(f'Similarity Distributions for {model} - RAG Methods', fontsize=16)

        for i, (method, scores) in enumerate(methods.items()):
            ax = axes[i]
            # Combine Trump and Biden scores for overall KDE
            overall_scores = scores['trump'] + scores['biden']
            sns.kdeplot(overall_scores, ax=ax, fill=True, color='skyblue', label=f'{method}', alpha=0.6)
            
            # Mean and Std calculations
            mean_overall = np.mean(overall_scores)
            std_overall = np.std(overall_scores)
            
            ax.axvline(mean_overall, color='blue', linestyle='--', label=f'{method} Mean: {mean_overall:.2f}')
            
            ax.set_title(f'{method}')
            ax.set_xlabel('Similarity Score')
            ax.set_ylabel('Density')
            ax.legend(loc='upper right')

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

# Function to plot candidate-specific similarity distributions
def plot_candidate_distributions(all_scores):
    for model, methods in all_scores.items():
        fig, axes = plt.subplots(2, 4, figsize=(20, 10), sharey=True)
        fig.suptitle(f'Similarity Distributions by Candidate for {model} - RAG Methods', fontsize=16)

        for i, (method, scores) in enumerate(methods.items()):
            # Trump-specific KDE
            ax = axes[0, i]
            sns.kdeplot(scores['trump'], ax=ax, fill=True, color='blue', label=f'{method} (Trump)', alpha=0.6)
            
            # Calculate and plot mean
            mean_trump = np.mean(scores['trump'])
            ax.axvline(mean_trump, color='blue', linestyle='--', label=f'{method} Mean: {mean_trump:.2f}')
            
            ax.set_title(f'{method} - Trump')
            ax.set_xlabel('Similarity Score')
            ax.set_ylabel('Density')
            ax.legend(loc='upper right')

            # Biden-specific KDE
            ax = axes[1, i]
            sns.kdeplot(scores['biden'], ax=ax, fill=True, color='orange', label=f'{method} (Biden)', alpha=0.6)
            
            # Calculate and plot mean
            mean_biden = np.mean(scores['biden'])
            ax.axvline(mean_biden, color='orange', linestyle='--', label=f'{method} Mean: {mean_biden:.2f}')
            
            ax.set_title(f'{method} - Biden')
            ax.set_xlabel('Similarity Score')
            ax.set_ylabel('Density')
            ax.legend(loc='upper right')

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()
        # Function to plot similarity distributions with 'Without RAG' as background
def plot_similarity_with_background(all_scores):
    for model, methods in all_scores.items():
        fig, axes = plt.subplots(1, 3, figsize=(20, 5), sharey=True)
        fig.suptitle(f'Similarity Distributions for {model} - RAG Methods with "Without RAG" Background', fontsize=16)

        # Get 'Without RAG' scores for background
        without_rag_scores = methods['Without RAG']['trump'] + methods['Without RAG']['biden']

        for i, method in enumerate(['RAG_dense', 'RAG_sparse', 'RAG_hybrid']):
            ax = axes[i]

            # Plot 'Without RAG' as the background
            sns.kdeplot(without_rag_scores, ax=ax, fill=True, color='gray', label='Without RAG', alpha=0.3)
            mean_without_rag = np.mean(without_rag_scores)
            ax.axvline(mean_without_rag, color='gray', linestyle='--', label=f'Without RAG Mean: {mean_without_rag:.2f}')

            # Plot current RAG method scores
            rag_scores = methods[method]['trump'] + methods[method]['biden']
            sns.kdeplot(rag_scores, ax=ax, fill=True, color='skyblue', label=f'{method}', alpha=0.6)
            mean_rag = np.mean(rag_scores)
            ax.axvline(mean_rag, color='blue', linestyle='--', label=f'{method} Mean: {mean_rag:.2f}')

            ax.set_title(f'{method} vs. Without RAG')
            ax.set_xlabel('Similarity Score')
            ax.set_ylabel('Density')
            ax.legend(loc='upper right')

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

# Function to plot candidate-specific distributions with 'Without RAG' as background
def plot_candidate_distributions_with_background(all_scores):
    for model, methods in all_scores.items():
        fig, axes = plt.subplots(2, 3, figsize=(20, 10), sharey=True)
        fig.suptitle(f'Similarity Distributions by Candidate for {model} - RAG Methods with "Without RAG" Background', fontsize=16)

        # Get 'Without RAG' scores for background
        without_rag_trump = methods['Without RAG']['trump']
        without_rag_biden = methods['Without RAG']['biden']

        for i, method in enumerate(['RAG_dense', 'RAG_sparse', 'RAG_hybrid']):
            # Trump-specific KDE with 'Without RAG' background
            ax = axes[0, i]
            sns.kdeplot(without_rag_trump, ax=ax, fill=True, color='gray', label='Without RAG', alpha=0.3)
            mean_without_rag_trump = np.mean(without_rag_trump)
            ax.axvline(mean_without_rag_trump, color='gray', linestyle='--', label=f'Without RAG Mean: {mean_without_rag_trump:.2f}')

            # Plot RAG method for Trump
            rag_trump = methods[method]['trump']
            sns.kdeplot(rag_trump, ax=ax, fill=True, color='blue', label=f'{method} (Trump)', alpha=0.6)
            mean_rag_trump = np.mean(rag_trump)
            ax.axvline(mean_rag_trump, color='blue', linestyle='--', label=f'{method} Mean: {mean_rag_trump:.2f}')

            ax.set_title(f'{method} - Trump vs. Without RAG')
            ax.set_xlabel('Similarity Score')
            ax.set_ylabel('Density')
            ax.legend(loc='upper right')

            # Biden-specific KDE with 'Without RAG' background
            ax = axes[1, i]
            sns.kdeplot(without_rag_biden, ax=ax, fill=True, color='gray', label='Without RAG', alpha=0.3)
            mean_without_rag_biden = np.mean(without_rag_biden)
            ax.axvline(mean_without_rag_biden, color='gray', linestyle='--', label=f'Without RAG Mean: {mean_without_rag_biden:.2f}')

            # Plot RAG method for Biden
            rag_biden = methods[method]['biden']
            sns.kdeplot(rag_biden, ax=ax, fill=True, color='orange', label=f'{method} (Biden)', alpha=0.6)
            mean_rag_biden = np.mean(rag_biden)
            ax.axvline(mean_rag_biden, color='orange', linestyle='--', label=f'{method} Mean: {mean_rag_biden:.2f}')

            ax.set_title(f'{method} - Biden vs. Without RAG')
            ax.set_xlabel('Similarity Score')
            ax.set_ylabel('Density')
            ax.legend(loc='upper right')

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()



# Main function to execute the workflow
def main():
    candidate_mapping = load_candidates_from_real_json('debate_final_json.json')
    print(candidate_mapping)
    # Load data paths
    file_without_rag_llama = 'generated_debate_without_RAG_using_Llama-3.2-90B-Vision-Instruct_evaluator.json'
    file_without_rag_gpt4o = 'generated_debate_without_RAG_using_gpt4o_evaluator.json'
    
    file_with_rag_list_llama = {
        'RAG_dense': 'generated_debate_with_RAG_dense_using_Llama-3.2-90B-Vision-Instruct_evaluator.json',
        'RAG_sparse': 'generated_debate_with_RAG_sparse_using_Llama-3.2-90B-Vision-Instruct_evaluator.json',
        'RAG_hybrid': 'generated_debate_with_RAG_hybrid_using_Llama-3.2-90B-Vision-Instruct_evaluator.json'
    }
    file_with_rag_list_gpt4o = {
        'RAG_dense': 'generated_debate_with_RAG_dense_using_gpt4o_evaluator.json',
        'RAG_sparse': 'generated_debate_with_RAG_sparse_using_gpt4o_evaluator.json',
        'RAG_hybrid': 'generated_debate_with_RAG_hybrid_using_gpt4o_evaluator.json'
    }

   # Extract scores for "Without RAG" and each RAG method
    scores_without_rag_llama = extract_scores_by_candidate(load_json(file_without_rag_llama), candidate_mapping, "Llama-3.2-90B-Vision-Instruct","")
    scores_without_rag_gpt4o = extract_scores_by_candidate(load_json(file_without_rag_gpt4o), candidate_mapping, "gpt 4o","")
    scores_with_rag_llama = {method: extract_scores_by_candidate(load_json(file_with_rag_list_llama[method]), candidate_mapping, "Llama-3.2-90B-Vision-Instruct", method) for method in file_with_rag_list_llama}
    scores_with_rag_gpt4o = {method: extract_scores_by_candidate(load_json(file_with_rag_list_gpt4o[method]), candidate_mapping, "gpt 4o", method) for method in file_with_rag_list_gpt4o}

    # Integrate "Without RAG" scores into the score dictionary for each model
    all_scores = {
        "Llama-3.2-90B-Vision-Instruct": {"Without RAG": scores_without_rag_llama, **scores_with_rag_llama},
        "GPT-4o": {"Without RAG": scores_without_rag_gpt4o, **scores_with_rag_gpt4o}
    }
    print(all_scores)
   
    test_results = calculate_score_differences_and_t_tests(all_scores)
    print(test_results)
    # Plot overall similarity distributions with 'Without RAG' as background
    plot_similarity_with_background(all_scores)

    # Plot candidate-specific distributions with 'Without RAG' as background
    plot_candidate_distributions_with_background(all_scores)



if __name__ == "__main__":
    main()