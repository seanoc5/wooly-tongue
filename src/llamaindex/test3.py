#create senetence window node parser with default settings
import logging
import sys
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceWindowNodeParser,SimpleNodeParser

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

samples_dir = '/opt/data/samples'

filename_fn = lambda filename: {'file_name': filename}
documents = SimpleDirectoryReader(samples_dir, filename_as_id=True, file_metadata=filename_fn).load_data(show_progress=True)


sentence_node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=1,
    window_metadata_key="window",
    original_text_metadata_key="original_text")
#base_node_parser = SentenceSplitter(llm=llm)
base_node_parser = SimpleNodeParser()
#
nodes = sentence_node_parser.get_nodes_from_documents(documents)
base_nodes = base_node_parser.get_nodes_from_documents(documents)
#
print(f"SENTENCE NODES :\n {nodes[4]}")
print(f"BASE NODES :\n {base_nodes[4]}")

print("Done!")
