import requests
from bs4 import BeautifulSoup
import json
import os
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util


def load_debate_data(file_path):
    with open(file_path, 'r') as file:
        debate_data = json.load(file)
    return debate_data
# Instantiate KeyBERT
kw_model = KeyBERT()
model = SentenceTransformer('intfloat/e5-large')  # A lightweight model for semantic similarity



def is_real_question(question_text):
    """
    Determines if a question is a real question or just a follow-up.
    """
    follow_up_phrases = ["President Trump?", "President Biden?", "requested to respond", "responds to previous", "no question"]
    return not any(phrase in question_text for phrase in follow_up_phrases)

def extract_topics_with_keybert(question, num_topics=1):
    """
    Extracts topics from a debate question using KeyBERT.
    
    Parameters:
    - question (str): The debate question.
    - num_topics (int): The number of topics to extract.
    
    Returns:
    - list: A list of extracted topics.
    """
    keywords = kw_model.extract_keywords(question, keyphrase_ngram_range=(1, 3), stop_words='english', top_n=num_topics)
    topics = [keyword[0] for keyword in keywords]
    return topics



def remove_semantic_duplicates(topics, similarity_threshold=0.75):
    """
    Removes semantic duplicates from a list of topics using sentence embeddings.
    
    Parameters:
    - topics (list): List of topic strings.
    - similarity_threshold (float): The threshold for semantic similarity to consider topics as duplicates.
    
    Returns:
    - list: A list of unique topics.
    """
    unique_topics = []
    topic_embeddings = model.encode(topics, convert_to_tensor=True)

    for i, topic in enumerate(topics):
        is_duplicate = False
        for j, unique_topic in enumerate(unique_topics):
            similarity = util.pytorch_cos_sim(topic_embeddings[i], model.encode(unique_topic))[0][0].item()
            if similarity > similarity_threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_topics.append(topic)

    return unique_topics




def search_articles(president_name, topic):
    # Create a search query string
    query = f"{president_name}+{topic}".replace(" ", "+")
    search_url = f"https://www.whitehouse.gov/?s={query}"

    # Step 1: Extract article links from the search results page
    response = requests.get(search_url)
    articles_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all <h2> tags with the class 'entry-title'
        article_links = []
        for entry in soup.find_all('h2', class_='entry-title'):
            link = entry.find('a', href=True)
            if link and link['href'] not in article_links:
                article_links.append(link['href'])

        print(f"Found {len(article_links)} articles for '{president_name}' and '{topic}'.")
        
        # Step 2: Visit each article and extract the title and content inside the <section class="body-content">
        for i, article_url in enumerate(article_links):
            print(f"\nExtracting content from Article {i+1}: {article_url}")
            article_response = requests.get(article_url)
            if article_response.status_code == 200:
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                
                # Extract the title
                title_tag = article_soup.find('h1')
                title = title_tag.get_text(strip=True) if title_tag else "No title found"
                
                # Extract content from <section class="body-content">
                body_content = article_soup.find('section', class_='body-content')
                if body_content:
                    paragraphs = body_content.find_all('p')  # Extract <p> tags within this section
                    content_text = ' '.join(para.get_text() for para in paragraphs)
                    
                    # Append article data to the list without the 'url'
                    articles_data.append({
                        'title': title,
                        'topic': topic,
                        'content': content_text
                    })
                else:
                    print("No content found in the specified section.")
            else:
                print(f"Failed to retrieve the article at {article_url}")

        # Step 3: Ensure the folder 'scraped_articles' exists
        if not os.path.exists('scraped_articles'):
            os.makedirs('scraped_articles')

        # Save the articles data to a JSON file inside 'scraped_articles' folder
        filename = f'scraped_articles/articles_content_{president_name}_{topic}.json'.replace(" ", "_")
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(articles_data, json_file, ensure_ascii=False, indent=4)

        print(f"\nArticle contents have been saved to '{filename}'.")
    else:
        print("Failed to retrieve the search results page.")

# # Example usage:
# search_articles("biden", "immigration")
# search_articles("trump", "economy")
# Extract topics for each question and print them
debate_json = load_debate_data('debate_final_json.json')

# Compile all topics from all questions into an array
all_topics = []

# Extract topics for each real question and compile them into the array
for entry in debate_json:
    question = entry['question']
    if is_real_question(question):
        topics = extract_topics_with_keybert(question)
        entry['topics'] = topics  # Add the topics back to the entry
        all_topics.extend(topics)  # Add the topics to the combined array

# Remove duplicate and semantical duplicate topics from the combined list
all_topics_unique = remove_semantic_duplicates(list(set(all_topics)))

# Save the modified debate JSON to a new file (or keep it in memory)
with open('debate_with_topics.json', 'w', encoding='utf-8') as f:
    json.dump(debate_json, f, ensure_ascii=False, indent=4)

# Print a preview of the modified data and the final array of unique topics
extracted_topics = [entry['topics'] for entry in debate_json if 'topics' in entry]

# Flatten the extracted topics list for searching articles
flattened_extracted_topics = [topic for sublist in extracted_topics for topic in sublist]

# Ensure no duplicates remain in the topic list
final_unique_topics = remove_semantic_duplicates(list(set(flattened_extracted_topics)))

# Run `search_articles` for each candidate and topic
candidates = ["Trump", "Biden"]
for candidate in candidates:
    for topic in final_unique_topics:
        search_articles(candidate, topic)  # Adjust this to call your actual `search_articles` function
        print(f"Searching articles for {candidate} on topic: {topic}")


