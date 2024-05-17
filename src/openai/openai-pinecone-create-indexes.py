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

def get_embedding(text_chunks, model="text-embedding-3-small"):
    print(f"Using embedding model: {model}")
    emb = oai_client.embeddings.create(input = text_chunks, model=model)
    return emb.data

my_metric = 'cosine'

for m in models:
    my_emb = get_embedding(lines, model=m)
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

    index_name = f"{m}-{my_metric}"
    dim_size = len(my_emb[0].embedding)
    spec = ServerlessSpec(cloud="aws", region="us-east-1")

    if index_name not in pc_client.list_indexes().names():
        print(f"index({index_name}) does not exist, create index")
        pc_client.create_index(
            index_name,
            dimension=dim_size,  # dimensionality of text-embed-3-small
            metric=my_metric,            # recommended by openai for their embeddings
            spec=spec
        )
        # wait for index to be initialized
        while not pc_client.describe_index(index_name).status['ready']:
            print("Waiting for index to be ready")
            time.sleep(1)
    else:
        print(f"index({index_name}) DOES exist, using existing...")

    # connect to index
    index = pc_client.Index(index_name)
    time.sleep(1)
    index.describe_index_stats()
    up_rsp = index.upsert(vectors=pc_doc_list)
    print(f"Pinecone Upsert response: {up_rsp}")

print("Done!")
