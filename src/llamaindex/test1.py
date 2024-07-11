# from llama_index import SimpleDirectoryReader
from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

documents = SimpleDirectoryReader("/opt/data/text").load_data()
print(f"Doc count: {len(documents)}")

nodes = node_parser.get_nodes_from_documents(
    [Document(text="long text")], show_progress=False
)
print(f"Node count: {len(nodes)}")
