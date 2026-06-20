# ─────────────────────────────────────────
# 1. Real Token Counting (Approximate not — exact)
# ─────────────────────────────────────────
import tiktoken
# def count_real_tokens(text, model="LongCat-2.0-Preview"):
#     """Accurate token count using Tiktoken"""
#     try:
#         encoding = tiktoken.encoding_for_model(model)
#     except KeyError:
#         encoding = tiktoken.get_encoding("cl100k_base")  # fallback
    
#     tokens = encoding.encode(text)
#     return len(tokens)

# # Test karo
# texts = [
#     "Hello",
#     "Hello world",
#     "Python is a great programming language for AI development",
#     "پاکستان ایک خوبصورت ملک ہے",  # Urdu text
# ]

# for text in texts:
#     real_count = count_real_tokens(text)
#     approx_count = len(text) // 4  # Hamara purana rough method
#     print(f"Text: '{text}'")
#     print(f"  Real tokens: {real_count} | Approx (len/4): {approx_count}")
#     print()


# ─────────────────────────────────────────
# 2. Look at the tokens to understand what gets tokenized.
# ─────────────────────────────────────────
"""
def show_tokens(text, model="LongCat-2.0-Preview"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"Unknown model: {model}")
        print("Using cl100k_base tokenizer...\n")
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens = encoding.encode(text)

    print(f"Text: '{text}'")
    print(f"Token count: {len(tokens)}")

    for token in tokens:
        print(f"{token} -> {encoding.decode([token])}")

show_tokens("AI Engineering is exciting!") 
"""
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# =========================
# CONFIG
# =========================

LONGCAT_DAILY_QUOTA = 5_000_000

MODEL_PRICING = {
    "gpt-4o-mini": {
        "input": 0.15,
        "output": 0.60,
        "type": "paid"
    },
    "gpt-4o": {
        "input": 2.50,
        "output": 10.00,
        "type": "paid"
    },
    "LongCat-2.0-Preview": {
        "input": 0.0,
        "output": 0.0,
        "type": "quota"
    }
}


# =========================
# TOKEN / COST TRACKER
# =========================

class TokenTracker:

    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def add_usage(self, prompt_tokens, completion_tokens):
        self.total_input_tokens += prompt_tokens
        self.total_output_tokens += completion_tokens

    @property
    def total_tokens(self):
        return self.total_input_tokens + self.total_output_tokens

    def calculate_cost(self, model):
        pricing = MODEL_PRICING.get(model)

        if not pricing:
            raise ValueError(f"Unknown model: {model}")

        input_cost = (
            self.total_input_tokens / 1_000_000
        ) * pricing["input"]

        output_cost = (
            self.total_output_tokens / 1_000_000
        ) * pricing["output"]

        total_cost = input_cost + output_cost

        return {
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6)
        }

    def longcat_quota_status(self):
        used = self.total_tokens
        remaining = max(0, LONGCAT_DAILY_QUOTA - used)

        return {
            "used_tokens": used,
            "remaining_tokens": remaining,
            "used_percent": round(
                (used / LONGCAT_DAILY_QUOTA) * 100,
                4
            )
        }


# =========================
# LONGCAT CLIENT
# =========================

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.longcat.chat/openai"
)

tracker = TokenTracker()


def ask_longcat(question):

    response = client.chat.completions.create(
        model="LongCat-2.0-Preview",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )

    usage = response.usage

    tracker.add_usage(
        usage.prompt_tokens,
        usage.completion_tokens
    )

    print("\n===== RESPONSE =====")
    print(response.choices[0].message.content)

    print("\n===== TOKEN USAGE =====")
    print(f"Prompt Tokens     : {usage.prompt_tokens}")
    print(f"Completion Tokens : {usage.completion_tokens}")
    print(f"Total Tokens      : {usage.total_tokens}")

    quota = tracker.longcat_quota_status()

    print("\n===== LONGCAT QUOTA =====")
    print(f"Used Tokens       : {quota['used_tokens']:,}")
    print(f"Remaining Tokens  : {quota['remaining_tokens']:,}")
    print(f"Used Percentage   : {quota['used_percent']}%")

    return response


# =========================
# TEST
# =========================

ask_longcat(
    "Explain Python decorators in simple words."
)
"""
# ====================Exercise==================
"""
Create a function estimate_conversation_cost(messages, model) that:

Counts the tokens for the entire conversation (a list of messages) using tiktoken
Estimates the output tokens (assume: output tokens = 50% of input tokens)
Calculates the total cost
Returns a dictionary in the following format:
"""
# =======================Solution=================

import tiktoken

MODEL_PRICING = {
    "LongCat-2.0-Preview": {
        "input": 0.0,
        "output": 0.0
    }
}

def estimate_conversation_cost(messages, model="LongCat-2.0-Preview"):

    # LongCat fallback tokenizer
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    input_tokens = 0

    for msg in messages:
        input_tokens += len(
            encoding.encode(msg["content"])
        )
        input_tokens += 4

    estimated_output_tokens = int(input_tokens * 0.5)

    pricing = MODEL_PRICING.get(model)

    input_cost = (
        input_tokens / 1_000_000
    ) * pricing["input"]

    output_cost = (
        estimated_output_tokens / 1_000_000
    ) * pricing["output"]

    return {
        "input_tokens": input_tokens,
        "estimated_output_tokens": estimated_output_tokens,
        "total_cost": round(
            input_cost + output_cost,
            6
        )
    }

messages = [
    {
        "role": "system",
        "content": "Tum helpful Python tutor ho"
    },
    {
        "role": "user",
        "content": "What are decorators in Python? Explain them in detail with examples."
    }
]

result = estimate_conversation_cost(messages)
print(result)