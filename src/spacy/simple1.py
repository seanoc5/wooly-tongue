# https://spacy.io/usage/processing-pipelines
import spacy
from spacy.tokens import Doc

if not Doc.has_extension("text_id"):
    Doc.set_extension("text_id", default=None)

text_tuples = [
    ("This is the first text.", {"text_id": "text1"}),
    ("This is the second text.", {"text_id": "text2"})
]

nlp = spacy.load("en_core_web_sm")
doc_tuples = nlp.pipe(text_tuples, as_tuples=True)

docs = []
for doc, context in doc_tuples:
    doc._.text_id = context["text_id"]
    docs.append(doc)

for doc in docs:
    print(f"{doc._.text_id}: {doc.text}")
