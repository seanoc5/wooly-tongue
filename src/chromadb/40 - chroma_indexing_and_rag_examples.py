import torch
torch.cuda.is_available()


from haystack import Pipeline
from haystack.components.converters import TextFileToDocument
from haystack.components.writers import DocumentWriter
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder

from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack import Document

from pathlib import Path
data_dir = "/opt/data/text"
text_files = list(Path(data_dir).glob("**/*.txt"))
print(text_files)

document_store = ChromaDocumentStore()
print(f"Doc store STARTS with: {document_store.count_documents()} documents")

# remove repeated substrings to get rid of headers/footers
cleaner = DocumentCleaner(remove_repeated_substrings=True)
# Since jina-v2 can handle 8192 tokens, 500 words seems like a safe chunk size
splitter = DocumentSplitter(split_by="word", split_length=100, split_overlap=20)
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
document_embedder = SentenceTransformersDocumentEmbedder(model=embedding_model)
document_writer = DocumentWriter(document_store)

indexing = Pipeline()
indexing.add_component("converter", TextFileToDocument())
indexing.add_component(instance=cleaner, name="document_cleaner")
indexing.add_component(instance=splitter, name="document_splitter")
indexing.add_component(instance=document_embedder, name="document_embedder")
indexing.add_component(instance=document_writer, name="document_writer")

indexing.connect("converter", "document_cleaner")
indexing.connect("document_cleaner", "document_splitter")
indexing.connect("document_splitter", "document_embedder")
indexing.connect("document_embedder", "document_writer")

indexing.run({"converter": {"sources": text_files}})

print(f"Doc store AFTER indexing: {document_store.count_documents()} documents")


# Create pipeline components
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack.components.embedders import SentenceTransformersTextEmbedder

retriever = ChromaQueryTextRetriever(document_store=document_store, top_k=3)
text_embedder = SentenceTransformersTextEmbedder(model=embedding_model)
text_embedder.warm_up()

query_pipeline = Pipeline()
# query_pipeline.add_component("text_embedder", text_embedder)
query_pipeline.add_component("retriever", retriever)

foo = retriever.run(query="test me")
query = "How many languages are there?"
query_embedding = text_embedder.run(text="What is BTOS?")

# result = query_pipeline.run({"text_embedder": {"text": query}})
# result = query_pipeline.run({"retriever":query_embedding})
qry = "What is BTOS"
k = 5
results = query_pipeline.run({"retriever": {"query": qry, "top_k": k}})

# ---------------------------------------- print out results
from rich.highlighter import RegexHighlighter
from rich.pretty import Pretty
from rich.table import Table
from rich.theme import Theme
from rich.console import Console
from rich.text import Text
from rich.padding import Padding
from rich import print  # https://rich.readthedocs.io/en/stable/markup.html#console-markup


table = Table(title=f'Demo results, query=[{query}]', show_lines=True)
table.add_column("sent #", style="blue", )     #no_wrap=True
table.add_column("text")     #no_wrap=True
table.add_column("Entities", style="blue", )


for d in results["retriever"]["documents"]:
    print("Result: ", d.meta, d.score)
print("Done!")
