# https://ollama.com/blog/embedding-models

import ollama
import chromadb
from rich import print  # https://rich.readthedocs.io/en/stable/markup.html#console-markup
from rich.console import Console
# console = Console(highlighter=my_hl, theme=theme)

documents = [
    "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
    "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
    "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
    "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
    "Llamas are vegetarians and have very efficient digestive systems",
    "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
    "Many places in South America, including Peru, have packs of llamas in the mountains.",
    "House cats are not good pack animals, they are often solitary animals",
    "Dogs are not good pack animals, but do often live in packs",
]

prompts = [
    "How much do llamas weight?",
    'Where were llamas domesticated?',
    'Where are llamas?',
    'What animal is in Peru?',
    'What animal is a good pack animal?',
    'Where can I find llamas?',
    'How long do llamas live?',
   ]


client = chromadb.Client()

collections = client.list_collections()
print(f"Collections: {collections}")

col_name = 'test-collection'
if(col_name in collections):
    collection = client.get_collection(name=col_name) # Get a collection object from an existing collection, by name. Will raise an exception if it's not found.
    print(f"[green]Found collection: {collection}[/]")
else:
    print(f"[blue]Could not find existing collection: {col_name}, create it now...[/]")
    # collection = client.get_or_create_collection(name=col_name) # Get a collection object from an existing collection, by name. If it doesn't exist, create it.
    # client.delete_collection(name="my_collection") # D
    collection = client.create_collection(name=col_name)

# store each document in a vector embedding database
for i, d in enumerate(documents):
    print(f"{i}) add doc: {d}")
    collection.add(
        ids=[str(i)],
        documents=[d]
    )

existing_count = collection.count()
print(f"existing doc count: {existing_count}")
ids = collection.get(include=[])
print(f"collection ids: {ids}")

print(f"\nready for queries on collection: {col_name}")

for prompt in prompts:
    print(f"\n[green bold]QUESTION: {prompt}[/]")
    # use default collection embedding function for the prompt and retrieve the most relevant doc
    results = collection.query(
        query_texts=[prompt],
        n_results=3
    )

    answers = results["documents"][0]
    for i, answer in enumerate(answers):
        id = results["ids"][0][i]
        distance = results["distances"][0][i]
        print(f"\t{id} ({distance:.2f}) ANSWER: {answer}")

print("Done!?")
