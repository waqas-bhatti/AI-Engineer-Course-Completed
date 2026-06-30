# 📆 DAY 3 Search Engine Class (ChromaDB Based)

# vector_engine.py

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

chat_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY")
)
CHAT_MODEL = "poolside/laguna-m.1:free"

class VectorSearchEngine:
    """
    Production-ready search engine — based on ChromaDB.
    An upgrade of the Week 4 SemanticSearchEngine.
    """
    
    def __init__(self, collection_name="knowledge_base", persist_path="./chroma_data"):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
    
    def add_document(self, text, metadata=None):
        """Add a new document — the ID will be generated automatically."""
        doc_id = f"doc_{self.collection.count() + 1}"
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        return doc_id
    
    def add_documents_batch(self, text_list, metadata_list=None):
        """Add multiple documents in a single call."""
        start_count = self.collection.count()
        ids = [f"doc_{start_count + i + 1}" for i in range(len(text_list))]
        
        if metadata_list is None:
            metadata_list = [{} for _ in text_list]
        
        self.collection.add(documents=text_list, metadatas=metadata_list, ids=ids)
        return ids
    
    def search(self, query, top_k=3, category_filter=None):
        """Find relevant documents based on the query."""
        where_filter = {"category": category_filter} if category_filter else None
        
        if self.collection.count() == 0:
            return []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=min(top_k, self.collection.count()),
            where=where_filter
        )
        
        output = []
        for doc, distance, meta in zip(
            results["documents"][0], 
            results["distances"][0], 
            results["metadatas"][0]
        ):
            output.append({
                "text": doc,
                "distance": distance,
                "metadata": meta
            })
        return output
    
    def chat(self, user_message, top_k=3):
        """
        RAG-style chat: Search and generate an AI answer.
        This will work using the USER’s own message — no hardcoded query!
        """
        relevant_docs = self.search(user_message, top_k=top_k)
        
        if not relevant_docs:
            context = "No relevant documents were found."
        else:
            context = "\n".join([f"- {d['text']}" for d in relevant_docs])
        
        prompt = f"""Answer the user’s question using this context.
If the answer is not in the context, use your general knowledge, but clearly mention that it was not found in the context.

Context:
{context}

Question of User: {user_message}"""

        response = chat_client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        return {
            "answer": response.choices[0].message.content,
            "sources": relevant_docs
        }
    
    def count(self):
        return self.collection.count()


# ─── Test (It will only run when executed directly.) ───
if __name__ == "__main__":
    engine = VectorSearchEngine(collection_name="test_collection")
    
    if engine.count() == 0:
        engine.add_documents_batch(
            [
                "Python is one of the most important languages for AI engineering",
                "RAG generates AI responses by retrieving information from documents.",
                "ChromaDB is an open-source vector database.",
            ],
            [{"category": "ai"}, {"category": "ai"}, {"category": "tools"}]
        )
    
    # This simulates that the USER asked this question.
    result = engine.chat("ChromaDB kya hai?")
    print("Answer:", result["answer"])
    print("\nSources used:")
    for src in result["sources"]:
        print(f"  - {src['text']} (distance: {src['distance']:.4f})")