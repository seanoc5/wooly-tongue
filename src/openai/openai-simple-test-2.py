import os
import time
from getpass import getpass
# https://cookbook.openai.com/examples/vector_databases/pinecone/semantic_search

lines = [
'''    
Joe tried to play tennis, so he went to a court and took his racket from its case but then realized he forgot to bring a ball.
When he came back to the court with some balls, he found someone had taken his racket but left the case, so he would have to try another day.

Bill’s case was tried in Federal court because his website was considered an interstate racket.
The judge heard the case but ruled it should be tried in the State where the racket began.

Jim tried to court Jane by singing over the phone but in this case, it came across as just racket.
He then tried signing at her window, and she thought he was still off tune but cute, so she let courting begin.
  
Ed noted one court may try Trump under a State law about criminal rackets.
He added the guy is trying to delay all legal matters until the court of public opinion decides whether it cares about any of his many rackets, in November.
'''
]
print(f"Line count: {len(lines)}")

queries = [
    "what bugs are around?",
    'Who would swat at a fly?',

    'Who is camping?',
    'what is happening in tents?',

    'Who is dealing with pants?',
    'Who is concerned about closing pants?',
    'Who is dealing with zippers?',

    'Who is playing baseball?',
    'Who is seeing a baseball in the air?',

    'who is fishing?',
    'what lures are around?',
]

from openai import OpenAI

models = 'text-embedding-3-small'
if os.environ.get('OAI_KEY'):
    oai_key = os.environ['OAI_KEY']
else:
    oai_key = getpass("Enter an OPENAI key: ")
client = OpenAI(api_key=oai_key)

def get_embedding(text_chunks, model="text-embedding-3-small"):
  emb = client.embeddings.create(input = text_chunks, model=model)
  return emb.data

my_emb = get_embedding(lines)

# print(f"OpenAI result: {my_openai_result}")
print(f"OpenAI embedding result: {len(my_emb)}, that should equal {len(lines)}")

pc_doc_list = []
for idx, line in enumerate(lines):
    # print(f"{idx}: {line}")
    pc_doc = {
        'id': str(idx),
        'values': my_emb[idx].embedding,
        'metadata': {'sequence':idx, 'text':line}
    }
    pc_doc_list.append(pc_doc)

from pinecone import Pinecone, ServerlessSpec
from getpass import getpass

if os.environ.get('PINECONE_API_KEY'):
    pc_key = os.environ['PINECONE_API_KEY']   # os.environ["PINECONE"] = getpass("Enter OpenAI API key:")
else:
    pc_key = getpass("Enter PINECONE API key:")

pc = Pinecone(api_key=pc_key)
index_name = 'openai-simple'
dim_size = len(my_emb[0].embedding)
spec = ServerlessSpec(cloud="aws", region="us-east-1")

if index_name not in pc.list_indexes().names():
    print(f"index({index_name}) does not exist, create index")
    pc.create_index(
        index_name,
        dimension=len(dim_size),  # dimensionality of text-embed-3-small
        metric='dotproduct',
        spec=spec
    )
    # wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        print("Waiting for index to be ready")
        time.sleep(1)
else:
    print(f"index({index_name}) DOES exist, using existing...")

# connect to index
index = pc.Index(index_name)
time.sleep(1)
index.describe_index_stats()
up_rsp = index.upsert(vectors=pc_doc_list)
print(f"Pinecone Upsert response: {up_rsp}")

k = 3
for q in queries:
    print(f"\n\nQuery: {q}")
    xq = client.embeddings.create(input=q, model=model).data[0].embedding
    res = index.query(vector=[xq], top_k=k, include_metadata=True)
    for match in res['matches']:
        print(f"\t\t{match['score']:.2f}: {match['metadata']['text']}")

print("Done!")
