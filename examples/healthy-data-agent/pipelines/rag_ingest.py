def ingest_documents(collection, documents):
    for index, document in enumerate(documents):
        metadata = {
            "source": document["source"],
            "lineage": document["dataset"],
            "freshness": document["updated_at"],
            "pii_scan": "passed",
            "redaction": "emails_masked",
        }
        collection.add(ids=[str(index)], documents=[document["text"]], metadatas=[metadata])

