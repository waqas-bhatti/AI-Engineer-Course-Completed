# ─────────────────────────────────────────
# 1. Basic Function — Create Prompt 
# ─────────────────────────────────────────

# def create_prompt(user_message, language="English"):
#     """
#     Create a prompt for the AI model based on the user's message and desired language.

#     Parameters:
#     user_message (str): The message from the user.
#     language (str): The language in which the response should be generated. Default is "English".

#     Returns:
#     str: A formatted prompt for the AI model.
#     """
#     prompt = f"Please respond to the following message in {language}:\n\n{user_message}"
#     return prompt.strip()
# print(create_prompt("What is the capital of France?", "French"))
# print(create_prompt("What is the capital of France?","English"))

# ─────────────────────────────────────────
# 2. *args — Multiple messages accept 
# ─────────────────────────────────────────

# def build_conversation(*messages):
#     """
#     Build a conversation history from multiple messages.

#     Parameters:
#     *messages (str): A variable number of messages to be included in the conversation history.

#     Returns:
#     str: A formatted conversation history.
#     """
#     conversation = []
#     for i, message in enumerate(messages):
#         role = "User" if i % 2 == 0 else "Assistant"
#         conversation.append({"role": role, "content": message})
#     return conversation
# chat = build_conversation("Hello!", 
#                           "Hi there! How can I assist you today?", 
#                           "Can you tell me a joke?", 
#                           "Sure! Why don't scientists trust atoms? Because they make up everything!")
# for message in chat:
#     print(f"{message['role']}: {message['content']}")

# ─────────────────────────────────────────
# 3. **kwargs — API call parameters
# ─────────────────────────────────────────

# def call_api(prompt, **kwargs):
#     """
#     Call the API with the given prompt and additional parameters.

#     Parameters:
#     prompt (str): The prompt for the API.
#     **kwargs: Additional parameters for the API call.

#     Returns:
#     dict: The response from the API.
#     """
#     config = {
#         "model": "gpt-3.5-turbo",
#         "temperature": 0.7,
#         "max_tokens": 150
#     }
#     config.update(kwargs)
#     print(f"Prompt: {prompt[:50]}...")
#     print(f"Config: {config}")
#     return {"prompt": prompt, "parameters": config}

# call_api("What is Python?")
# call_api("What is Python?", temperature=0.2, max_tokens=500)
# call_api("What is Python?", model="gpt-4o", temperature=1.0)

# ─────────────────────────────────────────
# 4. Lambda Functions — Quick transformations
# ─────────────────────────────────────────
# Token cost calculate karna
# calculate_cost = lambda tokens, price_per_token=0.000002: tokens * price_per_token

# print(calculate_cost(100))       # 0.0002
# print(calculate_cost(5000))      # 0.01
# print(calculate_cost(1000, 0.00003))  # GPT-4 pricing

# # Text clean karna
# clean_text = lambda text: text.strip().lower().replace("\n", " ")

# messy_text = "  Hello World\nThis is AI  "
# print(clean_text(messy_text))

# ─────────────────────────────────────────
# 5. Error Handling — API calls
# ─────────────────────────────────────────

# def safe_get_response(api_response):
#     """
#     Safely get a response from the API, handling potential errors.

#     Parameters:
#     api_response (dict): The response from the API.

#     Returns:
#     str: The response from the API or an error message.
#     """
#     try:
#         # Simulate API call
#         content = api_response["choices"][0]["message"]["content"]
#         return content
#     except (KeyError, IndexError) as e:
#         print(f"❌ Response parse error: {e}")
#         return None
#     except Exception as e:
#         print(f"❌ Unexpected error: {e}")
#         return None
    
#  # Test Api response
# good_response = {"choices": [{"message": {"content": "The capital of France is Paris."}}]}
# bad_response = {"choices": [{"message": {}}]}  # Missing content
# empty_response = {}  # Missing choices
# print(safe_get_response(good_response))  # Should print the content
# print(safe_get_response(bad_response))   # Should print an error message                              
# print(safe_get_response(empty_response)) # Should print an error message

