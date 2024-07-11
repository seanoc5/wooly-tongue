import chromadb
import requests
from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore

source_text = open('../../data/test-paragraphs.txt').read()

from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner

para_splitter = DocumentSplitter(split_by="passage", split_length=1, split_overlap=0)
sent_splitter = DocumentSplitter(split_by="sentence", split_length=1, split_overlap=0)


big_doc = Document(content=source_text, id='big_doc-1')
paragraphs = para_splitter.run([big_doc])
print(f"Para count: {len(paragraphs['documents'])}")

sentences = sent_splitter.run(paragraphs['documents'])
print(f"\t\tsentence count: {len(sentences['documents'])}")

questions = [
    'who is at the bank?',
    'Who is on the phone?',
    'Where is Jeff?',
    'what are the benefits of ML?'
    'what kind of work can StackTheory help with?'
             ]

# Create a ChromaDB client
client = chromadb.Client()
# Create a collection named "paragraphs"
para_coll = client.create_collection(name="paragraphs")
para_peek = para_coll.peek() # returns a list of the first 10 items in the collection
para_cnt = para_coll.count()

# Create a collection named "sentences"
sent_coll = client.create_collection(name="sentences")
sent_peek = para_coll.peek() # returns a list of the first 10 items in the collection
sent_cnt = para_coll.count()

document_cleaner = DocumentCleaner()
document_splitter = DocumentSplitter(split_by="word", split_length=150, split_overlap=50)


document_store = InMemoryDocumentStore()
document_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
document_writer = DocumentWriter(document_store)

preprocessing_pipeline = Pipeline()
# preprocessing_pipeline.add_component(instance=file_type_router, name="file_type_router")
# preprocessing_pipeline.add_component(instance=text_file_converter, name="text_file_converter")
# preprocessing_pipeline.add_component(instance=markdown_converter, name="markdown_converter")
# preprocessing_pipeline.add_component(instance=pdf_converter, name="pypdf_converter")
# preprocessing_pipeline.add_component(instance=document_joiner, name="document_joiner")
preprocessing_pipeline.add_component(instance=document_cleaner, name="document_cleaner")
preprocessing_pipeline.add_component(instance=document_splitter, name="document_splitter")
preprocessing_pipeline.add_component(instance=document_embedder, name="document_embedder")
preprocessing_pipeline.add_component(instance=document_writer, name="document_writer")

# preprocessing_pipeline.connect("file_type_router.text/plain", "text_file_converter.sources")
# preprocessing_pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
# preprocessing_pipeline.connect("file_type_router.text/markdown", "markdown_converter.sources")
# preprocessing_pipeline.connect("text_file_converter", "document_joiner")
# preprocessing_pipeline.connect("pypdf_converter", "document_joiner")
# preprocessing_pipeline.connect("markdown_converter", "document_joiner")
# preprocessing_pipeline.connect("document_joiner", "document_cleaner")
preprocessing_pipeline.connect("document_cleaner", "document_splitter")
preprocessing_pipeline.connect("document_splitter", "document_embedder")
preprocessing_pipeline.connect("document_embedder", "document_writer")
preprocessing_pipeline.run()

i = 0
for para in paragraphs['documents']:
    i += 1
    print(f"\t\t{i}): {para}")

    sentences = sent_splitter.run(para)
    for sentence in sentences:
        print(f"\t\tSentence : {sentence}")


# for idx, s in enumerate(sentences['documents'][:3]):
#     print(f"{idx}) {s.content}")

print(f"Done?")
