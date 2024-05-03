# https://github.com/langchain-ai/langchain/issues/6952
import spacy
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class SpacyEmbeddings:
    """ Class for generating Spacy-based embeddings for documents and queries. """

    def __init__(self):
        """ Initialize the SpacyEmbeddings object by loading the Spacy model. """
        self.nlp = spacy.load('en_core_web_sm')

    def embed_documents(self, texts):
        """ Embed a list of documents using Spacy.
        Args: texts (list): A list of documents.
        Returns: list: A list of document embeddings. """
        return [self.nlp(text).vector.tolist() for text in texts]

    def embed_query(self, text):
        """
        Embed a query using Spacy.
        Args: text (str): The query text.
        Returns: list: The query embedding.
        """
        return self.nlp(text).vector.tolist()


from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
# Load the document and split it into chunks
test_txt = open("/opt/data/samples/test.txt").read()
# documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=300,
    chunk_overlap=30,
    length_function=len,
    is_separator_regex=False,
)

documents = text_splitter.create_documents([test_txt])


spacy_embeddings = SpacyEmbeddings()

vectordb = Chroma.from_documents(documents=documents, embedding=spacy_embeddings, persist_directory="./content")
collection = vectordb.get_or
collection.peek() # returns a list of the first 10 items in the collection
collection.count()
# query it
query = "what is BTOS?"
docs = vectordb.similarity_search(query)

# print results
print(docs[0].page_content)
