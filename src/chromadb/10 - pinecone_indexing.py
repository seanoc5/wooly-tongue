# from urllib import request
import requests
import torch
from haystack import Pipeline, Document
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.writers import DocumentWriter
# Create pipeline components
from haystack_integrations.components.retrievers.chroma import ChromaQueryTextRetriever
from haystack_integrations.document_stores.chroma import ChromaDocumentStore

from rich import print  # https://rich.readthedocs.io/en/stable/markup.html#console-markup
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.style import Style
from rich.table import Table
from rich.theme import Theme

hl_list = [
    r"(?i)(?P<bankother>phone|bank shot|bank of the|banked)",
    r"(?i)(?P<bank>bank|boa|teller|deposit|vault|account)",

    r"(?i)(?P<boardother>back board|board of direct|board the)",
    r"(?i)(?P<board>board|plank|timber|2x4|wood supplies)",

    r"(?i)(?P<flying>fly over|pilot|navigation|boeing|747|landing)",
    r"(?i)(?P<cool>fly sister|cool)",
    r"(?i)(?P<fly>fly)",
]

class MyHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""
    base_style = "example."
    highlights = hl_list

my_hl = MyHighlighter()

theme = Theme(
    {"example.bankother": Style(color='green', bgcolor="grey93"),
     "example.bank": Style(color='dark_green', bold=True),

     "example.boardother": Style(color='blue', bgcolor="grey93"),
     "example.board": "bold dark_blue",

     "example.cool": Style(color='magenta', bgcolor="grey93"),
     "example.flyother": Style(color='red', bgcolor="grey93"),
     "example.flying": Style(color='dark_red', bold=True),
     })

console = Console(highlighter=my_hl, theme=theme)

print(f"Torchy?? [red]{torch.cuda.is_available()}[/red]")
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"

document_store = ChromaDocumentStore()
# document_store = Pine()

def process_text(content, embedding_mode, document_store):
    print(f"Read content (len:{len(content)}) from path: {fpath}")

    # cleaner = DocumentCleaner(remove_repeated_substrings=True)
    big_doc = Document('doc1', content=content)
    print(f"Doc store STARTS with: {document_store.count_documents()} documents")
    splitter = DocumentSplitter(split_by="sentence", split_length=1, split_overlap=0)
    chunked_docs = splitter.run(documents=[big_doc])
    # todo - some better way to do this??
    cnt = 0
    for chunk in chunked_docs["documents"]:
        cnt += 1
        chunk.id = f"{big_doc.id}--{cnt}"

    document_embedder = SentenceTransformersDocumentEmbedder(model=embedding_model)
    document_writer = DocumentWriter(document_store)
    indexing = Pipeline()
    # indexing.add_component(instance=cleaner, name="document_cleaner")
    # indexing.add_component(instance=splitter, name="document_splitter")
    indexing.add_component(instance=document_embedder, name="document_embedder")
    indexing.add_component(instance=document_writer, name="document_writer")
    # indexing.connect("converter", "document_cleaner")
    # indexing.connect("document_cleaner", "document_embedder")
    # indexing.connect("document_splitter", "document_embedder")
    indexing.connect("document_embedder", "document_writer")
    print(f"[green]Indexing {len(chunked_docs['documents'])} documents")
    # print(f"[green]Indexing {big_doc}")
    indexing.run({"document_embedder": {"documents": chunked_docs["documents"]}})
    # indexing.run({"document_cleaner": {"documents": chunked_docs["documents"]}})
    print(f"[green]Doc store AFTER indexing: {document_store.count_documents()} documents")
    return document_store

def do_query(q, embedding_model, k_results, document_store):
    retriever = ChromaQueryTextRetriever(document_store=document_store, top_k=k_results)
    foo = retriever.run(q)

    text_embedder = SentenceTransformersTextEmbedder(model=embedding_model)
    text_embedder.warm_up()
    bar = text_embedder.run(q)

    query_pipeline = Pipeline()
    # query_pipeline.add_component("text_embedder", text_embedder)
    query_pipeline.add_component("retriever", retriever)
    # query_embedding = text_embedder.run(text=query)
    # result = query_pipeline.run({"text_embedder": {"text": query}})
    # result = query_pipeline.run({"retriever":query_embedding})
    results = query_pipeline.run({"retriever": {"query": q, "top_k": k_results}})
    return results


def display_results(table_title, results, show_lines=True):
    table = Table(title=table_title, show_lines=show_lines, highlight=True)
    table.add_column("id", style="blue", )  # no_wrap=True
    table.add_column("text")  # no_wrap=True
    table.add_column("Score", style="blue", )
    for d in results["retriever"]["documents"]:
        # print(f"Result: ", d.meta, d.score)
        table.add_row(d.id, d.content.strip(), "{:.2f}".format(d.score))
    console.print(table)
    print('\n\n')

queries = [
    'who is in the bank to deposit money?',
    'who is on a bank?',

    'where can I get a board for fixing my wall?',
    'who is on the board?',

    'who is flying in a plane?',
    'who is looking super fly?',
    'who is looking cool?',
    ]
k = 5

fpath = 'https://raw.githubusercontent.com/seanoc5/wooly-tongue/main/data/test-paragraphs.txt'
rsp = requests.get(fpath)
if(rsp.status_code == 200):
    content = rsp.text
    print(f"Got content (len:{len(content)} from path: {fpath}, now process it (embed and save to doc store)")
    process_text(content, embedding_model, document_store)
    print("Prepare to run queries...")
    for q in queries:
       results = do_query(q, embedding_model, k, document_store)
       title = f"Embedding model: [bold blue]{embedding_model}[/] \nQuery: [bold blue]{q}[/]"
       display_results(title, results, show_lines=True)

else:
    print(f"PROBLEM!!! Could not find fpath: {fpath}")




print("Done!")
