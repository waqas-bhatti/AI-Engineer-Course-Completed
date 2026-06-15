# ─────────────────────────────────────────
# 1. Basic Data Types 
# ─────────────────────────────────────────

# name = "waqas"
# temprature = 0.7
# max_tokens = 1000
# is_streaming = True
# print(f"Name: {type(name)}")
# print(f"Temprature: {type(temprature)}")

# ─────────────────────────────────────────
# 3. Lists — AI responses, messages arrays
# ─────────────────────────────────────────
# messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "What is the capital of France?"},
#     {"role": "assistant", "content": "The capital of France is Paris."}
# ]
# print(f"Messages: {type(messages)}")
# print(messages[0])
# print(messages[-1])
# print(len(messages))
# append the list
# messages.append({"role": "user", "content": "What is the population of Paris?"})
# print(len(messages))

# ─────────────────────────────────────────
# 4. Dictionaries — API response yahi format hoti hai
# ─────────────────────────────────────────
# response = {
#     "id": "chatcmpl-123",
#     "object": "chat.completion",
#     "created": 1677652288,
#     "choices": [
#         {
#             "index": 0,
#             "message": {
#                 "role": "assistant",
#                 "content": "The capital of France is Paris."
#             },
#             "finish_reason": "stop"
#         }
#     ],
#     "usage": {
#         "prompt_tokens": 9,
#         "completion_tokens": 12,
#         "total_tokens": 21
#     }
# }
#nested dictionary access
# content = response["choices"][0]["message"]["content"]
# total_token = response["usage"]["total_tokens"]
# print(f"Content: {content}")
# print(f"Total Tokens: {total_token}")

#.get safe way to access dictionary keys
# model = response.get("model", "unknown")
# print(f"Model: {model}")

# ─────────────────────────────────────────
# 5. For Loop — Messages process karne ke liye
# ─────────────────────────────────────────
# messages = [
#     {"role": "user", "content": "Hello"},
#     {"role": "assistant", "content": "Hi!"},
#     {"role": "user", "content": "Python?"},
# ]

# for message in messages:
#       role = message["role"]
#       content = message["content"]
#       print(f"{role.capitalize()}: {content}")

# ─────────────────────────────────────────
# 5. While Loop — Chatbot loop ke liye
# ─────────────────────────────────────────

# This pattern AI chatbot For Use
# print("\n--- Simple Chat Loop Demo ---")
# conversation_history = []
# count = 0
# while count < 3:  # Limit to 3 interactions for demo
#     user_input = input("You: ")

#     if user_input.lower() in ["exit", "quit", "bye"]:
#         print("Bye!")
#         break
#     conversation_history.append({"role": "user", 
#                                  "content": user_input})
    
    # Simulate assistant response (replace with actual API call)
#     assistant_response = f"Echo: {user_input}"
#     conversation_history.append({"role": "assistant", "content": assistant_response})
    
#     print(f"Assistant: {assistant_response}")
#     count += 1
#     print(f"\nTotal messages: {len(conversation_history)}")

# ─────────────────────────────────────────
# 7. If/Elif/Else — Content filtering ke liye
# ─────────────────────────────────────────

# def check_content(text):
#       banned_words = ["harm", "danger", "violence"]
#       text_lower = text.lower()

#       for word in banned_words:
#             if word in text_lower:
#                   return "BLOCKED", f"Banned word found: {word}"
            
#       if len(text) > 3:
#             return "BLOCKED", "Content too long"
#       elif len(text) > 10:
#             return "TOO_LONG", "Input are very long, please shorten it"
#       else:
#             return "OK", "Content is acceptable"

# # Test the function'
# test_text = ["Hello!", "Hi", "x" * 1001, "How are you"]  
# for text in test_text:
#       status, msg = check_content(text)
#       print(f"Input: {text}\nStatus: {status}, Message: {msg} \n")

                         # ─────────────────────
                         # 🤖 Exercise with solution
                         # ─────────────────────
# messages = [
#     {"role": "user", "content": "Hello"}, 
#     {"role": "assistant", "content": "Hi! How can I help you?"},
#     {"role": "user", "content": "Python?"},     
#     {"role": "assistant", "content": "Python is a programming language."},
#     {"role": "user", "content": "What is AI?"}                                                                                   ]
# print("-" * 50)
# for msg in messages:
#       if msg["role"] == "user":
#             print(f"User: {msg['content']}")
#       elif msg["role"] == "assistant":
#             print(f"Assistant: {msg['content']}") 
#       else:
#             print(f"Unknown role: {msg['role']} with content: {msg['content']}")        
#             print("─" * 40)     

# -------------Exercise 1.2 — Token Counter (Simple)----------
# def count_tokens(text):
#       token_count = len(text) // 5
#       # return len(text.split())
#       print(f"Text: '{text[:50]}'")
#       print(f"Characters: {len(text)}")
#       print(f"Estimated tokens: ~{token_count}")

#       if token_count > 100:
#             print("Warning: Input may exceed token limits for some models.")  
#             return token_count
# # Test the function
# count_tokens("Hello world")
# count_tokens("Python are useful language thats use it in AI")
# count_tokens("x" * 500)

# =============exercise 3 solution============
response = {
    "choices": [
        {"message": {"role": "assistant", "content": "AI means Artificial Intelligence."}},
    ],
    "usage": {"prompt_tokens": 15, "completion_tokens": 10, "total_tokens": 25},
    "model": "gpt-4o-mini"
}
content = response["choices"][0]["message"]["content"]      
total_tokens = response["usage"]["total_tokens"]
prompt_tokens = response["usage"]["prompt_tokens"]
completion_tokens = response["usage"]["completion_tokens"]

cost = total_tokens * 0.0002
print("=" * 40)
print("📊 API Response Summary")
print("=" * 40)
print(f"🤖 Response: {content}")
print(f"📈 Model: {response['model']}")
print(f"🔢 Prompt Tokens: {prompt_tokens}")
print(f"🔢 Completion Tokens: {completion_tokens}")
print(f"🔢 Total Tokens: {total_tokens}")
print(f"💰 Cost: ${cost:.6f}")
print("=" * 40)

