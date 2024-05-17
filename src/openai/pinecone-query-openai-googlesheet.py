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


# ------------------------ WRITE to google spreadsheet ------------------------
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

# Define the scope of Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Credentials JSON file downloaded from Google Cloud Console
creds = '/opt/docs/stackedcone-bbec38745789.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, scope)

# Authenticate using the credentials
client = gspread.authorize(credentials)

# Create a new Google Sheets workbook
workbook = client.create('StackedCone2')
sheet_zero = workbook.get_worksheet(0)
# Share the spreadsheet with a particular user (replace 'user@example.com' with the email address)
workbook.share('seanoc5@gmail.com', perm_type='user', role='writer')

# Open the first worksheet in the new workbook
worksheet = workbook.get_worksheet(0)
# Change the name of the first worksheet
worksheet.update_title('Text and Questions')
# Update a specific cell range with the list
# Assuming you want to start from the first cell
cell_range = f"A1:A{len(lines)}"
worksheet.update(range_name=cell_range, values=[[item] for item in lines])
cell_range = f"C1:C{len(queries)}"
worksheet.update(range_name=cell_range, values=[[item] for item in queries])

# Add two sheets named 'one' and 'two'
sheet_openai = workbook.add_worksheet(title='OpenAI embeddings', rows="100", cols="200")
# for qidx, q in enumerate(queries):
#     row_num = (qidx * (k + 1))
#     sheet_openai.update_cell(row_num+1, 1 ,q)

# Share the workbook with anyone with the link
workbook.share("", perm_type='anyone', role='reader')

print("Workbook created successfully!")
print(f"Url: {workbook.url}!")


for midx, m in enumerate(models):
    time.sleep(2)

    index_name = f"{m}-{my_metric}"
    spec = ServerlessSpec(cloud="aws", region="us-east-1")

    if index_name not in pc_client.list_indexes().names():
        print(f"{midx} index({index_name}) does not exist, create index")
        raise SystemError
    else:
        print(f"{midx} index({index_name}) DOES exist, using existing...")

    # connect to index
    index = pc_client.Index(index_name)
    time.sleep(2)
    col_num = midx * 4 +1      # score, line, spacer, spacer
    index.describe_index_stats()
    sheet_openai.update_cell(1, col_num , m)
    for qidx, q in enumerate(queries):
        time.sleep(2)
        print(f"\n\n{qidx}) Query: {q}")
        row_num = qidx * (k + 1) + 2
        xq = oai_client.embeddings.create(input=q, model=m).data[0].embedding
        res = index.query(vector=[xq], top_k=k, include_metadata=True)
        sheet_openai.update_cell(row_num, col_num ,q)
        for ridx, match in enumerate(res['matches']):
            time.sleep(3)
            score = f"{match['score']:.2f}"
            line = match['metadata']['text']
            # print(f"\t\t{score}: {line}")
            sheet_openai.update_cell(row_num+ridx, col_num+1 ,score)
            sheet_openai.update_cell(row_num+ridx, col_num+2,line)


print("Done!")
