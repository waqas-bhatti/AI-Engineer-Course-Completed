# ============File I/O + JSON Handling=======
import json
import os
from pathlib import Path

# ─────────────────────────────────────────
# 1. Text File — Prompts save/load 
# ─────────────────────────────────────────

#Save the Prompt to a text file
"""
system_prompt = "You are a helpful assistant that provides concise answers."

with open("system_prompt.txt", "w", encoding="utf-8") as file:
    file.write(system_prompt)
    print("Save the Prompt")

#Load the Prompt from the text file
with open("system_prompt.txt", "r", encoding="utf-8") as file:
    loaded_prompt = file.read()
    print(f"Loaded Prompt: {loaded_prompt} (Length: {len(loaded_prompt)})") """

# Conversation history Save in JSON format
"""
conversation_history = [
    {"role": "user", "content": "Hello!"},      
      {"role": "assistant", "content": "Hi there! How can I assist you today?"},
      {"role": "user", "content": "Can you tell me a joke?"},
      {"role": "assistant", "content": "Why don't scientists trust atoms? Because they make up everything!"}
]

with open("conversation_history.json", "w", encoding="utf-8") as file:
    json.dump(conversation_history, file, indent = 2, ensure_ascii=False)
    print("\nConversation history saved to conversation_history.json")
    print("\nConversation history saved to conversation_history.json")

# Load the conversation history from the JSON file
with open("conversation_history.json", "r", encoding="utf-8") as file:
    loaded_history = json.load(file)
    print(f"\nLoaded Conversation History: {loaded_history} (Length: {len(loaded_history)})")
    print(f"\nLoaded Conversation History: {loaded_history} (Length: {len(loaded_history)})")
   """

   # ─────────────────────────────────────────
# 4. Config File — API settings store 
# ─────────────────────────────────────────

#config file save 
"""
config = {
      "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
    "system_prompt": "Tum helpful AI ho",
    "conversation_history": []
}

def save_config(config, filename="config.json"):
    with open(filename, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Config saved to {filename}")

def load_config(filename="config.json"):
    if not os.path.exists(filename):
        print(f"❌ Config Not Found: {filename}")
        return None
    with open(filename, "r") as f:
        return json.load(f)

save_config(config)
loaded_config = load_config()
print(f"Model: {loaded_config['model']}")
"""
# ===============🔸 PART 2: Environment Variables (.env) ===========

# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load environment variables from .env file
# api_key = os.getenv("OPENAI_API_KEY")
# if api_key:
#     print(f"✅ API Key Loaded Successfully: {api_key[:10]}...")  # Print first 10 chars for verification
# else:
#     print("❌ API Key Not Found. Please check your .env file.")

# # Multiple env variables
# def load_ai_config():
#     """All config env variables loaded"""
#     return {
#         "api_key": os.getenv("OPENAI_API_KEY", ""),
#         "model": os.getenv("AI_MODEL", "gpt-4o-mini"),       # default value
#         "temperature": float(os.getenv("TEMPERATURE", "0.7")),
#         "max_tokens": int(os.getenv("MAX_TOKENS", "1000")),
#     }

# config = load_ai_config()
# print("Config loaded:", {k: v if k != "api_key" else "***" for k, v in config.items()})    

# ====================Exercises====================
"""
One "prompt library" Create in JSON file:
{
  "coding_assistant": "...",
  "customer_support": "...",
  "urdu_teacher": "..."
}

Functions:
- save_prompts(prompts_dict) — save 
- get_prompt(name) — specific prompt 
- list_prompts() — All prompt names print
- add_prompt(name, content) — new prompt add 
"""
# ===========================================
import json
import os

PROMPTS_FILE = "prompts.json"

def save_prompts(prompts_dict):
    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts_dict, f, indent=2, ensure_ascii=False)
    print("✅ Prompts saved!")

def get_prompt(name):
    if not os.path.exists(PROMPTS_FILE):
        print("❌ No prompts file found")
        return None
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)
    return prompts.get(name, None)

def list_prompts():
    if not os.path.exists(PROMPTS_FILE):
        print("❌ No prompts file found")
        return
    with open(PROMPTS_FILE, "r") as f:
        prompts = json.load(f)
    print(f"\n📚 Available Prompts ({len(prompts)}):")
    for name in prompts:
        print(f"  • {name}")

def add_prompt(name, content):
    prompts = {}
    if os.path.exists(PROMPTS_FILE):
        with open(PROMPTS_FILE, "r") as f:
            prompts = json.load(f)
    prompts[name] = content
    save_prompts(prompts)
    print(f"✅ Prompt '{name}' added!")

# ─── Use karo ───
initial_prompts = {
    "coding_assistant": "You are a coding expert. Always write clean code with comments.",
    "customer_support": "You are a customer support agent. Be polite and helpful.",
    "urdu_teacher": "You are an Urdu teacher. Explain in simple Urdu.",
}

save_prompts(initial_prompts)
list_prompts()

print("\nCoding prompt:", get_prompt("coding_assistant"))

add_prompt("data_analyst", "You are a data analyst. Explain numbers and trends.")
list_prompts()