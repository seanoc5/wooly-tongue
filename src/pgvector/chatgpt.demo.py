import sys

from pgvector.psycopg import register_vector
import psycopg
from sentence_transformers import SentenceTransformer
# Sample code suggested by chatgpt sept 16, 2024-ish

import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.info("Starting here...")

# conn = psycopg.connect(dbname='pgvector_example', autocommit=True)
conn = psycopg.connect(dbname='vectors', autocommit=True)

# conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
register_vector(conn)

conn.execute('DROP TABLE IF EXISTS documents')
conn.execute('CREATE TABLE documents (id bigserial PRIMARY KEY, content text, embedding vector(768))')

input = [
    'what is moving?',

    'The dog is barking',
    'The dog is walking',
    'The puppy is barking',
    'Fido is making noise',

    'The cat is purring',
    'Fluffy is making noise',
    'The cat is meowing',
    'The cat is walking',

    'The bear is growling',
    'The bear is snoring',
    'The bear is walking',
    'The bear is eating',
]

# model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('sentence-transformers/msmarco-bert-base-dot-v5')

embeddings = model.encode(input)

for content, embedding in zip(input, embeddings):
    conn.execute('INSERT INTO documents (content, embedding) VALUES (%s, %s)', (content, embedding))

document_id = 1
neighbors = conn.execute(
    'SELECT content FROM documents WHERE id != %(id)s ORDER BY embedding <=> (SELECT embedding FROM documents WHERE id = %(id)s) LIMIT 3',
    {'id': document_id}).fetchall()

for neighbor in neighbors:
    print(neighbor[0])

logging.info("Done?!...")


