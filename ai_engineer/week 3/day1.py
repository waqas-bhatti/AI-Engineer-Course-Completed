# ============ Zero-shot vs Few-shot Prompting ===========
'''
ZERO-SHOT PROMPTING
└── Give the task directly without providing any examples
    "Tell me the sentiment of this sentence: 'This movie was very good'"
    The AI has to figure out on its own what "sentiment" means
    and what output format is expected.

FEW-SHOT PROMPTING
└── First provide 2–3 examples, then ask the actual question
    Example 1: "The movie was good" → Positive
    Example 2: "The food was terrible" → Negative
    Actual: "The service was slow" → ?
    The AI gets a clear pattern of what kind of output is expected.
'''
'''
WHEN TO USE EACH:

Zero-shot  → Use for simple, common tasks where the AI already
             understands what to do.
             Examples:
             - Translation
             - Basic Q&A
             - Summarization
             - Sentiment Analysis

Few-shot   → Use when you need a specific output format or when
             the AI seems confused about the task.
             Examples:
             - Custom classification
             - Structured JSON output
             - Special writing formats
             - Domain-specific tasks

             By showing a few examples first, the AI learns the
             exact pattern and produces more consistent results.
'''

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.longcat.chat/openai")
MODEL = "LongCat-2.0-Preview"

# ─────────────────────────────────────────
# 1. ZERO-SHOT — Without Example
# ─────────────────────────────────────────

# zero_shot_prompt = """Determine the sentiment of this customer review (Positive/Negative/Neutral):

# Review: "The delivery time was very long, but the product quality is good."
# """

# response = client.chat.completions.create(
#     model=MODEL,
#     messages=[{"role": "user", "content": zero_shot_prompt}],
#     max_tokens=100
# )
# print("🔸 ZERO-SHOT Result:")
# print(response.choices[0].message.content)
# print()

# # ─────────────────────────────────────────
# # 2. FEW-SHOT — With Example (consistent format)
# # ─────────────────────────────────────────

# few_shot_prompt = """Classify the sentiment of customer reviews. Reply with only one word: Positive, Negative, or Mixed..

# Review: "The product is very good, and I also received fast delivery."
# Sentiment: Positive

# Review: "The quality is completely bad, a waste of money."
# Sentiment: Negative

# Review: "The delivery time was very long, but the product quality is good."
# Sentiment:"""

# response2 = client.chat.completions.create(
#     model=MODEL,
#     messages=[{"role": "user", "content": few_shot_prompt}],
#     max_tokens=20
# )
# print("🔸 FEW-SHOT Result:")
# print(response2.choices[0].message.content)

# ================Exercise============
'''
Task: Write a zero-shot prompt that extracts the category from product names
(Electronics/Clothing/Food/Other)

Then create a few-shot version of the same task (with 3 examples).

Test both prompts with 5 different products:
- "iPhone 15"
- "Cotton T-Shirt"
- "Biryani Masala"
- "Laptop Stand"
- "Random item"

OBSERVE: Which version produces more consistent output format?
'''
# ==============Solution===================
products = ["iPhone 15", "Cotton T-Shirt", "Biryani Masala", "Laptop Stand", "Random item"]

# Zero-shot
print("=== ZERO-SHOT ===")
for product in products:
    prompt = f"Which category does this product belong to? (Electronics/Clothing/Food/Other)\nProduct: {product}"
    response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}], max_tokens=20)
    print(f"{product}: {response.choices[0].message.content}")

print("\n=== FEW-SHOT ===")
for product in products:
    prompt = f"""Determine the product category. Reply with only one word: Electronics, Clothing, Food, or Other..

Product: Samsung TV
Category: Electronics

Product: Jeans
Category: Clothing

Product: Chocolate Bar
Category: Food

Product: {product}
Category:"""
    response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}], max_tokens=10)
    print(f"{product}: {response.choices[0].message.content}")

#     ================Exercise==============
'''
Ek few-shot prompt banao jo Roman Urdu ko proper Urdu script mein convert kare.
3 examples do (Roman Urdu → Urdu script)
Phir 3 naye Roman Urdu sentences test karo.
'''


few_shot_prompt_template = """Roman Urdu ko Urdu script mein convert karo.

Roman: "aap kaise hain"
Urdu: "آپ کیسے ہیں"

Roman: "main theek hun"
Urdu: "میں ٹھیک ہوں"

Roman: "shukriya"
Urdu: "شکریہ"

Roman: "{sentence}"
Urdu:"""

test_sentences = ["mujhe Python seekhna hai", "yeh bohot acha hai", "kal milte hain"]

for sentence in test_sentences:
    prompt = few_shot_prompt_template.format(sentence=sentence)
    response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}], max_tokens=500)
    print(f"Roman: {sentence}")
    print(f"Urdu: {response.choices[0].message.content}\n")
