import os
from pathlib import Path

import requests
from haystack import Document
from llama_index import SimpleDirectoryReader
from sentence_transformers import SentenceTransformer, util
import torch

from rich.highlighter import RegexHighlighter
from rich.table import Table
from rich.theme import Theme
from rich.console import Console
from rich.text import Text
from rich.padding import Padding
from rich import print  # https://rich.readthedocs.io/en/stable/markup.html#console-markup

hl_list = [
        r"(?i)(?P<learn>ai|learn[a-z]*|lesson|ml|train[a-z]*|recogni[a-z]*|analy[a-z]*)",
        r"(?i)(?P<machine>(machine|computer|bot|agent|system|recommenda|speech|voice)[a-z]*)",
        r"(?i)(?P<model>embed[a-z]*|large|language|model[a-z]*|ml|llm|generat[a-z]*)",
        r"(?i)(?P<orgs>firm[a-z]*|org[a-z]*|compan[a-z]*|instit[a-z]*)",
        r"(?i)(?P<actions>(chat|search|build|generate|follow|create|use)[a-z]*)",
    ]

class MyHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""
    base_style = "example."
    highlights = hl_list

my_ml = MyHighlighter()

theme = Theme(
    {"example.learn": "bold magenta",
     "example.machine": "bold green",
     "example.model": "bold blue",
     "example.orgs": "bold yellow",
     "example.actions": "bold red",
     })
console = Console(highlighter=my_ml, theme=theme)

console.print("ML models for computer machine learning lessons and training with embeddings")

mycuda = torch.cuda.is_available()
print(f"Cuda available?: {mycuda}")

model = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(model)
print("embedder model loaded: {}".format(model))

git_files = ['https://raw.githubusercontent.com/seanoc5/wooly-tongue/main/data/ces-wp-24-16.pypdf.txt',
             'https://raw.githubusercontent.com/seanoc5/wooly-tongue/main/data/ces-wp-24-16.tika.txt']


# Issue request: r => requests.models.Response
documents = []
for gf in git_files:
    r = requests.get(gf)
    txt = r.text
    doc = Document(content=txt, meta={'file_name':gf})
    documents.append(doc)

# data_dir = Path("../../data")
# filename_fn = lambda filename: {'file_name': os.path.basename(filename)}
# documents = SimpleDirectoryReader(data_dir, filename_as_id=True, file_metadata=filename_fn).load_data(show_progress=True)
print(f"documents loaded: {len(documents)}")

queries = [
    "what segments show decline in adoption of AI or LLM.",
    "automation trends in business"
    "Measuring AI in US economy.",
    "Large language models.",
]


from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 256,
    chunk_overlap  = 20,
)


for doc in documents:
    # print(f"document: {doc}")
    fname = doc.meta['file_name']
    txt = doc.content
    docs = text_splitter.split_text(txt)
    docs_embeddings = embedder.encode(docs, convert_to_tensor=True, show_progress_bar=True)

    print(f"[bold red]================== File: {fname} docs split: {len(docs)} ================== [/bold red]")

# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    top_k = min(5, len(docs))
    for query in queries:
        # print(f"[bold blue]Query: {query} __________ [/bold blue]")
        # todo -- cache query embeddings, reuse in subsequent txt file comparisons
        query_embedding = embedder.encode(query, convert_to_tensor=True)

        table = Table(title=f"QUERY: {query}", show_lines=True, highlight=True)
        table.add_column("node id", style="blue", )     #no_wrap=True
        table.add_column("Score", style="blue", )     #no_wrap=True
        # table.add_column("Tika Score",  style="green")
        table.add_column("Tika Text")


        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, docs_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)

        # tika_cos_scores = util.cos_sim(query_embedding, tika_embeddings)[0]
        # tika_top_results = torch.topk(tika_cos_scores, k=top_k)


        for score, idx in zip(top_results[0], top_results[1]):
            t = docs[idx]
            node_id = idx.item()
            my_score = f"{score.item():.4f}"        # hacked approach to rounding to 4 decimals
            # table.add_row(docs[idx], "(Score: {:.4f})".format(score), 'tika score', 'tika text')
            table.add_row(str(node_id), str(my_score), t)

        """
        # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
        hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
        hits = hits[0]      #Get the hits for the first query
        for hit in hits:
            print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
        """

        console.print(table)
        console.print('\n\n')

print("Done")


