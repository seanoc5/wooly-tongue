import requests
from haystack import Document


git_files = ['https://raw.githubusercontent.com/seanoc5/wooly-tongue/main/data/ces-wp-24-16.pypdf.txt',
             'https://raw.githubusercontent.com/seanoc5/wooly-tongue/main/data/ces-wp-24-16.tika.txt']


# Issue request: r => requests.models.Response
documents = []
for gf in git_files:
    r = requests.get(gf)
    txt = r.text
    doc = Document(content=txt, meta={'file_name':gf})
    documents.append(doc)

# data_dir = Path("../../data")
# filename_fn = lambda filename: {'file_name': os.path.basename(filename)}
# documents = SimpleDirectoryReader(data_dir, filename_as_id=True, file_metadata=filename_fn).load_data(show_progress=True)
print(f"documents loaded: {len(documents)}")
