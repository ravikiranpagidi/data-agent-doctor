from langgraph.graph import StateGraph
from chromadb import Client


def embed_documents(documents):
    client = Client()
    collection = client.get_or_create_collection("customer_docs")
    for index, document in enumerate(documents):
        collection.add(ids=[str(index)], documents=[document])

