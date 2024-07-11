
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
# from llama_index
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.core import Settings

# from llama_index.core.embeddings import resolve_embed_model
# from llama_index.llms.ollama import Ollama

documents = SimpleDirectoryReader("/opt/data/text").load_data()

# bge embedding model
# Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# ollama
# Settings.llm = Ollama(model="mistral", request_timeout=30.0)

# llm = Ollama(model="llama2", request_timeout=30.0)

index = VectorStoreIndex.from_documents(
    documents,
)

print(f"Loaded {len(documents)} documents")
