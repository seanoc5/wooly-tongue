# https://chat.openai.com/share/117908b6-6937-48a4-98a4-9af703f60fc1

from transformers import BertModel, BertTokenizer
import torch
from scipy.spatial.distance import cosine

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to get word embeddings for a given word in a sentence
# def get_word_embedding(sentence, word):
def get_word_embedding(sentence):
    # Tokenize input
    inputs = tokenizer(sentence, return_tensors='pt')
    # Generate embeddings
    outputs = model(**inputs)
    # Extract embeddings
    embeddings = outputs.last_hidden_state.squeeze(0)
    # Find the token corresponding to the word
    word_tokens = tokenizer.tokenize(word)
    for i, token in enumerate(inputs['input_ids'][0]):
        if tokenizer.decode([token]) == word_tokens[0]:
            return embeddings[i]
    return None

# Function to find the most similar word
def find_most_similar_word(target_word, sentence1, sentence2):
    target_embedding = get_word_embedding(sentence1, target_word)
    if target_embedding is None:
        return "Word not found in the sentence."

    _, ids2 = get_word_embeddings(sentence2)
    tokens2 = [tokenizer.decode([id]) for id in ids2[0]]
    embeddings2, _ = get_word_embeddings(sentence2)

    max_similarity = -1
    most_similar_word = None
    # Compute similarities
    for j, emb in enumerate(embeddings2.squeeze(0)):
        sim = 1 - cosine(target_embedding.detach().numpy(), emb.detach().numpy())
        if sim > max_similarity:
            max_similarity = sim
            most_similar_word = tokens2[j]

    return most_similar_word, max_similarity

# Example usage
sentence1 = "The boy smiled at his teacher."
sentence2 = "The child was eating ice cream."
word_to_compare = "boy"

most_similar_word, similarity = find_most_similar_word(word_to_compare, sentence1, sentence2)
print(f"The most similar word to '{word_to_compare}' in the second sentence is '{most_similar_word}' with a similarity score of {similarity:.2f}.")
