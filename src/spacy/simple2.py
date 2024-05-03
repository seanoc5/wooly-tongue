# https://spacy.io/usage/linguistic-features#vectors-similarity
import spacy

nlp = spacy.load("en_core_web_md")  # make sure to use larger package!

source_text = open('../../data/test-paragraphs.txt').read()
doc = nlp(source_text)
sentences = list(doc.sents)

sentA = sentences[2]
sentB = sentences[3]

# Similarity of two documents
print(f"A) {sentA} \nB) {sentB} \nSimilarity:{sentA.similarity(sentB)}")

# Similarity of tokens and spans
# french_fries = doc1[2:4]
# burgers = doc1[5]
# print(french_fries, "<->", burgers, french_fries.similarity(burgers))

print("Done")
