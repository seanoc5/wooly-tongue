# https://github.com/langchain-ai/langchain/issues/6952
import spacy
# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
# from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import psycopg2
from spacy import displacy

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="dell",
    dbname="cm_dev",
    user="sean",
    password="pass1234"
)

# Create a cursor object
cursor = conn.cursor()

# Execute a query to retrieve 10 records from the database
cursor.execute("SELECT * FROM content LIMIT 10")

# Fetch the results of the query
records = cursor.fetchall()

spacy.require_gpu()

model_name = 'en_core_web_trf'
nlp_trf = spacy.load(model_name)

doc = nlp_trf(source_text)

# Initialize the SpaCy model
nlp = displacy(lang="en", options={"ents": "yes"})

# Process each record and extract the content_html field
for record in records:
    # Extract the content_html field from the record
    content_html = record["content_html"]

    # Parse the HTML content using SpaCy
    parsed_html = nlp(content_html)

    # Extract all the text from the parsed HTML content
    text = " ".join([t.text for t in parsed_html if t.pos_ == "VERB"])

    # Print the extracted text
    print(text)

print("done")
