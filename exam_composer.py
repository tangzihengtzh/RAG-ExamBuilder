# -*- coding: utf-8 -*-
"""
exam_composer.py
整合流程：
1. 从 PDF 提取文本并分块
2. 生成顺序嵌入数据库
3. 调用 LLM 生成题目（仅题干）
4. 使用 RAG 检索 + LLM 生成答案与解析
5. 保存完整题库文件
"""

import os
import json
from tqdm import tqdm
from pdf_loader import extract_chunks
from embedder import embed_chunks
from question_gen import generate_question
from answer_rag import retrieve_context, answer_with_rag, load_db

# ==== 路径配置 ====
PDF_PATH = r"E:\python_prj\地震局复习RAG\data\docs\防震减灾知识\防震减灾基础知识.pdf"          # ← 你的测试 PDF 文件路径
DB_PATH = r"./data/db/db.jsonl"
OUTPUT_PATH = r"./data/output"
OUTPUT_FILE = os.path.join(OUTPUT_PATH, "exam_result.jsonl")

# ==== 参数设置 ====
QUESTION_INTERVAL = 1    # 每隔多少个片段出一道题
CONTEXT_TOPK = 4         # RAG 检索片段数量


def main():
    # 0️⃣ 准备输出路径
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # 1️⃣ 提取文本分块
    print("📖 正在读取并分块 PDF 文本...")
    chunks = extract_chunks(PDF_PATH)
    print(f"✅ 共提取 {len(chunks)} 个文本块。")

    # 2️⃣ 嵌入数据库（若已有可跳过）
    if not os.path.exists(DB_PATH):
        print("⚙️ 正在生成嵌入数据库...")
        embed_chunks(chunks, DB_PATH)
    else:
        print("📂 检测到现有嵌入数据库，跳过嵌入步骤。")

    # 3️⃣ 读取数据库
    db = load_db(DB_PATH)
    print(f"✅ 成功加载数据库，共 {len(db)} 条。")

    # 4️⃣ 生成题目并解析
    results = []
    selected_chunks = chunks[::QUESTION_INTERVAL]
    print(f"🧩 计划生成 {len(selected_chunks)} 道题。")

    for chunk in tqdm(selected_chunks, desc="生成题目与解析", ncols=100):
        try:
            # 生成题目
            qtext = generate_question(chunk["text"])
            if not qtext.strip():
                continue

            # 检索上下文
            context = retrieve_context(qtext, db, k=CONTEXT_TOPK)

            # 生成解析
            ans_text = answer_with_rag(qtext, context)

            results.append({
                "source_index": chunk["index"],
                "question": qtext,
                "context_used": context,
                "answer_and_explanation": ans_text
            })
        except Exception as e:
            print(f"[ERROR] 第 {chunk['index']} 段生成失败: {e}")

    # 5️⃣ 保存结果
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in results:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"\n🎯 题库生成完成，共 {len(results)} 道题，已保存到 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
