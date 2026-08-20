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

Answer {i}:
{item['answer']}

"""

    prompt = f"""
You are an expert technical interviewer.

Evaluate the following interview.

{interview_text}

Return your response EXACTLY in this format.

Overall Score: <score>/100

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
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.5

        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

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

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content