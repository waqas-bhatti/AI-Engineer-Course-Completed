# 🔸 =============PART 1: Models ka Comparison Chart=================

# ─────────────────────────────────────────
# Smart Model Selector — Choose the model according to the task
# ─────────────────────────────────────────

"""
# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()
# client = OpenAI(api_key=os.getenv("API_KEY"))

# class ModelSelector:
    
    
#     SIMPLE_TASKS = ["translate", "summarize", "classify", "extract"]
#     COMPLEX_TASKS = ["analyze", "reason", "code_review", "complex_math"]
    
#     @staticmethod
#     def select_model(task_type, budget_conscious=True):
#         """
#         Args:
#             task_type: task ka type (string)
#             budget_conscious: True = Prefer the fastest model.
#         """
#         if budget_conscious:
#             return "gpt-4o"  # 95% This is sufficient for most cases.
        
#         if task_type in ModelSelector.COMPLEX_TASKS:
#             return "LongCat-2.0-Preview"
        
#         return "gpt-4o"
    
#     @staticmethod
#     def explain_choice(task_type):
#         model = ModelSelector.select_model(task_type, budget_conscious=False)
#         reasons = {
#             "gpt-4o": "It is a simple task, so the mini model will be fast and cheaper.",
#             "LongCat-2.0-Preview": "Complex reasoning is required for better accuracy. Longcat"
#         }
#         return model, reasons[model]


# # Test
# for task in ["summarize", "code_review", "translate", "complex_math"]:
#     model, reason = ModelSelector.explain_choice(task)
#     print(f"Task: {task:15} → Model: {model:15} | Reason: {reason}")
#     =================Exercise==============
"""
Create a function route_task(user_query) that decides which model to use based on the query:

If the query contains "explain", "analyze", or "why" → use gpt-4o
If the query contains "translate", "summarize", or "list" → use gpt-4o-mini
Default → use gpt-4o-mini

Then make the actual API call using the selected model and display the result along with the model name.
"""
# =========================Solution============
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def route_task(user_query):
    complex_keywords = ["explain", "analyze", "why", "compare", "reason"]
    simple_keywords = ["translate", "summarize", "list", "extract"]
    
    query_lower = user_query.lower()
    
    if any(kw in query_lower for kw in complex_keywords):
        model = "gpt-4o"
    elif any(kw in query_lower for kw in simple_keywords):
        model = "gpt-4o-mini"
    else:
        model = "gpt-4o-mini"  # default
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_query}],
        max_tokens=300
    )
    
    return response.choices[0].message.content, model

# Test
queries = [
    "Explain why recursion works",
    "Summarize this: Python is great",
    "What's the weather like",
]

for q in queries:
    response, model = route_task(q)
    print(f"Query: {q}")
    print(f"Model: {model}")
    print(f"Response: {response[:100]}...")
    print("-" * 40)
    """