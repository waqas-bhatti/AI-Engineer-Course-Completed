#  =======Prompt Templates (Reusable Patterns)==========
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.longcat.chat/openai")
MODEL = "LongCat-2.0-Preview"
# ─────────────────────────────────────────
# 1. Simple String Template
# ─────────────────────────────────────────

# EXPLAIN_TEMPLATE = """You are an expert in {expertise}.
# Explain {topic} for {audience}.
# Keep the response {length}.
# Language: {language}"""

# def explain_topic(topic, expertise="programming", audience="beginner", length="short (3-4 lines)", language="English"):
#     prompt = EXPLAIN_TEMPLATE.format(
#         expertise=expertise, topic=topic, audience=audience, length=length, language=language
#     )
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=200
#     )
#     return response.choices[0].message.content

# # Test — Same template, different parameters
# print(explain_topic("APIs"))
# print()
# print(explain_topic("APIs", audience="senior engineer", length="detailed", language="English"))

# ─────────────────────────────────────────
# 2. Class-based Template System (Pattern)
# ─────────────────────────────────────────

# class PromptTemplate:
#     """Reusable prompt template — this pattern is used in applications."""
    
#     def __init__(self, template_string, required_vars):
#         self.template = template_string
#         self.required_vars = required_vars
    
#     def render(self, **kwargs):
#         """Fill in the variables in the template"""
#         missing = [v for v in self.required_vars if v not in kwargs]
#         if missing:
#             raise ValueError(f"Missing variables: {missing}")
#         return self.template.format(**kwargs)
    
#     def run(self, client, model, max_tokens=300, **kwargs):
#         """Template render karo aur direct API call kar do"""
#         prompt = self.render(**kwargs)
#         response = client.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=max_tokens
#         )
#         return response.choices[0].message.content


# # ─── Templates Library banao ───
# code_review_template = PromptTemplate(
#     template_string="""You are a code reviewer. Review this {language} code.:

# ```{language}
# {code}
# ```

# Tell me:
# 1) Bugs (if any)
# 2) Improvements
# 3) Whether best practices are being followed or not""",
#     required_vars=["language", "code"]
# )

# # Test
# sample_code = """
# def add(a, b):
#     return a+b
# """

# result = code_review_template.run(
#     client, MODEL,
#     language="Python",
#     code=sample_code,
#     max_tokens=250
# )
# print(result)

# ============================================
'''
Create a "Professional Email Generator" using the PromptTemplate class:
Variables: recipient_name, purpose, tone (formal/casual), key_points (list)

Test it with 2 scenarios:
1. Leave request to boss
2. Project update to client
'''
# Solution
class PromptTemplate:
    def __init__(self, template_string, required_vars):
        self.template = template_string
        self.required_vars = required_vars
    
    def render(self, **kwargs):
        missing = [v for v in self.required_vars if v not in kwargs]
        if missing:
            raise ValueError(f"Missing: {missing}")
        return self.template.format(**kwargs)
    
    def run(self, client, model, max_tokens=300, **kwargs):
        prompt = self.render(**kwargs)
        response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], max_tokens=max_tokens)
        return response.choices[0].message.content

email_template = PromptTemplate(
    template_string="""Your Professioal Email writer, Now this write email:

To: {recipient_name}
Purpose: {purpose}
Tone: {tone}
Key points that need to be included: {key_points}

Write it in a complete professional email format, including a subject line.""",
    required_vars=["recipient_name", "purpose", "tone", "key_points"]
)

# Scenario 1
result1 = email_template.run(
    client, MODEL,
    recipient_name="Manager",
    purpose="Leave request",
    tone="formal",
    key_points=", ".join(["I need 2 days of leave", "personal reasons", "I will hand over my work to my colleague"])
)
print("EMAIL 1:\n", result1)
print("\n" + "="*50 + "\n")

# Scenario 2
result2 = email_template.run(
    client, MODEL,
    recipient_name="Client",
    purpose="Project status update",
    tone="formal but friendly",
    key_points=", ".join(["Phase 1 is completed", "Phase 2 will start next week", "No blockers"])
)
print("EMAIL 2:\n", result2)