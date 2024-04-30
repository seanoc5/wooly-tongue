# https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/usage_metadata_extractor/
# BROKEN -- requires OpenAI at the moment..
# ImportError: `llama-index-llms-openai` package not found, please run `pip install llama-index-llms-openai`
from llama_index.core import SimpleDirectoryReader, node_parser
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
)
from llama_index.core.node_parser import TokenTextSplitter

from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

llm_name = 'llama3'
print(f"using model: {llm_name}")

Settings.llm = Ollama(model=llm_name, request_timeout=60.0)
# print(Settings.llm)

text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=150, chunk_overlap=30
)

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

node_parser = SentenceSplitter(chunk_size=200, chunk_overlap=20)

nodes = node_parser.get_nodes_from_documents(
    [Document(text="long text")], show_progress=False
)

title_extractor = TitleExtractor(nodes=5)
qa_extractor = QuestionsAnsweredExtractor(questions=3)

# assume documents are defined -> extract nodes
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    transformations=[text_splitter, title_extractor, qa_extractor]
)

# documents = SimpleDirectoryReader("/opt/data/text").load_data()
documents = SimpleDirectoryReader("/opt/data/samples", filename_as_id=True).load_data()

# https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/
nodes = pipeline.run(
    documents=documents,
    in_place=True,
    show_progress=True,
)

print(documents[0].get_content())
orig_nodes = node_parser.get_nodes_from_documents(documents)

print(f"Original nodes len: {len(orig_nodes)}")

