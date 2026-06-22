# 🔸 ============PART 1: JSON Mode=============
# day4_json_mode.py

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv("KEY_OF_LONGCAT_API_KEY"),
    base_url="https://api.longcat.chat/openai"
)

# ─────────────────────────────────────────
# 1. JSON Mode — Force the AI to return JSON.
# ─────────────────────────────────────────

# response = client.chat.completions.create(
#     model="LongCat-2.0-Preview",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a data extraction assistant. Always return valid JSON."
#         },
#         {
#             "role": "user",
#             "content": """Extract information from this text in JSON format.:
            
#             'Ahmed Khan is a 28-year-old Software Engineer who lives in Lahore, 
#             email: ahmed@example.com'
            
#             JSON format: {"name": "", "age": 0, "city": "", "job": "", "email": ""}
#             """
#         }
#     ],
#     response_format={"type": "json_object"},  # This turns on JSON mode.
# )

# result_text = response.choices[0].message.content
# print("Raw response:", result_text)

# # Convert JSON string into a Python dictionary.
# data = json.loads(result_text)
# print(f"\nParsed data:")
# print(f"  Name: {data['name']}")
# print(f"  Age: {data['age']}")
# print(f"  City: {data['city']}")

# # ─────────────────────────────────────────
# # 2. Reusable Extraction Function
# # ─────────────────────────────────────────

# def extract_structured_data(text, schema_description):
#     """
#   Extracts structured data from text.
    
#     Args:
#         text: Source text
#         schema_description: Describe the required JSON schema as a string.
#     """
#     response = client.chat.completions.create(
#         model="LongCat-2.0-Preview",
#         messages=[
#             {
#                 "role": "system",
#                 "content": f"Extract data as JSON. Schema: {schema_description}. Return ONLY valid JSON."
#             },
#             {"role": "user", "content": text}
#         ],
#         response_format={"type": "json_object"},
#         temperature=0  # For JSON extraction, 0 is best for consistent results.
#     )
    
#     return json.loads(response.choices[0].message.content)


# # Test — Extract sentiment and rating from product reviews.
# review = "The phone is highly praised for its camera quality and battery life lasting all day. It is considered worthy of 5 stars, but the price is slightly high."

# result = extract_structured_data(
#     review,
#     schema_description='{"sentiment": "positive/negative/neutral", "rating_out_of_5": number, "pros": [list], "cons": [list]}'
# )
# print("\n📦 Review Analysis:")
# print(json.dumps(result, indent=2, ensure_ascii=False))

# =====================Exercise====================
"""
**"Create an array of 5 customer reviews. From each review, extract:

sentiment (positive/negative/neutral)
category (product_quality/shipping/customer_service/pricing/other)
urgency (needs_response/no_response_needed)

Print all results in a summary table."
"""
# ===================Solution=======================
def classify_review(review_text):
    response = client.chat.completions.create(
        model="LongCat-2.0-Preview",
        messages=[
            {
                "role": "system",
                "content": """Classify this review. Return JSON:
{"sentiment": "positive/negative/neutral", 
 "category": "product_quality/shipping/customer_service/pricing/other",
 "urgency": "needs_response/no_response_needed"}"""
            },
            {"role": "user", "content": review_text}
        ],
        response_format={"type": "json_object"},
        temperature=0
    )
    return json.loads(response.choices[0].message.content)

reviews = [
    "Product was damaged upon delivery, very bad experience.",
    "Quality is very good, I am completely satisfied.",
    "Price is a bit high but acceptable according to the quality.",
    "Customer service is not responding to my calls, I have been trying for 3 days.",
    "Average product, nothing special.",
]

print(f"{'Review':<45} | {'Sentiment':<10} | {'Category':<18} | {'Urgency'}")
print("-" * 100)

for review in reviews:
    result = classify_review(review)
    print(f"{review[:43]:<45} | {result['sentiment']:<10} | {result['category']:<18} | {result['urgency']}"
    )
