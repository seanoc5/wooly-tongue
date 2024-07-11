# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
# working
from llama_index.core import SimpleDirectoryReader
from sentence_transformers import SentenceTransformer

documents = SimpleDirectoryReader("/opt/data/text").load_data()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)
print(embeddings)
