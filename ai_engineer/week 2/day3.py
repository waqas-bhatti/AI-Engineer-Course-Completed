# ===========Streaming Responses=============
# 🔸 PART 1: Basic Streaming
# ─────────────────────────────────────────
# 1. Without Streaming (Normal — Trick use week 1)
# ─────────────────────────────────────────

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.longcat.chat/openai"
)


"""

print("🔸 WITHOUT STREAMING:")
response = client.chat.completions.create(
    model="LongCat-2.0-Preview",
    messages=[{"role": "user", "content": "Count from 1 to 10 with words in between"}],
    max_tokens=200
)
print(response.choices[0].message.content)

print("\n" + "=" * 50 + "\n")

# ─────────────────────────────────────────
# 2. With Streaming — stream=True
# ─────────────────────────────────────────

print("🔸 WITH STREAMING:")

stream = client.chat.completions.create(
    model="LongCat-2.0-Preview",
    messages=[{"role": "user", "content": "Count from 1 to 10 with words in between"}],
    max_tokens=200,
    stream=True  # THIS IS IMPORTANT
)

# Chunks come from the stream — word by word.
full_response = ""
for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:  # Sometimes empty chunks are received.
        print(content, end="", flush=True)  # flush=True = immediately print
        full_response += content

print()  # Naya line
print(f"\n✅ Total response length: {len(full_response)} characters")
"""

# 🔸 =============PART 2: Streaming Chatbot (Terminal)==================

def streaming_chat(system_prompt="AI Your Very Helpful"):
    """A streaming chatbot — the response will be displayed in real time."""
    
    conversation = [{"role": "system", "content": system_prompt}]
    
    print("🤖 Streaming Chatbot. Type 'quit' to exit.")
    print("─" * 50)
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("👋 Bye!")
            break
        
        if not user_input:
            continue
        
        conversation.append({"role": "user", "content": user_input})
        
        print("🤖 AI: ", end="", flush=True)
        
        stream = client.chat.completions.create(
            model="LongCat-2.0-Preview",
            messages=conversation,
            stream=True,
            max_tokens=500
        )
        
        full_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                full_response += content
        
        print()  # New line after response complete
        conversation.append({"role": "assistant", "content": full_response})

# Run karo
streaming_chat("You are a friendly Python tutor. Explain in Roman Urdu.")
