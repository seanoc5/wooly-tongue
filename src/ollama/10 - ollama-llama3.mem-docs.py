# from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder
# WORKING

from haystack import Document, Pipeline
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack_integrations.components.embedders.ollama.document_embedder import OllamaDocumentEmbedder
from haystack_integrations.components.embedders.ollama.text_embedder import OllamaTextEmbedder

emb_model = 'llama3'
embedder = OllamaTextEmbedder(model=emb_model )

result = embedder.run(
    text="What do llamas say once you have thanked them? No probllama!"
)

print(result["embedding"])


# In order to run this example, you will need to have an instance of Ollama running with
# an embedding model downloaded. Use the following commands to serve the nomic-embed-text model with Ollama
#
# docker run -d -p 11434:11434 --name ollama ollama/ollama:latest
# docker exec ollama ollama pull nomic-embed-text
from haystack import Pipeline

document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")

documents = [
    Document(content="I saw a black horse running"),
    Document(content="Germany has many big cities"),
    Document(content="My name is Wolfgang and I live in Berlin"),
]

document_embedder = OllamaDocumentEmbedder(model=emb_model)
documents_with_embeddings = document_embedder.run(documents)["documents"]
document_store.write_documents(documents_with_embeddings)

query_pipeline = Pipeline()
query_pipeline.add_component("text_embedder", OllamaTextEmbedder(model=emb_model))
query_pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store=document_store))
query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

query = "Who lives in Berlin?"

result = query_pipeline.run({"text_embedder": {"text": query}})

print(result["retriever"]["documents"][0])
