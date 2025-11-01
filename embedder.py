
# SILICONFLOW_API_KEY = "sk-ojnvarqgomblykgvmzljuegstpulbyvnpjvnshusbnjaddzl"
# BASE_URL  = "https://api.siliconflow.cn/v1"
# model="BAAI/bge-large-zh-v1.5",  # 模型名称固定

# embedder.py
from openai import OpenAI
from tqdm import tqdm
import json, os

client = OpenAI(api_key="sk-ojnvarqgomblykgvmzljuegstpulbyvnpjvnshusbnjaddzl", base_url="https://api.siliconflow.cn/v1")

def embed_chunks(chunks, output_file="db.jsonl"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for c in tqdm(chunks, desc="Embedding"):
            resp = client.embeddings.create(model="BAAI/bge-large-zh-v1.5", input=c["text"])
            vec = resp.data[0].embedding
            c["embedding"] = vec
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print("✅ 嵌入完成，顺序数据库已生成。")
