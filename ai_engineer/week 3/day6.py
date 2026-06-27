# Mega Exercises + Week Review

from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.longcat.chat/openai")
MODEL = "LongCat-2.0-Preview"

CODE_TEACHER_PERSONA = """Tum ek bohot patient code teacher ho.
Beginners ko Python samjhate ho, simple Roman Urdu/English mix mein.
Step-by-step explain karte ho, kabhi assume nahi karte ke student ko sab pata hai."""

EXPLAIN_TEMPLATE = """Yeh code line-by-line samjhao, step by step socho:

```python
{code}
```

Format mein jawab do:
<summary>2-3 lines mein code kya karta hai</summary>
<line_by_line>har important line ka explanation, numbered</line_by_line>
<potential_bugs>koi edge case ya bug jo ho sakta hai, ya "None found"</potential_bugs>"""


def explain_code(code_string):
    prompt = EXPLAIN_TEMPLATE.format(code=code_string)
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": CODE_TEACHER_PERSONA},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    
    raw = response.choices[0].message.content
    
    def extract_tag(tag, text):
        match = re.search(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
        return match.group(1).strip() if match else "Not found"
    
    return {
        "summary": extract_tag("summary", raw),
        "line_by_line": extract_tag("line_by_line", raw),
        "potential_bugs": extract_tag("potential_bugs", raw),
        "raw_response": raw
    }


# ─── Test karo ───
test_code = """def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)"""

result = explain_code(test_code)

print("📋 SUMMARY:")
print(result["summary"])
print("\n📝 LINE BY LINE:")
print(result["line_by_line"])
print("\n⚠️ POTENTIAL BUGS:")
print(result["potential_bugs"])

# Bonus observation: Empty list pass karo to dekho kya bug catch hota hai (division by zero!)