import time

import requests
from haystack import Document

from rich.highlighter import RegexHighlighter
from rich.pretty import Pretty, pprint as print
from rich.table import Table
from rich.theme import Theme
from rich.console import Console
from rich.text import Text
from rich.padding import Padding
from rich import print  # https://rich.readthedocs.io/en/stable/markup.html#console-markup
import spacy

# note: in intellij idea update run/debug config with emulate console option to get colors and better formatting
console = Console()

src = '../../data/ces-wp-24-16.tika.txt'
print(f'[red]using source: {src}[/red]\n')
source_text = open(src).read()


spacy.require_gpu()

model_name = 'en_core_web_trf'
nlp_trf = spacy.load(model_name)

doc = nlp_trf(source_text)

table = Table(title=f'Spacy {model_name} (first 10 sentences)', show_lines=True, min_width=100)
table.add_column("sent #", style="blue", )     #no_wrap=True
table.add_column("text")     #no_wrap=True
table.add_column("Entities", style="blue", )

idx = 0
for sent in doc.sents:
    idx += 1
    if idx < 20 or idx % 10 == 0:
        s = ''.join(sent.text.splitlines())
        ents = Pretty(sent.ents) if sent.ents else ''
        table.add_row(str(idx), s, ents)
2

console.print(table)

# for chunk in doc.noun_chunks:
    # print(chunk.text)

print(f"Done?")
