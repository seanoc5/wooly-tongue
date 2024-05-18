# https://ollama.com/blog/embedding-models

import chromadb
from rich import print  # https://rich.readthedocs.io/en/stable/markup.html#console-markup

documents = [
    "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
    "Llamas were first domesticated and used as pack animals 4,001 to 5,001 years ago in the Peruvian highlands",
    "Llamas can grow as much as 8 feet tall though the average llama between 7 feet 8 inches and 7 feet 11 inches tall",
    "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
    "Llamas are vegetarians and have very efficient digestive systems",
    "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
    "Many places in South America, including Peru, have packs of llamas in the mountains.",
    "Dogs have an average life-span of a dozen years or so.",
    "House cats generally do not live in packs, they are often solitary animals, even in Cusco.",
    "Dogs are not good pack animals, but do often live in packs, sometimes in Lima",
    "Mules are beasts of burden; they can carry substantial loads on trips."
]

questions = {
    1:{'q':"How much do llamas weight?", 'ids':[3,2]},
    2:{'q':'Where were llamas domesticated?', 'ids':[1,6]},
    3:{'q':'llamas domesticated', 'ids':[1,6]},
    4:{'q':'What animal is in Peru?', 'ids':[1,6]},
    5:{'q':'good pack animal?', 'ids':[1,10]},
    6:{'q':'animals live in packs', 'ids':[9,8]},
    7:{'q':'How long do animals live?', 'ids':[7,5]},
}


client = chromadb.Client()

collections = client.list_collections()
print(f"Collections: {collections}")

col_name = 'test-collection'
if(col_name in collections):
    collection = client.get_collection(name=col_name) # Get a collection object from an existing collection, by name. Will raise an exception if it's not found.
    print(f"[green]Found collection: {collection}[/]")
else:
    print(f"[blue]Could not find existing collection: {col_name}, create it now...[/]")
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

for q_number in questions:
    prompt = questions[q_number]['q']
    expected_ids = questions[q_number]['ids']
    print(f"\n[blue bold]{q_number}) QUESTION: {prompt}[/] (expected ids: {expected_ids})")
    # use default collection embedding function for the prompt and retrieve the most relevant doc
    results = collection.query(
        query_texts=[prompt],
        n_results=3
    )

    answers = results["documents"][0]
    for i, answer in enumerate(answers):
        id = int(results["ids"][0][i])
        distance = results["distances"][0][i]
        if(i < len(expected_ids)):
            expected = expected_ids[i]
            if(id==expected):
                print(f"\t[green bold]got({id}):expected({expected}) (distance:{distance:.2f}): {answer}[/]")
            else:
                print(f"[red bold]\tgot({id}):expected({expected}) (distance:{distance:.2f}): {answer}[/]")
                print(f"\t\t\t\t\t  [light_slate_grey]{documents[expected]}")
        else:
            print(f"\t[light_slate_grey](outside test)      (distance:{distance:.2f}): {answer}[/]")


print("Done!?")
