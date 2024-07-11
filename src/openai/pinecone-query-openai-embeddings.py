import os
import time
from getpass import getpass
# https://cookbook.openai.com/examples/vector_databases/pinecone/semantic_search

lines = [
'1) The fly was buzzing around Adam\'s sandwich.',
'1a) The buzzing of the insect was annoying Adam.',

'2) Bob unzipped the tent fly to get fresh air.',
'2a) The flaps of the tent were open and Bob enjoyed the breeze.',

'3) Cathy told her son to close his fly.',
'3a) As Cathy finished putting on her jeans, the cowgirl remembered to zip up.',

'4) The catcher, Dave, pointed to the fly and yelled to the short-stop to catch it.',
'4a) Dave later popped up and ended the inning.',
'4b) Dave hit a grounder past the first baseman.',

'5) Ed fisherman pulled out his favorite fly and cast it toward the river bank.',
'5a) Ed got his favorite fly and tied it to his line with a bit of bait.'
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

if os.environ.get('OAI_KEY'):
    oai_key = os.environ['OAI_KEY']
else:
    oai_key = getpass("Enter an OPENAI key: ")
oai_client = OpenAI(api_key=oai_key)

from pinecone import Pinecone, ServerlessSpec
from getpass import getpass

if os.environ.get('PINECONE_API_KEY'):
    pc_key = os.environ['PINECONE_API_KEY']   # os.environ["PINECONE"] = getpass("Enter OpenAI API key:")
else:
    pc_key = getpass("Enter PINECONE API key:")

pc_client = Pinecone(api_key=pc_key)


models = ['text-embedding-3-small',
          'text-embedding-3-large',
          'text-embedding-ada-002']
my_metric = 'cosine'
k = 5

def get_embedding(text_chunks, model="text-embedding-3-small"):
  emb = oai_client.embeddings.create(input = text_chunks, model=model)
  return emb.data

for m in models:
    index_name = f"{m}-{my_metric}"
    spec = ServerlessSpec(cloud="aws", region="us-east-1")

    if index_name not in pc_client.list_indexes().names():
        print(f"index({index_name}) does not exist, create index")
        raise SystemError
    else:
        print(f"index({index_name}) DOES exist, using existing...")

    # connect to index
    index = pc_client.Index(index_name)
    time.sleep(1)
    index.describe_index_stats()

    with open(f"{m}.txt", 'w') as f:
        for idx, q in enumerate(queries):
            print(f"\n\n{idx}) Query: {q}")
            f.write(f"Query ({idx}): {q}\n")
            xq = oai_client.embeddings.create(input=q, model=m).data[0].embedding
            res = index.query(vector=[xq], top_k=k, include_metadata=True)
            for match in res['matches']:
                print(f"\t\t{match['score']:.2f}: {match['metadata']['text']}")
                f.write(f"{match['score']:.2f}: {match['metadata']['text']}\n")
            f.write("\n")
print("Done!")