# ─────────────────────────────────────────
# 6. List Comprehension — Messages filter 
# ─────────────────────────────────────────

# messages = [
#     {"role": "user", "content": "Hello!"},      
#     {"role": "assistant", "content": "Hi there! How can I assist you today?"},      
#     {"role": "user", "content": "Can you tell me a joke?"},      
#     {"role": "assistant", "content": "Sure! Why don't scientists trust atoms? Because they make up everything!"}
# ]

# # only find the user messages
# user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
# print(user_messages)  # ['Hello!', 'Can you tell me a joke?']
# # find the assistant messages
# assistant_messages = [msg["content"] for msg in messages if msg["role"] == "assistant"]
# print(assistant_messages)  # ['Hi there! How can I assist you today?', "

# # only find the content
# all_contents = [msg["content"] for msg in messages]
# print(all_contents)  # ['Hello!', 'Hi there! How can I assist you today

# # long messages filter
# long_messages = [msg["content"] for msg in messages if len(msg["content"]) > 30]
# print(long_messages)  # ['Hi there! How can I assist you today?', 'Sure

# ─────────────────────────────────────────
# 7. Dict Comprehension — Data transform karna
# ─────────────────────────────────────────

# Model prices dict banana
# models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
# prices = [0.000002, 0.00003, 0.000001]

# model_pricing = {model: price for model, price in zip(models, prices)}
# print("Model Pricing:", model_pricing)

# # Token counts ke liye dict banana
# texts = ["Hello", "How are you?", "Python is awesome for AI development"]
# token_counts = {text: len(text) // 4 for text in texts}
# print("Token Counts:", token_counts)

# ====================Exercise ============================
""" create an function `build_system_prompt` to take parameters:
- name: AI name (e.g., "Aria")
- role: AI's role (e.g., "customer support agent")
- language: response language
- tone: "formal" or "friendly"

Output: A well-formatted system prompt string """

"""def build_system_prompt(name, role, language="English", tone="friendly"):
      tone_instructions = "suitable for instructions about tone or communication style" if tone == "formal" else "alk to me like a friend and keep it friendly."

      prompt = f"You are {name}, a {role}. Please respond in {language}. Your tone should be {tone}. {tone_instructions}"
      return prompt.strip()

print(build_system_prompt("Aria", "customer support agent"))
print("---")
print(build_system_prompt("Atlas", "Python tutor", "Urdu", "formal")) """

# ================================Exercise 2=================================
"""
craete an function `clean_messages` to take a list of messages and return a cleaned list based on token count:
- messages in list
- Every message to take tokens and count (len // 4)
- Total tokens calculate karo
- Agar total > 500 ho toh purane messages hatao
  (system message hamesha rakho, phir latest messages priority)
- Final cleaned messages list return karo
"""

def manage_token_budget(messages, max_tokens=500):
    """API contexts where there is a limit on the number of tokens that can be used in a conversation."""
    
    # System message alag rakho
    system_msgs = [m for m in messages if m["role"] == "system"]
    other_msgs = [m for m in messages if m["role"] != "system"]
    
    def count_tokens(msg_list):
        return sum(len(m["content"]) // 4 for m in msg_list)
    
    # System tokens always count
    system_tokens = count_tokens(system_msgs)
    remaining_budget = max_tokens - system_tokens
    
    # Retain the most recent messages and discard older ones.
    result = []
    current_tokens = 0
    
    for msg in reversed(other_msgs):  # Latest se start
        msg_tokens = len(msg["content"]) // 4
        if current_tokens + msg_tokens <= remaining_budget:
            result.insert(0, msg)
            current_tokens += msg_tokens
        else:
            break
    
    final = system_msgs + result
    print(f"Original messages: {len(messages)}, After trim: {len(final)}")
    print(f"Estimated tokens: ~{count_tokens(final)}")
    return final

# Test
test_messages = [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "Tell me about Python programming language in detail"},
    {"role": "assistant", "content": "Python is a high-level programming language known for simplicity"},
]
result = manage_token_budget(test_messages, max_tokens=30)
for m in result:
    print(f"  {m['role']}: {m['content'][1:30]}")