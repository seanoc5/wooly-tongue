# Demo notes and links


## Embedding Comparison(s)

### Popular Models
* OpenAI models
  * 'text-embedding-3-small',
    * small, fast, quite nice
  * 'text-embedding-3-large',
    * larger, better accuracy, but significantly slower
  * 'text-embedding-ada-002'
    * old/outdated defacto-standard
* Open Source models
  * 


## Generative vs Extractive
https://haystack.deepset.ai/blog/generative-vs-extractive-models

### Reader-Retriever Haystack Pipeline
Their purely extractive property means the model can only provide answers that quote verbatim from a text. Abstraction, paraphrasing, and the formation of well-formed answers are not in the repertoire of this model family.

Because of their extractive nature, these models have no use for storing factual information, and therefore do not necessarily benefit from having more parameters. Compared to their generative cousins, extractive models are therefore usually much smaller in size and require less training data.

## Use cases / contexts
**Semantic search** seems most _trustworthy_ at the moment. Generative ML/AI is quite impressive, but ultimately the challenge of hallucinations makes it difficult to rely on. 

**Summaraization & classification** also do well for those use cases that benefit from either/both.

**RAG** has great potential if it is possible to get good initial `retrieval`, otherwise GIGO

**ChatBots** are nice and flashy, but so far it is tough to show actual benefit in many cases.

### Semantic Search
**Brute-force/development:**
* decompose corpus into documents and (likely) document segments.
* embed and store document vectors
* get query 
  * embed it
  * send to storage for filtering and/or search
    * NOTE: pay attention to scoring method of the embedding model
    * e.g. cosine, doc-product,...
  * development mode: in memory doc store, compare all docs
  * production mode: use vector-db

**More Elegant:**
* Retriever-Reader
  * https://haystack.deepset.ai/tutorials/03_scalable_qa_system (old version)
  * these pipelines tend to be shorter/more terse than RAG (see below)


### RAG (retrieval augmented generation)
Often: quick/light sparse keyword search (solr, elastic, ... BM25/tf-idf).  
Aim is to find most 'relevant' documents already indexed, and add them to the prompt to the LLM.  
LLM is trained on... large language... and uses that training to analyze the prompt-content (prompt stuffing) and combines the training with the 'new' content in the prompt to return delicious peanutbutter cups. 
**Almost** like micro-training the LLM on new documents. 


### Summarization


### Classification


### General chatbot




## Notes / ToDo
https://haystack.deepset.ai/tutorials/03_scalable_qa_system
```from haystack import Pipeline
from haystack.nodes import TextConverter, PreProcessor

indexing_pipeline = Pipeline()
text_converter = TextConverter()
preprocessor = PreProcessor(
    clean_whitespace=True,
    clean_header_footer=True,
    clean_empty_lines=True,
    split_by="word",
    split_length=200,
    split_overlap=20,
    split_respect_sentence_boundary=True,
)
```
