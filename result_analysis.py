import json
import statistics
import matplotlib.pyplot as plt
import seaborn as sns

# Set academic-style theme for Seaborn plots
sns.set_theme(style="whitegrid", context="paper")

def load_json_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_similarity_scores(debate_data):
    """Extract similarity scores from the debate data."""
    scores = []
    for entry in debate_data:
        evaluation = entry.get("evaluation", {})
        if isinstance(evaluation, dict):
            for model, eval_content in evaluation.items():
                try:
                    # Check if the content is a valid JSON string
                    if eval_content.strip():
                        eval_dict = json.loads(eval_content)
                        score = eval_dict.get("Similarity", None)
                        if score is not None:
                            scores.append(score)
                    else:
                        print(f"Warning: Empty evaluation content for model '{model}' in entry '{entry.get('question', 'unknown question')}'")
                except json.JSONDecodeError:
                    print(f"Error: Invalid JSON format for model '{model}' in entry '{entry.get('question', 'unknown question')}'")
                    # Optional: Log or save the invalid JSON to a file for further inspection
                    with open('invalid_json_log.txt', 'a') as log_file:
                        log_file.write(f"Model: {model}, Entry: {entry.get('question', 'unknown question')}\n{eval_content}\n\n")
    return scores

def analyze_scores(scores):
    """Analyze and visualize the similarity scores for academic presentation."""
    if not scores:
        print("No similarity scores found.")
        return

    print(f"Total Responses Analyzed: {len(scores)}")
    print(f"Average Similarity Score: {statistics.mean(scores):.2f}")
    print(f"Median Similarity Score: {statistics.median(scores):.2f}")

    # Score distribution as a histogram with academic-style layout
    plt.figure(figsize=(8, 4))
    plt.suptitle('Evaluation of Generated Debate Without RAG', fontsize=16, y=1.05)
    sns.histplot(scores, bins=5, kde=True, color="dodgerblue")
    plt.title('Distribution of Similarity Scores', fontsize=14)
    plt.xlabel('Similarity Score', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(range(1, 6))
    plt.tight_layout()
    plt.savefig('histogram_similarity_scores.png', dpi=300)  # Save for academic use
    plt.show()

    # Box plot for academic presentation
    plt.figure(figsize=(8, 2))
    plt.suptitle('Evaluation of Generated Debate Without RAG', fontsize=16, y=1.2)
    sns.boxplot(x=scores, color="lightgreen")
    plt.title('Box Plot of Similarity Scores', fontsize=14)
    plt.xlabel('Similarity Score', fontsize=12)
    plt.tight_layout()
    plt.savefig('boxplot_similarity_scores.png', dpi=300)  # Save for academic use
    plt.show()

    # Violin plot for a detailed distribution view
    plt.figure(figsize=(8, 4))
    plt.suptitle('Evaluation of Generated Debate Without RAG', fontsize=16, y=1.05)
    sns.violinplot(x=scores, color="lightcoral")
    plt.title('Violin Plot of Similarity Scores', fontsize=14)
    plt.xlabel('Similarity Score', fontsize=12)
    plt.tight_layout()
    plt.savefig('violinplot_similarity_scores.png', dpi=300)  # Save for academic use
    plt.show()

def main():
    # Load the JSON data from the generated debate file
    debate_data = load_json_data('generated_debate_without_RAG.json')

    # Extract similarity scores
    scores = extract_similarity_scores(debate_data)

    # Analyze and visualize the scores
    analyze_scores(scores)

if __name__ == "__main__":
    main()
