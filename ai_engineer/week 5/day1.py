# 📆 DAY 1 — ChromaDB Basics (Real Vector Database)
import chromadb

# ─────────────────────────────────────────
# 1. Create a Persistent Client (Saved to Disk)
# ─────────────────────────────────────────
client = chromadb.PersistentClient(path="./chroma_data")

# ─────────────────────────────────────────
# 2. Create a Collection (similar to a table in SQL)
# ─────────────────────────────────────────

# collection = client.get_or_create_collection(name="my_notes")
# collection = client.get_or_create_collection(name="exercise_notes")
collection = client.get_or_create_collection(name="bulk_notes")

# ─────────────────────────────────────────
# 3. Add Documents — ChromaDB can generate embeddings automatically!
# ─────────────────────────────────────────

# collection.add(
#       documents = [
#             "Python AI Engineering ke liye sabse important language hai",
#         "RAG ka matlab Retrieval Augmented Generation hai",
#         "Vector databases embeddings store karne ke liye use hote hain",
#       ],
#     ids=["doc1", "doc2", "doc3"] # Har document ki unique ID zaroori hai
# )
# print(f"Total Documents in collections : {collection.count()} ")

# # ─────────────────────────────────────────
# # 4. Search Documents — in just one line!
# # ─────────────────────────────────────────

# results = collection.query(
#     query_texts=["RAG kya hota hai?"],
#     n_results=2
# )

# print("\nSearch results:")
# for doc, distance in zip(results["documents"][0], results["distances"][0]):
#     print(f"  Distance: {distance:.4f} → {doc}");


# 🔸 PART 2: IDs Aur Duplicate Handling
# ─────────────────────────────────────────
# Upsert — Add or Update (overwrites if the ID already exists)
# ─────────────────────────────────────────

# collection.upsert(
#     documents=["Python is a high-level programming language that is widely used in AI."],
#     ids=["doc1"]  # If doc1 already exists, it will be updated.
# )

# ─────────────────────────────────────────
# Specific delete the document
# ─────────────────────────────────────────

# collection.delete(ids=["doc3"])
# print(f"After delete: {collection.count()} documents")

# ─────────────────────────────────────────
# View all documents (useful for debugging)#─────────────────────────────────────────

# all_docs = collection.get()
# for doc_id, doc_text in zip(all_docs["ids"], all_docs["documents"]):
#     print(f"  [{doc_id}] {doc_text[:50]}")


# =====================Exercise=============
'''
Create a function add_document_auto_id(collection, text) that:

1. Uses collection.count() to automatically determine the next document ID (e.g., "doc4", "doc5", etc.).
Adds the document using the generated ID.
Returns the newly generated document ID.

Test the function by adding 3 documents.

2. Create a function bulk_import(collection, text_list) that:

Takes a list of texts as input.
Automatically generates IDs for each text.
Adds all documents in a single collection.add() call (do not call add() inside a loop — pass both documents and ids as lists in one call).
Prints the total number of documents added.

'''
# ===============Solution 1 ================
'''

def add_document_auto_id(collection, text):
    new_id = f"doc{collection.count() + 1}"
    collection.add(documents=[text], ids=[new_id])
    return new_id

id1 = add_document_auto_id(collection, "Embeddings convert text into numbers.")
id2 = add_document_auto_id(collection, "ChromaDB is a vector database.")
id3 = add_document_auto_id(collection, "FastAPI is a web framework for Python.")

print(f"Added IDs: {id1}, {id2}, {id3}")
print(f"Total: {collection.count()}")
'''

# Solution 2


def bulk_import(collection, text_list):
    start_count = collection.count()
    ids = [f"doc{start_count + i + 1}" for i in range(len(text_list))]
    
    collection.add(documents=text_list, ids=ids)
    
    print(f"✅ {len(text_list)} documents imported")
    return ids

notes = [
    "Chain-of-thought prompting improves reasoning accuracy.",
    "Few-shot prompting helps the model learn patterns from examples.",
    "JSON mode is used for structured output.",
]
bulk_import(collection, notes)
print(f"Total in collection: {collection.count()}")