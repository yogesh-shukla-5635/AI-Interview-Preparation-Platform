from flask import Blueprint, render_template, request, session, redirect
import os

from utils.resume_parser import extract_resume_text
from utils.ai import analyze_resume

resume = Blueprint("resume", __name__)

UPLOAD_FOLDER = "uploads"

# -----------------------
# Resume Analyzer
# -----------------------

@resume.route("/resume", methods=["GET", "POST"])
def resume_page():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        file = request.files["resume"]

        if file.filename == "":
            return "Please select a PDF file."

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)

        file.save(filepath)

        # Extract text
        resume_text = extract_resume_text(filepath)

        # AI Analysis
        report = analyze_resume(resume_text)

        return render_template(
            "resume_result.html",
            report=report
        )

    return render_template("resume.html")