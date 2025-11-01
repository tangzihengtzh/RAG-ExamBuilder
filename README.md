# 📘 StudyRAG — 基于 RAG 的教材自动出题与交互答题系统

一个轻量级的 **Retrieval-Augmented Generation (RAG)** 项目，  
可从 PDF/Word 教材自动生成高质量的选择题，并支持交互式答题、错题记录与解析。

---

## 🚀 项目简介

**StudyRAG** 旨在帮助学习者高效复习教材内容。  
它通过 LLM + 向量数据库实现以下功能：

1. 📖 从教材 PDF 中自动提取文本并顺序切片；  
2. 🧠 调用硅基流动 API 生成文本嵌入（支持中文模型 `BAAI/bge-large-zh-v1.5`）；  
3. ✍️ 使用 LLM 自动生成题目（仅题干与选项）；  
4. 🔍 利用 RAG 检索生成答案与解析；  
5. 💬 提供交互式答题与错题记录功能。

---

## 🗂️ 项目结构

```
地震局复习RAG/
│
├── pdf_loader.py          # 从 PDF 提取文本并分块
├── embedder.py            # 调用硅基流动 API 生成嵌入
├── question_gen.py        # 仅根据材料生成题目
├── answer_rag.py          # 检索上下文并生成答案与解析
├── exam_composer.py       # 整合流程，生成完整题库
└── load_question_user.py  # 控制台交互式答题程序
```

---

## ⚙️ 环境配置

```bash
pip install openai tqdm PyPDF2
```

可选（更稳定的 PDF 解析）：
```bash
pip install pymupdf
```

---

## 🔑 硅基流动 API 设置

在代码中替换为你自己的 API Key：
```python
client = OpenAI(api_key="sk-你的密钥", base_url="https://api.siliconflow.cn/v1")
```

---

## 🧩 使用方法

### 1️⃣ 从教材提取与嵌入
```bash
python exam_composer.py
```
系统将：
- 提取 PDF 文本；
- 生成嵌入数据库；
- 调用 LLM 生成题目与解析；
- 输出到 `./data/output/exam_result.jsonl`

### 2️⃣ 交互式刷题
```bash
python load_question_user.py
```
支持：
- 随机出题；
- 答题判定；
- 自动记录错题到 `wrong_log.jsonl`。

---

## 📄 输出示例

```json
{
  "source_index": 12,
  "question": "题目：地震纵波与横波的传播速度比较如何？\nA. 纵波更快\nB. 横波更快\nC. 两者相同\nD. 无法确定",
  "answer_and_explanation": "答案：A\n解析：纵波传播速度比横波快，可通过固体与液体。"
}
```

---

## 💡 特点

- ✅ 完全中文支持（嵌入 + 出题 + 答题）
- ✅ 顺序嵌入，支持上下文扩展
- ✅ 出题与答题分离，质量可控
- ✅ RAG 检索增强解题，提供可追溯依据
- ✅ 控制台交互式体验 + 错题本功能

---

## 🧠 未来计划

- [ ] 增加错题复练模式  
- [ ] 支持多 PDF 批量处理  
- [ ] 题目质量自动评估与过滤  
- [ ] 导出 DOCX / PDF 试卷  

---

# 📘 English Version — StudyRAG: RAG-Based Exam Builder

**StudyRAG** is a lightweight Retrieval-Augmented Generation (RAG) project that  
automatically generates multiple-choice questions from textbooks (PDF/Word) and  
provides interactive quiz and error logging features.

---

## 🚀 Overview

StudyRAG leverages LLMs and vector embeddings to:
1. 📖 Extract ordered text chunks from textbooks;
2. 🧠 Generate embeddings via SiliconFlow API (`BAAI/bge-large-zh-v1.5`);
3. ✍️ Produce quiz questions (without answers);
4. 🔍 Use RAG retrieval to generate correct answers and explanations;
5. 💬 Provide a terminal-based interactive quiz interface.

---

## 🗂️ Project Structure

```
RAG-ExamBuilder/
│
├── pdf_loader.py          # PDF text extraction and chunking
├── embedder.py            # Embedding generation (SiliconFlow API)
├── question_gen.py        # Question generation (no answers)
├── answer_rag.py          # RAG-based answer & explanation generation
├── exam_composer.py       # Main orchestration pipeline
└── load_question_user.py  # Interactive quiz interface
```

---

## ⚙️ Environment Setup

```bash
pip install openai tqdm PyPDF2
# Optional
pip install pymupdf
```

---

## 🔑 SiliconFlow API Configuration

Replace with your own API key:
```python
client = OpenAI(api_key="sk-your-key", base_url="https://api.siliconflow.cn/v1")
```

---

## 🧩 Usage

### Step 1 — Generate Questions & Answers
```bash
python exam_composer.py
```
Generates:
- Chunked text
- Embedding database
- LLM-generated questions & explanations
- Output → `./data/output/exam_result.jsonl`

### Step 2 — Interactive Quiz
```bash
python load_question_user.py
```
Features:
- Randomized quiz order  
- Auto grading  
- Error logging to `wrong_log.jsonl`

---

## 📄 Example Output

```json
{
  "source_index": 12,
  "question": "Question: How does the propagation speed of P-waves compare to S-waves?\nA. P-waves are faster\nB. S-waves are faster\nC. Both are equal\nD. Cannot be determined",
  "answer_and_explanation": "Answer: A\nExplanation: P-waves travel faster and can propagate through both solids and liquids."
}
```

---

## 💡 Features

- ✅ Full Chinese-language support  
- ✅ Ordered embeddings (context continuity)  
- ✅ Separated question and answer generation  
- ✅ RAG-enhanced explanations  
- ✅ CLI-based interaction + error log

---

## 🧠 Future Improvements

- [ ] Wrong-question replay mode  
- [ ] Multi-PDF batch processing  
- [ ] Auto quality evaluation  
- [ ] DOCX/PDF exam export  

---

## 📜 License
MIT License © 2025 StudyRAG Team
