# 📆 DAY 2 — Metadata Filtering + Advanced Queries

import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="categorized_notes")


# ─────────────────────────────────────────
# 1. Added with Metadata
# ─────────────────────────────────────────

collection.add(
    documents=[
        "Python list mutable hota hai, change kar sakte ho",
        "Tuple immutable hota hai Python mein",
        "React mein useState state manage karta hai",
        "Next.js App Router file-based routing use karta hai",
        "FastAPI automatic API docs generate karta hai",
    ],
    metadatas=[
        {"category": "python", "difficulty": "beginner"},
        {"category": "python", "difficulty": "beginner"},
        {"category": "frontend", "difficulty": "intermediate"},
        {"category": "frontend", "difficulty": "intermediate"},
        {"category": "backend", "difficulty": "intermediate"},
    ],
    ids=["m1", "m2", "m3", "m4", "m5"]
)

# ─────────────────────────────────────────
# 2. **Filtered search — only within the "python" category**
# ─────────────────────────────────────────

results = collection.query(
    query_texts=["Mutable kya hota hai?"],
    n_results=3,
    where={"category": "python"}   # this is a Filter
)

print("Filtered (python only):")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"  [{meta['category']}] {doc}")

# ─────────────────────────────────────────
# 3. Multiple conditions ($and operator)
# ─────────────────────────────────────────

results2 = collection.query(
    query_texts=["How to manage the state?"],
    n_results=3,
    where={
        "$and": [
            {"category": "frontend"},
            {"difficulty": "intermediate"}
        ]
    }
)

print("\nFiltered (frontend + intermediate):")
for doc in results2["documents"][0]:
    print(f"  {doc}");

# =====================Exercise==================
'''
Create a function smart_search(collection, query, category=None, n=3) that:

Applies a filter if a category is provided.
Searches across all documents if no category is provided.
Returns the results along with metadata.
'''
# =====================Solution==================

def smart_search(collection, query, category=None, n=3):
    where_filter = {"category": category} if category else None
    
    results = collection.query(
        query_texts=[query],
        n_results=n,
        where=where_filter
    )
    
    output = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        output.append({"text": doc, "metadata": meta})
    return output

# Test (pehle category wali collection use karo agar hai)
results = smart_search(collection, "Python kya hai?")
for r in results:
    print(r)