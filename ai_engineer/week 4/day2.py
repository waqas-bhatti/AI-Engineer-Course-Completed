from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
from itertools import combinations

load_dotenv()
embedding_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY")
)

def get_embedding(text):
    response = embedding_client.embeddings.create(input=text, model="qwen/qwen3-embedding-8b")
    return response.data[0].embedding

# ─────────────────────────────────────────
# 1. Cosine Similarity Function (numpy)
# ─────────────────────────────────────────

def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)
    
    return dot_product / (magnitude_a * magnitude_b)

# ─────────────────────────────────────────
# 2. Test Start — similar vs different texts
# ─────────────────────────────────────────

# text1 = "I am hungry."
# text2 = "I need food."
# text3 = "The weather is very nice today."

# emb1 = get_embedding(text1)
# emb2 = get_embedding(text2)
# emb3 = get_embedding(text3)

# similarity_1_2 = cosine_similarity(emb1, emb2)
# similarity_1_3 = cosine_similarity(emb1, emb3)

# print(f"'{text1}' vs '{text2}'")
# print(f"  Similarity: {similarity_1_2:.4f}  (high expected)")
# print()
# print(f"'{text1}' vs '{text3}'")
# print(f"  Similarity: {similarity_1_3:.4f}  (low expected)")

# ─────────────────────────────────────────
# 3. Multiple texts mein se best match dhundna
# ─────────────────────────────────────────

# def find_most_similar(query_text, candidate_texts):
#     """Finds the text in the candidates that is most similar to the query."""
#     query_embedding = get_embedding(query_text)
    
#     results = []
#     for candidate in candidate_texts:
#         candidate_embedding = get_embedding(candidate)
#         score = cosine_similarity(query_embedding, candidate_embedding)
#         results.append((candidate, score))
    
#     results.sort(key=lambda x: x[1], reverse=True)
#     return results


# candidates = [
#      "Python",
#     "Pakistan has a cricket match today.",
#     "Python is essential to become an Frontend Engineer.",
#     "Biryani recipe."
# ]

# query = "I want to learn coding."
# results = find_most_similar(query, candidates)

# print(f"\nQuery: '{query}'\n")
# for text, score in results:
#     print(f"  {score:.4f}  →  {text}");

# ===============Exercie=============
'''
1.Create a function filter_by_similarity(query, candidates, threshold=0.5) that:

Works like find_most_similar()
BUT only returns results whose similarity score is greater than the threshold
If no matches are found, return "No relevant matches found"

2. Create a function find_duplicates(text_list, threshold=0.9) that:

Finds highly similar (near-duplicate) texts in the list
Returns pairs of texts whose similarity score is greater than the threshold
(e.g., "I want to learn Python" and "I would like to learn Python" should be considered duplicates)

'''
# Solution 

'''
def cosine_similarity(vec_a, vec_b):
    a, b = np.array(vec_a), np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def filter_by_similarity(query, candidates, threshold=0.5):
    query_embedding = get_embedding(query)
    
    results = []
    for candidate in candidates:
        score = cosine_similarity(query_embedding, get_embedding(candidate))
        if score >= threshold:
            results.append((candidate, score))
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    if not results:
        return "No relevant matches found"
    return results

candidates = [
    "Python is a good language for beginners.",
    "There is a cricket match today.",
    "Python is necessary to become an frontend Engineer."
]

result = filter_by_similarity("I want to learn python.", candidates, threshold=0.4)
print(result)
    
'''
2. 

def cosine_similarity(vec_a, vec_b):
    a, b = np.array(vec_a), np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_duplicates(text_list, threshold=0.9):
    embeddings = {text: get_embedding(text) for text in text_list}
    duplicates = []
    
    # Check every unique pair (use combinations so pairs don’t repeat).
    for text1, text2 in combinations(text_list, 2):
        score = cosine_similarity(embeddings[text1], embeddings[text2])
        if score >= threshold:
            duplicates.append((text1, text2, score))
    
    return duplicates

texts = [
    "A man is eating food.",
    "A man is eating a piece of bread.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
    "A woman is playing violin.",
    "Two men pushed carts through the woods.",
    "A man is riding a white horse on an enclosed ground.",
    "A monkey is playing drums."
]

dupes = find_duplicates(texts, threshold=0.7)
for t1, t2, score in dupes:
    print(f"DUPLICATE ({score:.4f}):")
    print(f"  '{t1}'")
    print(f"  '{t2}'\n")
