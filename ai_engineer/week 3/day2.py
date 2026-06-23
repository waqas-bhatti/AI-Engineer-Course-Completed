# ===========Chain-of-Thought (CoT) Prompting=========
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("2_KEY_OF_LONGCAT_API_KEY"), base_url="https://api.longcat.chat/openai")
MODEL = "LongCat-2.0-Preview"

# ─────────────────────────────────────────
# 1. WITHOUT Chain-of-Thought
# ─────────────────────────────────────────
# print("Without Chain of Thought")

# problem = """Ahmed has 45 rupees. He bought 3 pencils, each costing 8 rupees.
# Then his friend gave him 20 rupees. How much money does Ahmed have now?"""

# response = client.chat.completions.create(
#     model=MODEL,
#     messages=[{"role": "user", "content": problem}],
#     max_tokens=100
# )
# print("\n🔸 WITHOUT CoT:")
# print(response.choices[0].message.content)
# print()

# # ─────────────────────────────────────────
# # 2. WITH Chain-of-Thought
# # ─────────────────────────────────────────

# cot_problem = problem + "\n\nThink step by step, show each step clearly, then give the final answer."

# response2 = client.chat.completions.create(
#     model=MODEL,
#     messages=[{"role": "user", "content": cot_problem}],
#     max_tokens=300
# )
# print("🔸 WITH CoT:")
# print(response2.choices[0].message.content)

# =================Exercise===============
'''
Create 3 multi-step word problems (in a mix of Urdu and English, based on daily-life scenarios).

For each problem, test it in two ways:
1. WITHOUT Chain of Thought (CoT)
2. WITH Chain of Thought (CoT)

Then compare the results and observe:
Did the model make any mistakes when solving the problem WITHOUT CoT?
'''
# ======================Solution===========
problems = [
    "Ali ke paas 12 Bottles thi. Usne apne 3 dostoon ko 2-2 dein. Phir usne 8 nayi khareedi. Ab kitni bottles hain?",
    "Ek bus mein 40 log thay. 15 utar gaye next stop pe, phir 22 chad gaye. Ab kitne log hain bus mein?",
    "Sara ne 5 kitabein khareedi, har ek 150 rupay ki. Usne 100 rupay discount mila. Total kitna paisa lagaya?",
]

for problem in problems:
    print(f"PROBLEM: {problem}\n")
    
    # Without CoT
    r1 = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": problem}], max_tokens=80)
    print(f"WITHOUT CoT: {r1.choices[0].message.content}")
    
    # With CoT
    cot_prompt = problem + "\n\nStep by step socho, har step dikhao."
    r2 = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": cot_prompt}], max_tokens=250)
    print(f"WITH CoT: {r2.choices[0].message.content}")
    print("-" * 50)

