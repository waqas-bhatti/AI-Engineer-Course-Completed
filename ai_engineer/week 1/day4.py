# =========OOP Basics for AI============
# 🔸 Classes — Structure of AI Apps

# import json
# import os
# from datetime import datetime

# # ─────────────────────────────────────────
# # 1. Simple Class — Basic ChatBot
# # ─────────────────────────────────────────

# class SimpleChatBot:
#     """
#     A basic chatbot class.
#     In Week 2, we will add the real OpenAI API to it.
#     """
#     def __init__(self, name, system_prompt):
#         """
#         Constructor — It works when the chatbot is built
        
#         Args:
#             name: The Name of Bot
#             system_prompt: Bot personality/instructions
#         """
#         self.name = name
#         self.system_prompt = system_prompt
#         self.conversation_history = [
#             {"role": "system", "content": system_prompt}
#         ]
#         self.created_at = datetime.now().isoformat()
#         print(f"✅ ChatBot '{self.name}' created with system prompt: '{self.system_prompt}'")

#     def add_user_message(self, message):
#         """"Add the user's message to the chat history."""
#         self.conversation_history.append({
#             "role": "user",
#             "content": message
#         })
    
#     def add_ai_response(self, response):
#         """Add the AI's response to the chat history."""
#         self.conversation_history.append({
#             "role": "assistant",
#             "content": response
#         })
    
#     def get_history(self):
#         """Conversation history return """
#         return self.conversation_history
    
#     def clear_history(self):
#         """Clear the chat history, but keep the system prompt."""
#         self.conversation_history = [
#             {"role": "system", "content": self.system_prompt}
#         ]
#         print("✅ History cleared!")
    
#     def save_history(self, filename=None):
#         """Save the conversation to disk."""
#         if not filename:
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"chat_{self.name}_{timestamp}.json"
        
#         with open(filename, "w", encoding="utf-8") as f:
#             json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
#         print(f"✅ Saved to {filename}")
    
#     def get_message_count(self):
#         """Return the count of messages, excluding the system message."""
#         return len(self.conversation_history) - 1
    
#     def __repr__(self):
#         """Return a string representation of the ChatBot object."""
#         return f"ChatBot(name={self.name}, messages={self.get_message_count()})"   
        
# # ─── Use This ───
# bot = SimpleChatBot(
#     name="Aria",
#     system_prompt="You are a helpful Python tutor. Explain things in simple Urdu/English."
# )

# print(bot)  # ChatBot(name=Aria, messages=0)

# # Messages add 
# bot.add_user_message("What is python?")
# bot.add_ai_response("Python is a high-level programming language that is famous for its easy-to-read syntax.")
# bot.add_user_message("What is its use?")
# bot.add_ai_response("Python is used in AI, web development, data science, and automation.")

# print(bot)  # ChatBot(name=Aria, messages=4)
# print(f"\nTotal messages: {bot.get_message_count()}")

# # History Display
# for msg in bot.get_history():
#     if msg["role"] != "system":
#         print(f"[{msg['role']}]: {msg['content'][:50]}")

# bot.save_history()            

# ─────────────────────────────────────────
# 2. Inheritance — Specialized Bot banana
# ─────────────────────────────────────────


# class CodingAssistant(SimpleChatBot):
#     """
#     A specialized version of SimpleChatBot designed exclusively for coding.
# Inheritance: It inherits all the features and functionality of the parent class.
#     """
    
#     def __init__(self, language="Python"):
#         # Parent class ka __init__ call karo
#         super().__init__(
#             name=f"{language}Expert",
#             system_prompt=f"""Your {language} expert Now.
# You always provide working code examples, explain bugs clearly, and follow best practices."""
#         )
#         self.language = language
#         self.code_snippets = []  # Extra attribute
    
#     def save_code_snippet(self, title, code):
#         """Saving code snippets — it wasn't present in the parent class."""
#         self.code_snippets.append({
#             "title": title,
#             "code": code,
#             "timestamp": datetime.now().isoformat()
#         })
#         print(f"✅ Code snippet saved: {title}")
    
#     def list_snippets(self):
#         """Saved snippets Dsiplay"""
#         if not self.code_snippets:
#             print("No any snippet Remeaning Now")
#             return
#         print(f"\n📁 Saved Snippets ({len(self.code_snippets)}):")
#         for i, s in enumerate(self.code_snippets, 1):
#             print(f"  {i}. {s['title']}")


# # ─── Use this ───
# py_bot = CodingAssistant("Python")
# py_bot.add_user_message("Display the List comprehension")
# py_bot.add_ai_response("squares = [x**2 for x in range(10)]")
# py_bot.save_code_snippet("List Comprehension Example", "squares = [x**2 for x in range(10)]")
# py_bot.list_snippets()
# print(py_bot)

# ─────────────────────────────────────────
# 3. Class Methods And Static Methods
# ─────────────────────────────────────────

# class TokenManager:
#     """Tokens count how to manage """
    
#     PRICE_PER_TOKEN = {
#         "gpt-4o-mini": 0.000004,
#         "gpt-4o": 0.00003,
#         "gpt-3.5-turbo": 0.000001,
#     }
    
