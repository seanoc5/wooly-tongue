# -*- coding: utf-8 -*-
"""LayoutPDFReader_Demo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hx5Y2TxWriAuFXcwcjsu3huKyn39Q2id

**Introduction**

Most PDF to text parsers do not provide layout information. Often times, even the sentences are split with arbritrary CR/LFs making it very difficult to find paragraph boundaries. This poses various challenges in chunking and adding long running contextual information such as section header to the passages while indexing/vectorizing PDFs for LLM applications such as retrieval augmented generation (RAG).

LayoutPDFReader solves this problem by parsing PDFs along with hierarchical layout information such as:

Sections and subsections along with their levels.
Paragraphs - combines lines.
Links between sections and paragraphs.
Tables along with the section the tables are found in.
Lists and nested lists.
With LayoutPDFReader, developers can find optimal chunks of text to vectorize, and a solution for limited context window sizes of LLMs.

# New Section

**Installation**

Install the llmsherpa library.
# !pip install llmsherpa
"""
import os

# Problem with `wt2` venv, older version of llama-index

from llmsherpa.readers import LayoutPDFReader

llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
pdf_url = "https://arxiv.org/pdf/1910.13461.pdf" # also allowed is a file path e.g. /home/downloads/xyz.pdf
# pdf_url = "https://arxiv.org/pdf/2212.14024.pdf"
pdf_reader = LayoutPDFReader(llmsherpa_api_url)
doc = pdf_reader.read_pdf(pdf_url)


import openai
openai.api_key = os.environ["OPENAI_API_KEY"]

"""**Summarize a Section using prompts**

LayoutPDFReader offers powerful ways to pick sections and subsections from a large document and use LLMs to extract insights from a section.

The following code looks for the Fine-tuning section of the document:
"""

from IPython.display import display, HTML
selected_section = None
# find a section in the document by title
for section in doc.sections():
    if section.title == '3 Fine-tuning BART':
        selected_section = section
        break
# use include_children=True and recurse=True to fully expand the section.
# include_children only returns at one sublevel of children whereas recurse goes through all the descendants
HTML(section.to_html(include_children=True, recurse=True))

"""Now, let's create a custom summary of this text using a prompt:"""

# from llama_index.llms import OpenAI
from llama_index.llms.openai import OpenAI
context = selected_section.to_html(include_children=True, recurse=True)
question = "list all the tasks discussed and one line about each task"
resp = OpenAI().complete(f"read this text and answer question: {question}:\n{context}")
print(resp.text)

"""**Analyze a Table using prompts**

With LayoutPDFReader, you can iterate through all the tables in a document and use the power of LLMs to analyze a Table Let's look at the 6th table in this document. If you are using a notebook, you can display the table as follows:
"""

from IPython.display import display, HTML
HTML(doc.tables()[5].to_html())

"""Now let's ask a question to analyze this table:"""

# from llama_index.llms import OpenAI
from llama_index.llms.openai import OpenAI
context = doc.tables()[5].to_html()
resp = OpenAI().complete(f"read this table and answer question: which model has the best performance on squad 2.0:\n{context}")
print(resp.text)

"""That's it! LayoutPDFReader also supports tables with nested headers and header rows.

Here's an example with nested headers (note that the HTML doesn't render properly in ipython but the html structure is correct):
"""

from IPython.display import display, HTML
HTML(doc.tables()[6].to_html())

"""Now let's ask an interesting question:"""

from llama_index.llms.openai import OpenAI
context = doc.tables()[6].to_html()
question = "tell me about R1 of bart for different datasets"
resp = OpenAI().complete(f"read this table and answer question: {question}:\n{context}")
print(resp.text)

"""
**Vector search and Retrieval Augmented Generation with Smart Chunking**

LayoutPDFReader does smart chunking keeping the integrity of related text together:

All list items are together including the paragraph that precedes the list.
Items in a table are chuncked together
Contextual information from section headers and nested section headers is included
The following code creates a LlamaIndex query engine from LayoutPDFReader document chunks"""

from llama_index import Document
from llama_index import VectorStoreIndex

index = VectorStoreIndex([])
for chunk in doc.chunks():
    mydoc = Document(text=chunk.to_context_text(), extra_info={})
    index.insert(mydoc)
query_engine = index.as_query_engine()

"""Let's run one query:"""

response = query_engine.query("list all the tasks that work with bart")
print(response)

"""Let's try another query that needs answer from a table:"""

response = query_engine.query("what is the bart performance score on squad")
print(response)

"""**Get the Raw JSON**

To get the complete json returned by llmsherpa service and process it differently, simply get the json attribute
"""

doc.json

