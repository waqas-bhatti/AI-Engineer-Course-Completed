#  ===========Mini Semantic Search Engine (Python)========='

from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
import json


load_dotenv()

embedding_client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://openrouter.ai/api/v1")
chat_client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.longcat.chat/openai")
CHAT_MODEL = "LongCat-2.0-Preview"

# class SemanticSearchEngine:
#     """
#     A mini semantic search engine.
#     Stores documents, generates embeddings for them,
#     and finds the most relevant documents for a given query.
#     """
    
#     def __init__(self):
#         self.documents = []      # Original text
#         self.embeddings = []     # Corresponding embeddings
    
#     def add_document(self, text):
#         """Add a new document and generate its embedding."""
#         embedding = self._get_embedding(text)
#         self.documents.append(text)
#         self.embeddings.append(embedding)
#         print(f"✅ Added: '{text[:50]}...'")
    
#     def add_documents_batch(self, text_list):
#         """Multiple documents ek saath add karo"""
#         for text in text_list:
#             self.add_document(text)
    
#     def _get_embedding(self, text):
#         response = embedding_client.embeddings.create(input=text, model="qwen/qwen3-embedding-8b")
#         return response.data[0].embedding
    
#     def _cosine_similarity(self, vec_a, vec_b):
#         a, b = np.array(vec_a), np.array(vec_b)
#         return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
#     def search(self, query, top_k=3):
#         """Find the most relevant documents for the query."""
#         if not self.documents:
#             return []
        
#         query_embedding = self._get_embedding(query)
        
#         scores = []
#         for i, doc_embedding in enumerate(self.embeddings):
#             score = self._cosine_similarity(query_embedding, doc_embedding)
#             scores.append((self.documents[i], score))
        
#         scores.sort(key=lambda x: x[1], reverse=True)
#         return scores[:top_k]
    
#     def search_with_answer(self, query, top_k=2):
#         """
#         BONUS: Generate an answer using search + AI
#         (This is a mini preview of RAG — we will go into a deep dive in Week 6)
#         """
#         top_results = self.search(query, top_k=top_k)
        
#         if not top_results:
#             return "No relevant document was found."
        
#         context = "\n".join([f"- {doc}" for doc, score in top_results])
        
#         prompt = f""" Answer the question using this context.:

# Context:
# {context}

# Question: {query}

# Answer only based on the provided context, If the answer is not in the context, say "I don't know."""

#         response = chat_client.chat.completions.create(
#             model=CHAT_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=200
#         )
#         return response.choices[0].message.content


# # ─── Run tests (this will only execute when the file is run directly). ───
# if __name__ == "__main__":
#     engine = SemanticSearchEngine()

#     faqs = [
#         "Python is the most important programming language for AI engineering.",
#     "RAG stands for Retrieval-Augmented Generation. It retrieves information from documents to generate AI responses.",
#     "Vector databases are used to store embeddings.",
#     "Prompt engineering is the technique of crafting prompts to obtain better responses from AI.",
#     "AI agents can use tools to complete complex tasks.",
#     "A token is the basic unit of processing in AI models, roughly equivalent to 4 characters.",
#     ]

#     engine.add_documents_batch(faqs)

#     print("\n" + "=" * 60)
#     results = engine.search("What is RAG?", top_k=2)
#     print("Search results:")
#     for doc, score in results:
#         print(f"  {score:.4f} → {doc}")

#     print("\n" + "=" * 60)
#     answer = engine.search_with_answer("Vector databases are used to store embeddings?")
#     print("AI Answer:", answer)

# # ========================Exercise===================
'''
1. # Using the SemanticSearchEngine class, build your own "Personal Learning Notes" search engine:
# - Add 8–10 notes of what you learned in Week 1–3 (in your own words)
# - Test 3 queries
# - Show the best matching notes with scores

2. 
# Extend the SemanticSearchEngine class:
# - Store a "category" with each document (in a tuple/dict)
# - Add an optional "category_filter" parameter in the search() method
# - If a filter is provided, search only within documents of that category

'''
# # =====================Solution 1 ======================

# notes_engine = SemanticSearchEngine()

# my_notes = [
#     "f-strings se Python mein variables ko strings ke andar dalte hain",
#     "Dictionary mein .get() method safe tarika hai value nikalne ka, error nahi aata",
#     "OpenAI API mein messages list mein system, user, assistant roles hote hain",
#     "Temperature parameter response ki creativity control karta hai, 0 se 1 tak",
#     "JSON mode response_format se AI ko force karte hain structured output dene ke liye",
#     "Function calling se AI tools (calculator, weather) use kar sakta hai",
#     "Few-shot prompting mein examples dete hain AI ko pattern samjhane ke liye",
#     "Chain-of-thought prompting AI ko step-by-step sochne ke liye kehta hai",
# ]

# for note in my_notes:
#     notes_engine.add_document(note)

# queries = ["How can we get AI to produce structured responses?", "How can variables be inserted into strings?", "How can we teach AI to use tools?"]

# for q in queries:
#     print(f"\nQuery: {q}")
#     results = notes_engine.search(q, top_k=2)
#     for doc, score in results:
#         print(f"  {score:.4f} → {doc}")

# ============================Solution 2 =================

class CategoryAwareSearchEngine:
    def __init__(self):
        self.documents = []  # Every item: {"text": ..., "category": ..., "embedding": ...}
    
    def add_document(self, text, category):
        embedding = self._get_embedding(text)
        self.documents.append({"text": text, "category": category, "embedding": embedding})
    
    def _get_embedding(self, text):
        response = embedding_client.embeddings.create(input=text, model="qwen/qwen3-embedding-8b")
        return response.data[0].embedding
    
    def _cosine_similarity(self, vec_a, vec_b):
        a, b = np.array(vec_a), np.array(vec_b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def search(self, query, top_k=3, category_filter=None):
        query_embedding = self._get_embedding(query)
        
        candidates = self.documents
        if category_filter:
            candidates = [d for d in self.documents if d["category"] == category_filter]
        
        scores = [(d["text"], d["category"], self._cosine_similarity(query_embedding, d["embedding"])) 
                   for d in candidates]
        scores.sort(key=lambda x: x[2], reverse=True)
        return scores[:top_k]


engine = CategoryAwareSearchEngine()
engine.add_document("Python lists are mutable.", "python")
engine.add_document("In React, the useState hook is used to manage state.", "frontend")
engine.add_document("Tuples are immutable in Python.", "python")
engine.add_document("In Next.js, components are used to build the frontend.", "frontend")

print("Without filter:")
for text, cat, score in engine.search("State kaise manage karte hain?"):
    print(f"  [{cat}] {score:.4f} → {text}")

print("\nWith category_filter='frontend':")
for text, cat, score in engine.search("What is Frontend?", category_filter="frontend"):
    print(f"  [{cat}] {score:.4f} → {text}")