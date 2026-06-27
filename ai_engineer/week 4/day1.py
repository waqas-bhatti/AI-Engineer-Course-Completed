from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

embedding_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY")
)

# ─────────────────────────────────────────
# 1. Generate a simple embedding.
# ─────────────────────────────────────────

# response = embedding_client.embeddings.create(
#     input="I am learning Python",
#     model="google/gemini-embedding-001"
# )

# embedding = response.data[0].embedding
# print(f"Embedding length: {len(embedding)}")  # 3072
# print(f"First 5 numbers: {embedding[:5]}")



# ─────────────────────────────────────────
# 2. Reusable function banao
# ─────────────────────────────────────────

# def get_embedding(text):
#     """Kisi bhi text ka embedding return karta hai"""
#     response = embedding_client.embeddings.create(
#         input=text,
#         model="qwen/qwen3-embedding-8b",
#       #   encoding_format="float"
#     )
#     return response.data[0].embedding

# # ─────────────────────────────────────────
# # 3. Do similar aur do different texts compare karo (visually)
# # ─────────────────────────────────────────

# texts = [
#     "Mujhe bhook lagi hai",
#     "Khana chahiye mujhe",
#     "Aaj weather bohot acha hai",
# ]

# embeddings = [get_embedding(t) for t in texts]

# for i, text in enumerate(texts):
#     print(f"\nText {i+1}: '{text}'")
#     print(f"First 5 values: {embeddings[i][:5]}")

# ==============Exercise================
'''
1. Create a function get_embedding_cached(text) that:

Caches embeddings in a dictionary (if the same text appears again, it should not make another API call)
Prints cache hit/miss status ("✅ From cache" or "🔄 New API call")

Test it by sending the same text 3 times — the API call should only happen the first time.

=====================================================
2. Create a function get_embeddings_batch(text_list) that:

Takes a list of texts
Generates embeddings for all of them (using a loop)
Returns a dictionary: {text: embedding}
Prints progress ("Processing 3/10...")
'''    
# ============Solution==================
# _cache = {}

# def get_embedding_cached(text):
#     if text in _cache:
#         print(f"✅ From cache: '{text[:30]}'")
#         return _cache[text]
    
#     print(f"🔄 New API call: '{text[:30]}'")
#     response = embedding_client.embeddings.create(input=text, model="qwen/qwen3-embedding-8b")
#     embedding = response.data[0].embedding
#     _cache[text] = embedding
#     return embedding

# # Test
# get_embedding_cached("What is python?")
# get_embedding_cached("What is python?")  # Cache se aayega
# get_embedding_cached("What is python?")  # Cache se aayega
# get_embedding_cached("How becoma a AI Engineer?") # New Api Call

# 2 Solution ===========================
def get_embeddings_batch(text_list):
    results = {}
    total = len(text_list)
    
    for i, text in enumerate(text_list, 1):
        print(f"Processing {i}/{total}...")
        response = embedding_client.embeddings.create(input=text, model="qwen/qwen3-embedding-8b")
        results[text] = response.data[0].embedding
    
    print(f"✅ Done! {total} embeddings generated")
    return results

texts = [
    "Python programming language hai",
    "JavaScript language used for web development",
    "AI Engineer are work with LLMs",
]
embeddings_dict = get_embeddings_batch(texts)
print(f"\nKeys: {list(embeddings_dict.keys())}")