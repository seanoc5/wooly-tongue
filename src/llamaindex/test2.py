# https://docs.llamaindex.ai/en/stable/examples/customization/llms/SimpleIndexDemo-Huggingface_stablelm/
# conflict with `datasets`, so I
# pip uninstall datasets
# pip install llama-index-llms-huggingface

import logging
import sys

from llama_index.core.node_parser import SimpleFileNodeParser

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import Settings

samples_dir = '/opt/data/samples'

filename_fn = lambda filename: {'file_name': filename}
documents = SimpleDirectoryReader(samples_dir, filename_as_id=True, file_metadata=filename_fn).load_data(show_progress=True)
print([x.doc_id for x in documents])

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 700,
    chunk_overlap  = 20,
    length_function = len,
    separators= [
            "\n\n\n\n",
            "\n\n\n",
            "\n\n",
        ".",
            "\n",
            ",",
            # " ",
            # "\u200B",  # Zero-width space
            # "\uff0c",  # Fullwidth comma
            # "\u3001",  # Ideographic comma
            # "\uff0e",  # Fullwidth full stop
            # "\u3002",  # Ideographic full stop
            # "",
        ],
)



for doc in documents:
    txt = doc.text
    texts = text_splitter.split_text(txt)
    print(len(texts)) # 11
    print(texts[0]) # 'What I Worked On\n\nFebruary 2021'

# parser = SimpleFileNodeParser()
# md_nodes = parser.get_nodes_from_documents(documents)
# md_nodes[0]

# setup prompts - specific to StableLM
from llama_index.core import PromptTemplate

system_prompt = """<|SYSTEM|># StableLM Tuned (Alpha version)
- StableLM is a helpful and harmless open-source AI language model developed by StabilityAI.
- StableLM is excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
- StableLM is more than just an information source, StableLM is also able to write poetry, short stories, and make jokes.
- StableLM will refuse to participate in anything that could harm a human.
"""

# This will wrap the default prompts that are internal to llama-index
query_wrapper_prompt = PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>")

import torch

llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=256,
    generate_kwargs={"temperature": 0.7, "do_sample": False},
    system_prompt=system_prompt,
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name="StabilityAI/stablelm-tuned-alpha-3b",
    model_name="StabilityAI/stablelm-tuned-alpha-3b",
    device_map="auto",
    stopping_ids=[50278, 50279, 50277, 1, 0],
    tokenizer_kwargs={"max_length": 4096},
    # uncomment this if using CUDA to reduce memory usage
    # model_kwargs={"torch_dtype": torch.float16}
)

Settings.llm = llm
Settings.chunk_size = 1024

index = VectorStoreIndex.from_documents(documents)

# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
