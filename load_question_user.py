# -*- coding: utf-8 -*-
"""
load_question_user.py
交互式刷题程序：
- 从 exam_result.jsonl 读取题目
- 控制台答题
- 统计分数与错题
"""

import json
import os
import random
from tqdm import tqdm

QUESTION_PATH = "./data/output/exam_result.jsonl"
WRONG_LOG_PATH = "./data/output/wrong_log.jsonl"


def load_questions(path):
    """加载题库"""
    if not os.path.exists(path):
        print("❌ 未找到题库文件，请先运行 exam_composer.py")
        return []
    questions = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                item = json.loads(line)
                q_text = item["question"]
                ans_text = item["answer_and_explanation"]

                # 解析题干和选项
                q = parse_question(q_text)
                if not q:
                    continue

                # 从 answer_and_explanation 里提取答案和解析
                answer, explanation = parse_answer(ans_text)
                q["answer"] = answer
                q["explanation"] = explanation
                questions.append(q)
            except Exception as e:
                print(f"[WARN] 解析失败：{e}")
    return questions


def parse_question(text):
    """解析题干部分"""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    q = {"question": "", "options": {}}
    for l in lines:
        if l.startswith("题目"):
            q["question"] = l.replace("题目：", "").strip()
        elif len(l) >= 3 and l[0] in "ABCD" and l[1] == ".":
            q["options"][l[0]] = l[2:].strip()
    if not q["question"] or len(q["options"]) < 2:
        return None
    return q


def parse_answer(text):
    """解析答案与解析"""
    answer, explanation = "", ""
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("答案"):
            answer = line.split("：")[-1].strip().upper()
        elif line.startswith("解析"):
            explanation = line.replace("解析：", "").strip()
    return answer, explanation


def save_wrong(q):
    """记录错题"""
    os.makedirs(os.path.dirname(WRONG_LOG_PATH), exist_ok=True)
    with open(WRONG_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(q, ensure_ascii=False) + "\n")


def main():
    questions = load_questions(QUESTION_PATH)
    if not questions:
        print("❌ 没有题目可用。")
        return

    print(f"📘 成功加载 {len(questions)} 道题。输入 q 退出。\n")

    score = 0
    total = 0

    # 随机顺序出题
    for q in random.sample(questions, len(questions)):
        print("题目：", q["question"])
        for k, v in q["options"].items():
            print(f"  {k}. {v}")

        user_ans = input("\n你的答案（A/B/C/D 或 q 退出）：").strip().upper()
        if user_ans == "Q":
            break

        total += 1
        if user_ans == q["answer"]:
            print("✅ 正确！\n")
            score += 1
        else:
            print(f"❌ 错误！正确答案是：{q['answer']}")
            print(f"解析：{q['explanation']}\n")
            save_wrong(q)

    if total > 0:
        print("🎯 答题结束！")
        print(f"总题数：{total}，正确数：{score}，正确率：{(score / total * 100):.1f}%")
        print(f"📁 错题已保存到：{WRONG_LOG_PATH}\n")


if __name__ == "__main__":
    main()
