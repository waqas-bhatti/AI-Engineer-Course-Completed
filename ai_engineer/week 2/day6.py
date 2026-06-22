# ================Token Management=========
# 🔸 ========= Token Management Strategies ============
# ─────────────────────────────────────────
# 1. Context Window Manager — Production Pattern
# ─────────────────────────────────────────

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY")
)


# class ContextWindowManager:
#     """
#     Keeps conversation inside the model context window.
#     Removes older messages when token limit is exceeded.
#     """

#     MODEL_LIMITS = {
#         "google/gemma-4-31b-it:free": 128_000,
#         "google/gemma-4-26b-a4b-it:free": 128_000,
#     }

#     def __init__(
#         self,
#         model="google/gemma-4-31b-it:free",
#         reserve_for_response=2000
#     ):
#         self.model = model

#         # OpenRouter models may not exist in tiktoken mappings
#         try:
#             self.encoding = tiktoken.encoding_for_model(model)
#         except KeyError:
#             print(
#                 f"⚠️ Tokenizer mapping not found for '{model}'. "
#                 f"Using cl100k_base fallback."
#             )
#             self.encoding = tiktoken.get_encoding("cl100k_base")

#         self.max_tokens = self.MODEL_LIMITS.get(model, 16000)
#         self.reserve = reserve_for_response

#     def count_tokens(self, text):
#         return len(self.encoding.encode(str(text)))

#     def count_messages_tokens(self, messages):
#         total = 0

#         for msg in messages:
#             total += self.count_tokens(msg["content"])

#             # Approximate chat formatting overhead
#             total += 4

#         return total

#     def fit_to_window(self, messages):
#         """
#         Keeps system message(s).
#         Removes oldest messages if context exceeds budget.
#         """

#         available_budget = self.max_tokens - self.reserve

#         system_msgs = [
#             m for m in messages
#             if m["role"] == "system"
#         ]

#         other_msgs = [
#             m for m in messages
#             if m["role"] != "system"
#         ]

#         system_tokens = self.count_messages_tokens(system_msgs)

#         budget_left = available_budget - system_tokens

#         kept_messages = []
#         current_tokens = 0

#         # Start from newest messages
#         for msg in reversed(other_msgs):

#             msg_tokens = (
#                 self.count_tokens(msg["content"])
#                 + 4
#             )

#             if current_tokens + msg_tokens <= budget_left:
#                 kept_messages.insert(0, msg)
#                 current_tokens += msg_tokens
#             else:
#                 break

#         removed_count = len(other_msgs) - len(kept_messages)

#         if removed_count > 0:
#             print(
#                 f"⚠️ Removed {removed_count} old messages "
#                 f"to fit context window."
#             )

#         return system_msgs + kept_messages


# # ---------------------------
# # TESTING
# # ---------------------------

# manager = ContextWindowManager(
#     model="google/gemma-4-31b-it:free",
#     reserve_for_response=500
# )

# long_conversation = [
#     {
#         "role": "system",
#         "content": "You are a helpful AI assistant."
#     }
# ]

# for i in range(50):
#     long_conversation.append(
#         {
#             "role": "user",
#             "content":
#                 f"This is user message number {i}. "
#                 f"I am intentionally writing a long text "
#                 f"to increase token usage and test "
#                 f"context trimming behavior."
#         }
#     )

#     long_conversation.append(
#         {
#             "role": "assistant",
#             "content":
#                 f"I have received and understood "
#                 f"message number {i}."
#         }
#     )

# print("\n=== BEFORE TRIMMING ===")
# print("Messages:", len(long_conversation))
# print(
#     "Tokens:",
#     manager.count_messages_tokens(long_conversation)
# )

# trimmed = manager.fit_to_window(long_conversation)

# print("\n=== AFTER TRIMMING ===")
# print("Messages:", len(trimmed))
# print(
#     "Tokens:",
#     manager.count_messages_tokens(trimmed)
# )

# print("\n=== KEPT MESSAGES ===")
# for msg in trimmed[-5:]:
#     print(msg["role"], ":", msg["content"][:60])

# ==================Exercise===============
"""
Craete an Chatbot:
- Use the BudgetTracker 
- Every Response display current spend amount
- To automatically switch from gpt-4o to gpt-4o-mini once 80% of your budget is exhausted, you need to implement application-level tracking
- If cross the 100%, They can display stop the user
"""

class CostAwareChatbot:
    PRICING = {"google/gemma-4-31b-it:free": {"input": 0.15, "output": 0.60}, "google/gemma-4-26b-a4b-it:free": {"input": 2.50, "output": 10.00}}
    
    def __init__(self, budget_usd=1.0):
        self.budget = budget_usd
        self.spend = 0.0
        self.current_model = "google/gemma-4-31b-it:free"
        self.conversation = [{"role": "system", "content": "Scope Of AI Engineer in Future"}]
    
    def chat(self, user_message):
        # Budget check pehle
        percent_used = (self.spend / self.budget) * 100
        
        if percent_used >= 100:
            return "❌ Budget has run out! Set a new budget.”"
        
        if percent_used >= 80 and self.current_model == "google/gemma-4-31b-it:free":
            print("⚠️ 80% of the budget has been used, so we're switching to google/gemma-4-26b-a4b-it:free.")
            self.current_model = "google/gemma-4-26b-a4b-it:free"
        
        self.conversation.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model=self.current_model,
            messages=self.conversation,
            max_tokens=300
        )
        
        ai_response = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": ai_response})
        
        # Cost calculate 
        p = self.PRICING[self.current_model]
        cost = (response.usage.prompt_tokens / 1_000_000) * p["input"] + \
               (response.usage.completion_tokens / 1_000_000) * p["output"]
        self.spend += cost
        
        print(f"💰 Spend so far: ${self.spend:.6f} / ${self.budget} ({(self.spend/self.budget)*100:.1f}%)")
        
        return ai_response

# Test
bot = CostAwareChatbot(budget_usd=0.01)  # Test Small budget
print(bot.chat("Scope of AI Engineer in Future"))
print(bot.chat("Tell me more about it."))