#     @staticmethod
#     def count_tokens(text):
#         """Text count the tokens (approximate)"""
#         return max(1, len(text) // 4)
    
#     @staticmethod
#     def count_messages_tokens(messages):
#         """Count tokens for a list of messages"""
#         total = 0
#         for msg in messages:
#             total += TokenManager.count_tokens(msg.get("content", ""))
#             total += 4  # Per message overhead
#         return total
    
#     @classmethod
#     def calculate_cost(cls, tokens, model="gpt-4o-mini"):
#         """Cost calculate them"""
#         price = cls.PRICE_PER_TOKEN.get(model, 0.000002)
#         return tokens * price
    
#     @classmethod
#     def get_cheapest_model(cls):
#         """Told the cheapest model"""
#         return min(cls.PRICE_PER_TOKEN, key=cls.PRICE_PER_TOKEN.get)


# # ─── Use This ───
# tokens = TokenManager.count_tokens("Python is an amazing language for AI development!")
# print(f"Tokens: {tokens}")

# cost = TokenManager.calculate_cost(1000, "gpt-4o")
# print(f"1000 tokens (gpt-4o) cost: ${cost:.4f}")

# cheapest = TokenManager.get_cheapest_model()
# print(f"Cheapest model: {cheapest}")

# ===========================================
"""Create a PromptManager class that:

Stores a prompts dictionary as an instance variable.
Has an add(name, content) method to add a new prompt.
Has a get(name) method to return a prompt (returns None if not found).
Has a delete(name) method to remove a prompt.
Has a save_to_file(filename) method to save prompts in JSON format.
Has a load_from_file(filename) method to load prompts from a JSON file.
Has a list_all() method to display all prompts."""
# ======================Solution========================
# import json
# import os
# class PromptManager:
#     def __init__(self):
#         self.prompts = {}
    
#     def add(self, name, content):
#         self.prompts[name] = content
#         print(f"✅ Prompt '{name}' added")
    
#     def get(self, name):
#         prompt = self.prompts.get(name)
#         if not prompt:
#             print(f"❌ Prompt '{name}' nahi mila")
#         return prompt
    
#     def delete(self, name):
#         if name in self.prompts:
#             del self.prompts[name]
#             print(f"✅ Prompt '{name}' deleted")
#         else:
#             print(f"❌ Prompt '{name}' Not Found")
    
#     def save_to_file(self, filename="prompts.json"):
#         with open(filename, "w", encoding="utf-8") as f:
#             json.dump(self.prompts, f, indent=2, ensure_ascii=False)
#         print(f"✅ Saved to {filename}")
    
#     def load_from_file(self, filename="prompts.json"):
#         if not os.path.exists(filename):
#             print(f"❌ File No found: {filename}")
#             return
#         with open(filename, "r", encoding="utf-8") as f:
#             self.prompts = json.load(f)
#         print(f"✅ Loaded {len(self.prompts)} prompts")
    
#     def list_all(self):
#         if not self.prompts:
#             print("❌ No prompts available")
#             return
#         print(f"\n📚 Prompts ({len(self.prompts)}):")
#         for name, content in self.prompts.items():
#             print(f"  • {name}: {content[:50]}...")

# # ─── Use This ───
# pm = PromptManager()
# pm.add("coding", "Your coding expert")
# pm.add("support", "Your support agent")
# pm.list_all()
# pm.save_to_file()

# pm2 = PromptManager()
# pm2.load_from_file()
# pm2.list_all()
# print(pm2.get("coding"))

# ==============Exercise No 2====================
"""Create a ConversationSession class that:

Automatically generates a session_id based on the current timestamp.
Tracks messages within the session.
Tracks token usage.
Has an is_expired() method that returns True if the session is older than 1 hour.
Has a to_dict() method that converts the entire session into a dictionary.
Implements __len__ to return the total number of messages in the session."""
# ========================Solution================
from datetime import datetime

class ConversationSession:
    def __init__(self, system_prompt="You are helpful"):
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.messages = [{"role": "system", "content": system_prompt}]
        self.created_at = datetime.now()
        self.total_tokens = 0
        print(f"✅ Session created: {self.session_id}")
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        tokens = len(content) // 4
        self.total_tokens += tokens
    
    def is_expired(self, hours=1):
        elapsed = (datetime.now() - self.created_at).seconds / 3600
        return elapsed > hours
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "messages": self.messages,
            "total_tokens": self.total_tokens,
            "is_expired": self.is_expired()
        }
    
    def __len__(self):
        return len(self.messages) - 1  # system message minus

# ─── Use This ───
session = ConversationSession("Are You helpful")
session.add_message("user", "Hello!")
session.add_message("assistant", "Hi! How can I assist you today?")
session.add_message("user", "learn the Python programming language.")

print(f"Messages: {len(session)}")
print(f"Tokens used: {session.total_tokens}")
print(f"Expired: {session.is_expired()}")
print(f"Session dict keys: {list(session.to_dict().keys())}")