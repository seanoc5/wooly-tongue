import os

from haystack.components.converters import pypdf
from rich.table import Table
from sentence_transformers import SentenceTransformer, util
import torch


mycuda = torch.cuda.is_available()
print(mycuda)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# As dataset, we use census.gov publication AI in the US workplace (something new and interesting for demo)
import requests
pdf_name = "CES-WP-24-16.pdf"
if os.path.exists(pdf_name):
    print(f"Found pdf ({pdf_name}) available locally, no need to (re)download it")
else:
    print(f"Coud NOT find pdf ({pdf_name}) available locally, attempting to download it...")
    url = f'https://www.census.gov/hfp/btos/downloads/{pdf_name}'
    response = requests.get(url)
    with open(pdf_name, 'wb') as f:
        f.write(response.content)
    print(f"Wrote file(?): {pdf_name}")

# Open the PDF file
text = ""
with open(pdf_name, 'rb') as file:
    reader = pypdf.PdfReader(file)
    # page_count = reader.page_count
    page_count = 0
    for page in reader.pages:
        page_count = page_count + 1
        text += page.extract_text() + "\n"

print(f"Extracted text from ({page_count}) pages, text size:({len(text)}")

# from langchain.text_splitter import SpacyTextSplitter
# text_splitter = SpacyTextSplitter()
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 256,
    chunk_overlap  = 20
)

docs = text_splitter.split_text(text)

docs_embeddings = embedder.encode(docs, convert_to_tensor=True, show_progress_bar=True)

with open('/opt/docs/CensusonAIinBusinessCES-WP-24-16.pdf.txt', 'r') as file:
    # Read the contents of the file
    tika_text = file.read()
tika_docs = text_splitter.split_text(tika_text)
tika_embeddings = embedder.encode(tika_docs, convert_to_tensor=True, show_progress_bar=True)

print(f"Tika text: {len(tika_text)} tika docs: {len(tika_docs)} ----- pytext:{len(text)} -- docs:{len(docs)}")

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


    # print("\n============================================")
    # qtext = Text(f"[bold green]{query}[/bold green]")
    # qtext.stylize("bold magenta",)         # https://youtrack.jetbrains.com/issue/PY-43860/Python-package-rich-print-text-in-color-bold-etc.-does-not-print-color-bold-etc.-in-the-Run-and-Debug-panes.-Works-in-Python
    # print(f"[bold green]Query:{query}[/bold green]")
    # print(f"[bold green]Top 5 most similar sentences in corpus:[/bold green]")


    for score, idx in zip(top_results[0], top_results[1]):
        t = docs[idx]
        table.add_row(docs[idx], "(Score: {:.4f})".format(score), 'tika score', 'tika text')

        # print(docs[idx], "(Score: {:.4f})".format(score))
        # print("{}) [bold green] ------ Score: {:.4f} ------ [/bold green]".format(idx, score))
        # console.print(Padding(docs[idx], pad=(0, 0, 0, 4)))
        # print()

    """
    # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
    hits = hits[0]      #Get the hits for the first query
    for hit in hits:
        print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
    """

console.print(table)

print("Done")


