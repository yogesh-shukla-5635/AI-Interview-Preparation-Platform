from groq import Groq
from config import Config
import re

client = Groq(api_key=Config.GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-20b"


def generate_questions(category):

    prompt = f"""
You are an experienced technical interviewer.

Generate 5 interview questions for the category: {category}

Rules:
- Medium difficulty
- Number them from 1 to 5
- Only questions
- No answers
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response.choices[0].message.content.strip()

    questions = []

    for line in text.split("\n"):
        line = line.strip()

        if line:
            if line[0].isdigit():
                questions.append(line[2:].strip())

    return questions


def evaluate_interview(answers):

    interview_text = ""

    for i, item in enumerate(answers, start=1):

        interview_text += f"""
Question {i}:
{item['question']}

Candidate Answer {i}:
{item['answer']}
"""

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answers fairly and accurately.

{interview_text}

IMPORTANT SCORING RULES:

- There are exactly {len(answers)} questions.
- Evaluate EVERY answer individually.
- Do NOT give a very low score just because an answer is short.
- If the answer is relevant and mostly correct, give good marks.
- Give low marks only if the answer is irrelevant, incorrect, empty, or says "I don't know".
- Consider technical correctness, relevance, clarity, and completeness.

Score each question using this scale:

0 = No answer or completely incorrect
1 = Very poor
2 = Partially correct
3 = Good and mostly correct
4 = Very good
5 = Excellent and technically correct

Calculate the final score out of 100 based on all questions.

Return EXACTLY in this format:

Overall Score: <score>/100

Question-wise Evaluation:
1. Score: <score>/5 - <short feedback>
2. Score: <score>/5 - <short feedback>
3. Score: <score>/5 - <short feedback>
4. Score: <score>/5 - <short feedback>
5. Score: <score>/5 - <short feedback>

Strengths:
- Point 1
- Point 2
- Point 3

Weaknesses:
- Point 1
- Point 2
- Point 3

Suggestions:
- Point 1
- Point 2
- Point 3
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a fair and consistent technical interview "
                        "evaluator. Follow the scoring rules exactly."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Evaluation Error: {str(e)}"


def analyze_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer and AI/ML career advisor.

Analyze the following resume carefully and generate a professional ATS evaluation.

RESUME:
{resume_text}

STRICT OUTPUT FORMAT RULES:

1. Return ONLY valid Markdown.
2. Do NOT return HTML.
3. Do NOT use code fences.
4. Do NOT add introductory text before the report.
5. Every table must use valid Markdown syntax.
6. Every table row must contain the same number of columns as its header.
7. Always separate columns using the | symbol.
8. Never merge column names together.
9. Keep the analysis clear, concise, and professional.
10. Give realistic scores based only on the actual resume content.

Use EXACTLY this structure:

# ATS Score: X/100

## Score Breakdown

| Category | Score | Rationale |
|---|---:|---|
| Keyword Match | X/100 | Brief explanation |
| Formatting & Readability | X/100 | Brief explanation |
| Section Structure | X/100 | Brief explanation |
| Content Depth | X/100 | Brief explanation |
| Overall | X/100 | Brief explanation |

---

## 1. Strengths

| Strength | Why It Matters |
|---|---|
| Strength 1 | Brief explanation |
| Strength 2 | Brief explanation |
| Strength 3 | Brief explanation |
| Strength 4 | Brief explanation |
| Strength 5 | Brief explanation |

---

## 2. Weaknesses

| Issue | Why It Hurts ATS or Hiring |
|---|---|
| Issue 1 | Brief explanation |
| Issue 2 | Brief explanation |
| Issue 3 | Brief explanation |
| Issue 4 | Brief explanation |
| Issue 5 | Brief explanation |

---

## 3. Missing Skills

| Category | Recommended Skills |
|---|---|
| ML/DL Frameworks | Relevant missing skills |
| NLP & LLMs | Relevant missing skills |
| Data Handling | Relevant missing skills |
| Model Deployment | Relevant missing skills |
| Version Control & DevOps | Relevant missing skills |
| Cloud & Infrastructure | Relevant missing skills |

---

## 4. Improvement Suggestions

1. Specific improvement suggestion based on the resume.
2. Specific improvement suggestion based on the resume.
3. Specific improvement suggestion based on the resume.
4. Specific improvement suggestion based on the resume.
5. Specific improvement suggestion based on the resume.

FINAL CHECK BEFORE RESPONDING:

- Do not use code fences.
- Do not generate HTML.
- Do not merge table headers.
- Ensure all tables have correctly separated columns.
- Ensure every row has the same number of columns.
- Use only information supported by the resume.
- Return the report only.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise ATS resume reviewer. "
                        "Follow the requested Markdown structure exactly. "
                        "Validate all Markdown tables before responding."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content.strip()
        
        result = re.sub(r'^```[a-zA-Z]*\s*', '', result)
        result = re.sub(r'\s*```$', '', result)
        return result.strip() 

    except Exception as e:
        return f"Resume Analysis Error: {str(e)}"
