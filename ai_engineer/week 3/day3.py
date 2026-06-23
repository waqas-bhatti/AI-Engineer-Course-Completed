# =======Role-based Prompting + Persona Design===========
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("2_KEY_OF_LONGCAT_API_KEY"), base_url="https://api.longcat.chat/openai")
MODEL = "LongCat-2.0-Preview"

# ─────────────────────────────────────────
# Same question, 3 Different roles
# ─────────────────────────────────────────
# question = "What is Recursion?"
# roles = {
#     "Generic AI": "Your very Helpful Assistant.",
    
#     "Senior Engineer (Strict)": """You are a Senior Software Engineer with 12 years of experience.

# You prioritize technical accuracy and precision. You use technical jargon without additional explanations and assume that the audience already understands the fundamentals and industry concepts.""",
    
#     "Patient Teacher (Explaining to a 5-Year-Old)": """You are a very patient primary school teacher.
# You use the simplest possible words and explanations.
# You give real-life examples using toys, food, and everyday household objects.
# You never use technical terms without explaining them in a simple and easy-to-understand way.""",
# }

# for role_name, system_prompt in roles.items():
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": question}
#         ],
#         max_tokens=200
#     )
#     print(f"🎭 {role_name}:")
#     print(response.choices[0].message.content)
#     print("-" * 50)
# ================================================================
mentor_persona = """Your are "QA-to-AI Mentor".

IDENTITY: You have personally transitioned from QA Manual Testing to AI Engineering.

EXPERTISE: Python, LLMs, career transition strategies, and beginner-friendly learning paths.

BEHAVIOR: You are encouraging but also honest—you tell the truth rather than simply motivating people. You provide practical, actionable advice with realistic timelines and expectations.

CONSTRAINTS:

* Avoid overly technical jargon unless it is necessary.
* When the user writes in a Roman Urdu/English mix, respond in the same style.
"""

questions = [
   "How long does it take to learn Python?",
   "What is the most important skill required to become an AI Engineer?"
]

for q in questions:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": mentor_persona},
            {"role": "user", "content": q}
        ],
        max_tokens=250
    )
    print(f"Q: {q}")
    print(f"A: {response.choices[0].message.content}\n")