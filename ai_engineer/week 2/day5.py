# ============Function Calling (Intro)=========
#what is function calling
"""
NORMAL AI:
User: "What is the weather in Lahore?"
AI: "I don’t know, my training data doesn’t include real-time weather."

FUNCTION CALLING AI:
User: "What is the weather in Lahore?"
AI: "You should call the get_weather() function with city='Lahore'."
[Your code calls the function and fetches real weather data]
AI: "It is currently 32°C in Lahore and sunny."
"""

# 🔸 PART 1: Simple Function Calling Example

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.longcat.chat/openai"
)

# ─────────────────────────────────────────
# 1. First, create a real function that the AI will use.
# ─────────────────────────────────────────

# def get_current_weather(city):
#     """This is a fake weather function — in a real app, this would make an actual API call."""
#     fake_weather_data = {
#         "lahore": {"temp": 32, "condition": "Sunny"},
#         "karachi": {"temp": 30, "condition": "Humid"},
#         "islamabad": {"temp": 25, "condition": "Cloudy"},
#     }
    
#     city_lower = city.lower()
#     data = fake_weather_data.get(city_lower, {"temp": 28, "condition": "Unknown"})
#     return json.dumps(data)


# def calculate(expression):
#     """Simple calculator function"""
#     try:
#         result = eval(expression)  # Note: Using eval() in production is risky — use a safer parser instead.
#         return json.dumps({"result": result})
#     except Exception as e:
#         return json.dumps({"error": str(e)})
    
# ─────────────────────────────────────────
# 2. Tell the AI that these functions are available (tools schema).
# ─────────────────────────────────────────

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_weather",
#             "description": "Provides the current weather of a city",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "city": {
#                         "type": "string",
#                         "description": "Name of City, e.g. Lahore"
#                     }
#                 },
#                 "required": ["city"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "calculate",
#             "description": "Calculates a mathematical expression.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "expression": {
#                         "type": "string",
#                         "description": "Math expression, e.g. '5 + 3 * 2'"
#                     }
#                 },
#                 "required": ["expression"]
#             }
#         }
#     }
# ]

# ─────────────────────────────────────────
# 3. Call the AI — it will decide which tool to use.
# ─────────────────────────────────────────

# def chat_with_tools(user_message):
#     messages = [{"role": "user", "content": user_message}]
    
#     # Step 1: Send the Message to AI, shown the available tools
#     response = client.chat.completions.create(
#         model="LongCat-2.0-Preview",
#         messages=messages,
#         tools=tools
#     )
    
#     response_message = response.choices[0].message
    
#     # Step 2: Check whether the AI decided to use a tool.
#     if response_message.tool_calls:
#         messages.append(response_message)
        
#         # Process every tool call.
#         for tool_call in response_message.tool_calls:
#             function_name = tool_call.function.name
#             function_args = json.loads(tool_call.function.arguments)
            
#             print(f"🔧 AI ne decide kiya: {function_name}({function_args})")
            
#             # Step 3: Make the actual function call.
#             if function_name == "get_current_weather":
#                 result = get_current_weather(**function_args)
#             elif function_name == "calculate":
#                 result = calculate(**function_args)
#             else:
#                 result = json.dumps({"error": "Unknown function"})
            
#             # Step 4: Send the result back to the AI
#             messages.append({
#                 "tool_call_id": tool_call.id,
#                 "role": "tool",
#                 "name": function_name,
#                 "content": result
#             })
        
#         # Step 5: The AI will generate the final response using tool results.
#         final_response = client.chat.completions.create(
#             model="LongCat-2.0-Preview",
#             messages=messages
#         )
#         return final_response.choices[0].message.content
    
#     else:
#         # The AI did not use the tool — it gave a direct answer.
#         return response_message.content


# # ─── Test This ───
# print(chat_with_tools("What is the weather in Lahore?"))
# print()
# print(chat_with_tools("What is 25 × 4 + 10?"))
# print()
# print(chat_with_tools("What is Your Name?"))  # Yeh tool use nahi karega

# =================Exercise============== 
"""
Create 3 tools:

get_current_weather(city)
calculate(expression)
get_time(timezone) — returns a fake time

Then create a single chat function that:

Takes user input
Decides how many tools are needed (it may require multiple tools)
Combines all tool results and provides a final answer
"""
# ==================Solution================
def get_current_weather(city):
    data = {"lahore": {"temp": 32, "condition": "Sunny"}}
    return json.dumps(data.get(city.lower(), {"temp": 28, "condition": "Unknown"}))

def calculate(expression):
    try:
        return json.dumps({"result": eval(expression)})
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_time(timezone="PKT"):
    return json.dumps({"time": "3:45 PM", "timezone": timezone})

available_functions = {
    "get_current_weather": get_current_weather,
    "calculate": calculate,
    "get_time": get_time,
}

tools = [
    {"type": "function", "function": {
        "name": "get_current_weather", "description": "Update the Weather",
        "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}
    }},
    {"type": "function", "function": {
        "name": "calculate", "description": "Calculate the Math",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}
    }},
    {"type": "function", "function": {
        "name": "get_time", "description": "Current time Display",
        "parameters": {"type": "object", "properties": {"timezone": {"type": "string"}}, "required": []}
    }},
]

def multi_tool_chat(user_message):
    messages = [{"role": "user", "content": user_message}]
    response = client.chat.completions.create(model="LongCat-2.0-Preview", messages=messages, tools=tools)
    response_message = response.choices[0].message
    
    if response_message.tool_calls:
        messages.append(response_message)
        
        # Handle multiple tool calls (this is the key part).
        for tool_call in response_message.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 Calling: {func_name}({args})")
            result = available_functions[func_name](**args)
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": func_name,
                "content": result
            })
        
        final = client.chat.completions.create(model="LongCat-2.0-Preview", messages=messages)
        return final.choices[0].message.content
    
    return response_message.content

print(multi_tool_chat("Tell me the weather in Lahore and also calculate 50 × 2."))