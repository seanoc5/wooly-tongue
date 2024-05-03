import time

import requests
from haystack import Document

from rich.highlighter import RegexHighlighter
from rich.pretty import Pretty
from rich.table import Table
from rich.theme import Theme
from rich.console import Console
from rich.text import Text
from rich.padding import Padding
from rich import print  # https://rich.readthedocs.io/en/stable/markup.html#console-markup

console = Console()

source_text = open('../../data/test-paragraphs.txt').read()

import spacy
spacy.require_gpu()

nlp_sm = spacy.load('en_core_web_sm')
nlp_md = spacy.load('en_core_web_md')
nlp_lg = spacy.load('en_core_web_lg')
nlp_trf = spacy.load('en_core_web_trf')

en_cores = {'small':nlp_sm, 'medium':nlp_md, 'large':nlp_lg, 'trf':nlp_trf}
for name, nlp in en_cores.items():
    tic = time.perf_counter()
    doc = nlp(source_text)
    toc = time.perf_counter()
    print(f'{name}  Time: {toc - tic:0.4f} seconds')

    table = Table(title=f'Spacy {name}', show_lines=True)
    table.add_column("sent #", style="blue", )     #no_wrap=True
    table.add_column("text", highlight=True)     #no_wrap=True
    table.add_column("Entities", style="blue", )


    for idx, sent in enumerate(doc.sents):
        s = ''.join(sent.text.splitlines())
        ents = Pretty(sent.ents) if sent.ents else ''
        table.add_row(str(idx), s, ents)


    console.print(table)

# for chunk in doc.noun_chunks:
    # print(chunk.text)

print(f"Done?")
