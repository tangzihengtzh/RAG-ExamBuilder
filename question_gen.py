# question_gen.py
from openai import OpenAI
client = OpenAI(api_key="sk-ojnvarqgomblykgvmzljuegstpulbyvnpjvnshusbnjaddzl", base_url="https://api.siliconflow.cn/v1")

PROMPT = """你是一位考试命题专家。
请根据以下资料内容，编写1道单项选择题。
要求：
1. 包含完整的题目和四个选项（A、B、C、D）。
2. 不要提供答案或解析。
3. 题目应考查资料的核心概念。
4. 题干中不应该出现诸如“根据材料。。”这样的话语，因为出题材料考生不可见

资料：
---
{context}
---
输出格式：
题目：...
A. ...
B. ...
C. ...
D. ...
"""

def generate_question(text):
    resp = client.chat.completions.create(
        model="Pro/deepseek-ai/DeepSeek-V3.1-Terminus",
        messages=[{"role": "user", "content": PROMPT.format(context=text)}],
        temperature=0.7,
        max_tokens=512
    )
    return resp.choices[0].message.content.strip()
