# =================First OpenAI API Call===============
# Setup
# pip install openai python-dotenv

# 🔸 PART 1: Pehla API Call + USER MESSAGE
from groq import Groq
from dotenv import load_dotenv
import os
"""
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "Your Python Teacher Let me in Learn Simple words with example"
        },
        {
            "role": "user",
            "content": "What is AI Engineer?"
        }
    ],
    temperature=0.7,     # 0 = consistent, 1 = creative
    max_tokens=300       # Maximum words/tokens in response
)

print(response.choices[0].message.content)
print("\n📊 Token Usage:")
print(f"  Prompt tokens: {response.usage.prompt_tokens}")
print(f"  Completion tokens: {response.usage.completion_tokens}")
print(f"  Total tokens: {response.usage.total_tokens}")

cost = response.usage.total_tokens * 0.000002
print(f"  Estimated cost: ${cost:.6f}")

"""

# ─────────────────────────────────────────
# Real Chatbot — Multi-turn conversation
# ─────────────────────────────────────────

# load_dotenv()

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )

# def chat_with_ai(system_prompt="AI Your very Helpful"):
#     """Talk to in Terminal"""
    
#     # Add the system prompt to the history.
#     conversation = [
#         {"role": "system", "content": system_prompt}
#     ]
    
#     print("🤖 AI Chatbot is ready! Type 'quit' to exit")
#     print("─" * 50)
    
#     while True:
#         # Take Input from User
#         user_input = input("\n👤 You Enter: ").strip()
        
#         if not user_input:
#             continue
        
#         if user_input.lower() in ["quit", "exit", "bye", "q"]:
#             print("🤖 AI: Goodbye! See you soon! 👋")
#             break
        
#         # Add the User message history
#         conversation.append({
#             "role": "user",
#             "content": user_input
#         })
        
#         # Call the API
#         try:
#             response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=conversation,
#                 temperature=0.7,
#                 max_tokens=200 
#             )
            
#             # Find the AI response
#             ai_response = response.choices[0].message.content
            
#             # Add the system prompt to the history."
#             conversation.append({
#                 "role": "assistant",
#                 "content": ai_response
#             })
            
#             print(f"\n🤖 AI: {ai_response}")
#             print(f"   [Tokens: {response.usage.total_tokens}]")
            
#         except Exception as e:
#             print(f"❌ Error: {e}")
#             break
    
#     return conversation


# # ─── Run the Chatbot ───
# system = """You are a friendly Python tutor.
# Explain concepts in Roman Urdu and English.
# Always provide examples.
# Stay beginner-friendly."""

# chat_history = chat_with_ai(system)
# print(f"\n📊 Total messages: {len(chat_history) - 1}")

# 🔸 ========PART 3: Helper Function — Clean API Wrapper======
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LONGCAT_API_KEY"),
    base_url="https://api.longcat.chat/openai"
)

def ask_ai(
    question,
    system_prompt="You are a helpful assistant.",
    model="LongCat-2.0-Preview",
    temperature=0.7,
    max_tokens=1000
):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        content = response.choices[0].message.content

        return {
            "response": content,
            "tokens": response.usage.total_tokens,
            "success": True
        }

    except Exception as e:
        return {
            "response": None,
            "error": str(e),
            "success": False
        }


# Test
result = ask_ai(
    "What is python list",
    "Please learn me Python list"
)

if result["success"]:
    print(result["response"])
    print("Tokens:", result["tokens"])
else:
    print("Error:", result["error"])

"""
# ===========================================
"""
`ask_ai()` function use karke ek Q&A script banao jo:
- 5 alag alag questions puchhe AI se
- Har question ke tokens aur cost log kare
- End mein total cost print kare
Topics: Python, AI, Programming, etc."""
# ================Solution====================
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("LONGCAT_API_KEY"),
    base_url="https://api.longcat.chat/openai"
)
questions = [
    "What is the difference between a list and a tuple in Python?",
    "What does an AI Engineer do?",
    "Why do we use a virtual environment?",
    "Why do we use a virtual environment??",
    "What is JSON and why is it used?",
]
total_tokens = 0
total_cost = 0.0

print("=" * 60)
print("🤖 AI Q&A Session")
print("=" * 60)

for i, question in enumerate(questions, 1):
    print(f"\n❓ Q{i}: {question}")
    
    response = client.chat.completions.create(
        model="LongCat-2.0-Preview",
        messages=[
            {"role": "system", "content": "Reply in Short and clear — 2-3 lines mein."},
            {"role": "user", "content": question}
        ],
        max_tokens=150
    )
    
    answer = response.choices[0].message.content
    tokens = response.usage.total_tokens
    cost = tokens * 0.000002
    
    total_tokens += tokens
    total_cost += cost
    
    print(f"✅ A: {answer}")
    print(f"   📊 Tokens: {tokens} | Cost: ${cost:.6f}")

print("\n" + "=" * 60)
print(f"📊 TOTAL: {total_tokens} tokens | Cost: ${total_cost:.4f}")
print("=" * 60)