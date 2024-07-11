# https://medium.com/@omargohan/ollama-adds-support-for-embeddings-d2646b9fc326

# Import the necessary modules
import ollama
import chromadb
import argparse

# Create an argument parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument("-p", "--prompt", type=str, required=True, help="Prompt to generate response for")
parser.add_argument("-m", "--model", type=str, default="mistral", help="LLM model to use for generation")
parser.add_argument("-e", "--embedding_model", type=str, default="mxbai-embed-large", help="Embedding model to use")
args = parser.parse_args()

# Create a ChromaDB client
client = chromadb.Client()

# Create a collection named "test"
collection = client.create_collection(name="test")

# Define the documents (this part is hardcoded for demostration purposes)
documents = ["Artificial intelligence in healthcare offers significant benefits such as improved diagnostic accuracy and speed, enabling earlier and more precise detection of diseases through the analysis of medical images and patient data.","AI-driven technologies enhance personalized patient care by analyzing genetic, clinical, and lifestyle data to create tailored treatment plans, and they also streamline administrative tasks, reducing paperwork and improving operational efficiency within healthcare organizations.","In drug discovery and development, AI accelerates the process by analyzing vast datasets to identify potential drug candidates, predict drug efficacy, and interactions, thereby saving resources and speeding up development.","Additionally, AI applications in healthcare can improve access to care, particularly in remote and underserved areas, through telemedicine services and remote patient monitoring, ensuring healthcare services are more accessible regardless of location."]

# Define the embedding model
embedding_model = args.embedding_model

# Add the documents and embeddings to the collection
for i, d in enumerate(documents):
 response = ollama.embeddings(model=embedding_model, prompt=d)
 embedding = response["embedding"]
 collection.add(
  ids=[str(i)],
  embeddings=[embedding],
  documents=[d]
 )

# Define the prompt
prompt = args.prompt

# Create embeddings for the prompt
response = ollama.embeddings(
 prompt=prompt,
 model=embedding_model
)

# Query the collection for the most similar document
results = collection.query(
 query_embeddings=[response["embedding"]],
 n_results=1
)

# Get the most similar document
data = results['documents'][0][0]

# Generate a response using the model
output = ollama.generate(
 model=args.model,
 prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

# Print the response
print(output['response'])
