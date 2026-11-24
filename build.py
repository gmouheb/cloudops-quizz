#!/usr/bin/env python3
"""Parse the practice-exam markdown files into questions.js for the quiz page.

Usage: python3 build.py

Each entry in EXAMS becomes one exam in the app's exam picker. To add an exam,
add its markdown file here.
"""
import json
import re
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
OUT = HERE / "questions.js"

EXAMS = [
    {
        "id": "soa-c03",
        "code": "SOA-C03",
        "level": "Associate",
        "name": "AWS Certified CloudOps Engineer – Associate",
        "short": "CloudOps Engineer",
        "source": "aws-cloudops-practice-exam-explained.md",
        "note": "The explanations are that file author's reasoning, not AWS's official rationale.",
        "pass": 720,
    },
    {
        "id": "saa-c03",
        "code": "SAA-C03",
        "level": "Associate",
        "name": "AWS Certified Solutions Architect – Associate",
        "short": "Solutions Architect",
        "source": "aws-solutions-architect-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page.",
        "pass": 720,
    },
    {
        "id": "dea-c01",
        "code": "DEA-C01",
        "level": "Associate",
        "name": "AWS Certified Data Engineer – Associate",
        "short": "Data Engineer",
        "source": "aws-data-engineer-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page.",
        "pass": 720,
    },
    {
        "id": "dva-c02",
        "code": "DVA-C02",
        "level": "Associate",
        "name": "AWS Certified Developer – Associate",
        "short": "Developer",
        "source": "aws-developer-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page.",
        "pass": 720,
    },
    {
        "id": "mla-c02",
        "code": "MLA-C02",
        "level": "Associate",
        "name": "AWS Certified Machine Learning Engineer – Associate",
        "short": "ML Engineer",
        "source": "aws-ml-engineer-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page.",
        "pass": 720,
    },
    {
        "id": "clf-c02",
        "code": "CLF-C02",
        "level": "Foundational",
        "name": "AWS Certified Cloud Practitioner",
        "short": "Cloud Practitioner",
        "source": "aws-cloud-practitioner-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page.",
        "pass": 700,
    },
    {
        "id": "aif-c01",
        "code": "AIF-C01",
        "level": "Foundational",
        "name": "AWS Certified AI Practitioner",
        "short": "AI Practitioner",
        "source": "aws-ai-practitioner-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page. The 4 matching questions are split into one question per statement.",
        "pass": 700,
    },
    {
        "id": "dop-c02",
        "code": "DOP-C02",
        "level": "Professional",
        "name": "AWS Certified DevOps Engineer – Professional",
        "short": "DevOps Engineer",
        "source": "aws-devops-engineer-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page.",
        "pass": 750,
    },
    {
        "id": "aip-c01",
        "code": "AIP-C01",
        "level": "Professional",
        "name": "AWS Certified Generative AI Developer – Professional",
        "short": "Generative AI Developer",
        "source": "aws-genai-developer-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page.",
        "pass": 750,
    },
    {
        "id": "aib-c01",
        "code": "AIB-C01",
        "level": "Foundational",
        "name": "AWS Certified AI Business Strategist",
        "short": "AI Business Strategist",
        "source": "aws-ai-business-strategist-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page.",
        "pass": 700,
    },
    {
        "id": "scs-c03",
        "code": "SCS-C03",
        "level": "Specialty",
        "name": "AWS Certified Security – Specialty",
        "short": "Security",
        "source": "aws-security-specialty-practice-exam-explained.md",
        "note": "The explanations are AWS's official rationale from the Skill Builder results page.",
        "pass": 750,
    },
]

MD_EXT = ["fenced_code", "tables"]


def md(text):
    return markdown.markdown(text.strip(), extensions=MD_EXT)


def md_inline(text):
    html = md(text)
    m = re.fullmatch(r"<p>(.*)</p>", html, re.S)
    return m.group(1) if m else html


def parse_topics(text):
    topics = {}
    for m in re.finditer(r"^\| (\d+) \| [A-F, ]+ \| (.+?) \|$", text, re.M):
        topics[int(m.group(1))] = md_inline(m.group(2))
    return topics


def parse_options(lines):
    """Return (stem_lines, options) from the lines before the answer."""
    opts, stem, cur = [], [], None
    for line in lines:
        dash = re.match(r"^- ([A-F])\. (.*)$", line)
        bold = re.match(r"^\*\*([A-F])\.\*\*\s*$", line)
        if dash:
            cur = {"key": dash.group(1), "body": [dash.group(2)]}
            opts.append(cur)
        elif bold:
            cur = {"key": bold.group(1), "body": []}
            opts.append(cur)
        elif cur is None:
            stem.append(line)
        else:
            cur["body"].append(line)
    return stem, [
        {"key": o["key"], "html": md_inline("\n".join(o["body"]))} for o in opts
    ]


def parse_question(num, block, topics):
    lines = block.strip("\n").split("\n")
    while lines and lines[-1].strip() in ("", "---"):
        lines.pop()

    ans_idx = next(i for i, l in enumerate(lines) if l.startswith("**Answer:"))
    answer = re.findall(r"[A-F]", lines[ans_idx].split(":", 1)[1])
    stem, options = parse_options(lines[:ans_idx])

    rest = "\n".join(lines[ans_idx + 1:])
    correct, _, incorrect = rest.partition("**Why the others are incorrect:**")
    correct = correct.replace("**Why correct:**", "", 1)

    keys = [o["key"] for o in options]
    assert keys == [chr(65 + i) for i in range(len(keys))], (num, keys)
    assert set(answer) <= set(keys) and answer, (num, answer)
    assert correct.strip() and incorrect.strip(), num

    return {
        "n": num,
        "topic": topics.get(num, ""),
        "stem": md("\n".join(stem)),
        "options": options,
        "answer": answer,
        "why": md(correct),
        "whyNot": md(incorrect),
    }


def build_exam(meta):
    text = (HERE / meta["source"]).read_text(encoding="utf-8")
    topics = parse_topics(text)
    parts = re.split(r"^## Question (\d+)\s*$", text, flags=re.M)
    questions = [
        parse_question(int(parts[i]), parts[i + 1], topics)
        for i in range(1, len(parts), 2)
    ]
    title = re.search(r"^# (.+)$", text, re.M).group(1)
    return {**meta, "title": title, "questions": questions}


def main():
    exams = [build_exam(meta) for meta in EXAMS]
    OUT.write_text(
        "// Generated by build.py from " + ", ".join(m["source"] for m in EXAMS)
        + ". Do not edit by hand.\n"
        "window.EXAMS = " + json.dumps(exams, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    for exam in exams:
        qs = exam["questions"]
        multi = sum(len(q["answer"]) > 1 for q in qs)
        print(f"{exam['code']}: {len(qs)} questions ({multi} multi-select)")
    print(f"Wrote {len(exams)} exams to {OUT.name}")


if __name__ == "__main__":
    main()
