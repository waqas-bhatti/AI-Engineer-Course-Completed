# =============Mega Exercise=============
"""
Create a terminal-based app:
[1] Add Prompt
[2] View Prompt
[3] Use Prompt (Ask AI)
[4] List All Prompts
[5] Exit
Prompts should be saved in a JSON file.
When "Use Prompt" is selected, it should also ask for a question and get a real response from the AI."""
# =================Solution=====================
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv("Put the API key"),
    base_url="https://api.longcat.chat/openai"
)
PROMPTS_FILE = "my_prompts.json"

def load_prompts():
    if not os.path.exists(PROMPTS_FILE):
        return {}
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_prompts(prompts):
    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

def show_menu():
    print("\n" + "=" * 40)
    print("📚 Prompt Library")
    print("=" * 40)
    print("[1] New Add the Prompt")
    print("[2] Display Prompt")
    print("[3] User the Prompt (AI)")
    print("[4] List all prompts")
    print("[5] Exit")
    return input("\nChoice: ").strip()

def main():
    print("🚀 Prompt Library App Start!")
    
    while True:
        choice = show_menu()
        prompts = load_prompts()
        
        if choice == "1":
            name = input("Prompt naam: ").strip()
            content = input("Prompt content: ").strip()
            prompts[name] = content
            save_prompts(prompts)
            print(f"✅ '{name}' Successfully Added!")
        
        elif choice == "2":
            name = input("Which prompt do you want to view?: ").strip()
            if name in prompts:
                print(f"\n📋 {name}:\n{prompts[name]}")
            else:
                print("❌ Not Found")
        
        elif choice == "3":
            if not prompts:
                print("❌ No Any Prompt Now")
                continue
            print("Available prompts:", ", ".join(prompts.keys()))
            name = input("Where are use prompt: ").strip()
            if name not in prompts:
                print("❌ Not Found")
                continue
            question = input("Question: ").strip()
            
            print("\n⏳ Ask the AI ...")
            response = client.chat.completions.create(
                model="LongCat-2.0-Preview",
                messages=[
                    {"role": "system", "content": prompts[name]},
                    {"role": "user", "content": question}
                ],
                max_tokens=400
            )
            print(f"\n🤖 AI: {response.choices[0].message.content}")
        
        elif choice == "4":
            if not prompts:
                print("Not Any Prompt")
            else:
                print(f"\n📚 All Prompts ({len(prompts)}):")
                for name, content in prompts.items():
                    print(f"  • {name}: {content[:50]}...")
        
        elif choice == "5":
            print("👋 Bye!")
            break
        
        else:
            print("❌ Wrong Choice")

if __name__ == "__main__":
    main()
