# https://spacy.io/usage/linguistic-features#vectors-similarity
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_md")  # make sure to use larger package!

# source_text = open('../../data/test-paragraphs.txt').read()
source_text = '''
By combining the power of transformer-based language models, pipeline-oriented structure, and developer-friendly tooling, 
Haystack is the NLP framework of choice for a range of organizations. Companies like 
Bank of America, Airbus, BMW, and Sooth.ai all rely on Haystack to set up their semantic search systems.
'''
doc = nlp(source_text)
sentences = list(doc.sents)

sentA = sentences[0]
sentB = sentences[1]

# Similarity of two documents
print(f"A) {sentA} \nB) {sentB} \nSimilarity:{sentA.similarity(sentB)}")

for chunk in doc.noun_chunks:
    print(chunk.text)

# Initialize the matcher
matcher = Matcher(nlp.vocab)



print("Done")
