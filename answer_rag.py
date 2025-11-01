# answer_rag.py
import numpy as np
from openai import OpenAI
import json

client = OpenAI(api_key="sk-ojnvarqgomblykgvmzljuegstpulbyvnpjvnshusbnjaddzl", base_url="https://api.siliconflow.cn/v1")

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))

def load_db(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def retrieve_context(question_text, db, k=3):
    q_emb = client.embeddings.create(model="BAAI/bge-large-zh-v1.5", input=question_text).data[0].embedding
    sims = [(cosine(np.array(q_emb), np.array(item["embedding"])), item) for item in db]
    sims.sort(key=lambda x: x[0], reverse=True)
    topk = [s[1]["text"] for s in sims[:k]]
    # ↑可根据 index 取相邻上下文进一步扩展
    return "\n".join(topk)

def answer_with_rag(question_text, context_text):
    PROMPT = f"""请根据以下资料回答选择题，并给出正确选项与简短解析。
题目：
{question_text}

资料：
{context_text}

输出格式：
答案：<A/B/C/D>
解析：<一句话说明>
"""
    resp = client.chat.completions.create(
        model="Pro/deepseek-ai/DeepSeek-V3.1-Terminus",
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0.3,
        max_tokens=512
    )
    return resp.choices[0].message.content.strip()
