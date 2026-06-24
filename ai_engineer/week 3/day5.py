# ==============Prompt Testing + Optimization===========
from openai import OpenAI
from dotenv import load_dotenv
import os
from collections import Counter

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.longcat.chat/openai")
MODEL = "LongCat-2.0-Preview"
# ─────────────────────────────────────────
# 1. A/B Testing Prompts
# ─────────────────────────────────────────

# def test_prompt_variations(prompt_variations, test_input):
#     """Test multiple prompt versions on the same input."""
#     results = {}
#     for name, template in prompt_variations.items():
#         prompt = template.format(input=test_input)
#         response = client.chat.completions.create(
#             model=MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=100
#         )
#         results[name] = response.choices[0].message.content
#     return results


# prompt_variants = {
#     "v1_basic": "Summarize this: {input}",
#     "v2_with_constraint": "Summarize this in exactly 2 sentences: {input}",
#     "v3_with_role": "Tum professional editor ho. Summarize this in exactly 2 sentences, simple language: {input}",
# }

# test_text = "Artificial Intelligence is transforming industries worldwide. From healthcare to finance, AI systems are automating complex tasks, improving efficiency, and enabling new capabilities that were previously impossible. However, this rapid adoption also raises concerns about job displacement and ethical considerations."

# results = test_prompt_variations(prompt_variants, test_text)
# for version, output in results.items():
#     print(f"🔹 {version}:")
#     print(f"   {output}\n")

# ─────────────────────────────────────────
# 2. Self-Consistency — Multiple runs, majority vote
# ─────────────────────────────────────────

def self_consistency_check(prompt, num_runs=3, temperature=0.9):
    """Run the same prompt multiple times and return the majority response."""
    answers = []
    
    for i in range(num_runs):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=temperature
        )
        answer = response.choices[0].message.content.strip()
        answers.append(answer)
        print(f"   Run {i+1}: {answer}")
    
    most_common = Counter(answers).most_common(1)[0]
    return most_common[0]  # sabse common answer


tricky_question = "If a train travels at 60 km/h for 2.5 hours, how much total distance will it cover? Return only the number."

print("\n🔄 Self-Consistency Check:")
final_answer = self_consistency_check(tricky_question)
print(f"\n✅ Final (majority) answer: {final_answer}")