from groq import Groq
from config import Config

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
                    "content": "You are a fair and consistent technical interview evaluator. Follow the scoring rules exactly."
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
You are an expert ATS Resume Reviewer.

Analyze this resume and provide:

1. ATS Score (out of 100)
2. Strengths
3. Weaknesses
4. Missing Skills
5. Improvement Suggestions

Resume:
{resume_text}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS resume reviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Resume Analysis Error: {str(e)}"    