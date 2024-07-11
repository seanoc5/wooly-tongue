# https://ollama.com/blog/embedding-models

import ollama
import chromadb

documents = [
    "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
    "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
    "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
    "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
    "Llamas are vegetarians and have very efficient digestive systems",
    "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]

# https://docs.trychroma.com/integrations/ollama
# import chromadb.utils.embedding_functions as embedding_functions
# ollama_ef = embedding_functions.OllamaEmbeddingFunction(
#     url="http://localhost:11434/api/embeddings",
#     model_name="llama2",
# )
# embeddings = ollama_ef(["This is my first text to embed",
#                         "This is my second document"])

model_names = ["mxbai-embed-large", 'llama2', 'llama3']
client = chromadb.Client()

for model_name in model_names:
    print("Embedding model for {}...".format(model_name))

    collection = client.create_collection(name=model_name)

    # store each document in a vector embedding database
    for i, d in enumerate(documents):
        response = ollama.embeddings(model=model_name, prompt=d)
        embedding = response["embedding"]
        print(f"\t\t{i}) Save embedding for doc: {d}")
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d]
        )

    # next
    # an example prompt
    # prompt = "What animals are llamas related to?"
    prompt = "How much do llamas weight?"
    print("QUESTION: " + prompt)

    # generate an embedding for the prompt and retrieve the most relevant doc
    response = ollama.embeddings(
        prompt=prompt,
        model=model_name
    )
    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=3
    )
    answers = results["documents"][0]
    for i, answer in enumerate(answers):
        print(f"\t\t{i}) ANSWER: {answer}")

    # data = results['documents'][0][0]
    # print(data)

print("Done!?")
