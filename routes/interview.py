from flask import Blueprint, render_template, request, session, redirect
import re

from utils.ai import generate_questions, evaluate_interview
from utils.database import save_interview
from utils.certificate import generate_certificate
from flask import send_file

interview = Blueprint("interview", __name__)


# -----------------------
# Interview Page
# -----------------------
@interview.route("/interview")
def interview_page():

    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "interview.html",
        questions=None
    )


# -----------------------
# Start Interview
# -----------------------
@interview.route("/start_interview", methods=["POST"])
def start_interview():

    category = request.form["category"]

    questions = generate_questions(category)

    session["category"] = category
    session["questions"] = questions
    session["current_question"] = 0
    session["answers"] = []

    return render_template(
        "interview.html",
        questions=questions,
        question=questions[0],
        question_no=1,
        total=len(questions),
        progress=20
    )


# -----------------------
# Next Question
# -----------------------
@interview.route("/next_question", methods=["POST"])
def next_question():

    if "questions" not in session:
        return redirect("/interview")

    answer = request.form["answer"]

    answers = session.get("answers", [])

    current = session["current_question"]

    question = session["questions"][current]

    answers.append({
        "question": question,
        "answer": answer
    })

    session["answers"] = answers

    current += 1
    session["current_question"] = current

    # Interview Complete
    if current >= len(session["questions"]):

        report = evaluate_interview(answers)

        match = re.search(r"(\d+)/100", report)

        score = 0

        if match:
            score = int(match.group(1))

        save_interview(
            session["user_id"],
            session["category"],
            score,
            report
        )

        certificate = generate_certificate(
            session["user_name"],
            session["category"],
            score
        )

        return render_template(
            "result.html",
            answers=answers,
            report=report,
            certificate=certificate
        )

    # Next Question
    progress = int(((current + 1) / len(session["questions"])) * 100)

    return render_template(
        "interview.html",
        questions=session["questions"],
        question=session["questions"][current],
        question_no=current + 1,
        total=len(session["questions"]),
        progress=progress
    )
@interview.route("/download_certificate")
def download_certificate():
    if "user_name" not in session:
        return redirect("/")

    safe_name = session["user_name"].replace(" ", "_")
    file_path = f"certificates/{safe_name}_certificate.pdf"
    return send_file(
        file_path,
        as_attachment=True
    )