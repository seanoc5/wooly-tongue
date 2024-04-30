import os
from pathlib import Path

from llama_index.core import SimpleDirectoryReader
from rich.table import Table
from sentence_transformers import SentenceTransformer, util
import torch


mycuda = torch.cuda.is_available()
print(f"Cuda available?: {mycuda}")

model = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(model)
print("embedder model loaded: {}".format(model))

data_dir = Path("../data")
filename_fn = lambda filename: {'file_name': filename}
documents = SimpleDirectoryReader(data_dir, filename_as_id=True, file_metadata=filename_fn).load_data(show_progress=True)
print(f"documents loaded: {len(documents)}")


from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 256,
    chunk_overlap  = 20,
)

for doc in documents:
    # print(f"document: {doc}")
    fname = doc.metadata['file_name']
    txt = doc.text
    docs = text_splitter.split_text(txt)
    docs_embeddings = embedder.encode(docs, convert_to_tensor=True, show_progress_bar=True)


# print(f"Tika text: {len(tika_text)} tika docs: {len(tika_docs)} ----- pytext:{len(text)} -- docs:{len(docs)}")

# Query sentences:
queries = [
    "automation trends in business"
    "Measuring AI in US economy.",
    "Employment related to AI.",
    "Large language models.",
]



from rich.console import Console
from rich.text import Text
from rich.padding import Padding
from rich import print  # https://rich.readthedocs.io/en/stable/markup.html#console-markup

console = Console()
# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
top_k = min(3, len(docs))
for query in queries:
    query_embedding = embedder.encode(query, convert_to_tensor=True)

    table = Table(title=query, show_lines=True)
    table.add_column("Python Text", style="blue", )     #no_wrap=True
    table.add_column("Python Score", style="blue", )     #no_wrap=True
    table.add_column("Tika Score",  style="green")
    table.add_column("Tika Text", style="green")


    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, docs_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    tika_cos_scores = util.cos_sim(query_embedding, tika_embeddings)[0]
    tika_top_results = torch.topk(tika_cos_scores, k=top_k)


    for score, idx in zip(top_results[0], top_results[1]):
        t = docs[idx]
        table.add_row(docs[idx], "(Score: {:.4f})".format(score), 'tika score', 'tika text')

    """
    # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
    hits = hits[0]      #Get the hits for the first query
    for hit in hits:
        print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
    """

console.print(table)

print("Done")


