from flask import Blueprint, render_template, session, redirect
from utils.database import get_interview_history
from utils.database import get_dashboard_stats
profile = Blueprint("profile", __name__)


# -----------------------
# Dashboard
# -----------------------
@profile.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    stats = get_dashboard_stats(session["user_id"])

    return render_template(
        "dashboard.html",
        username=session["user_name"],
        stats=stats
    )


# -----------------------
# Profile Page
# -----------------------
@profile.route("/profile")
def profile_page():

    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "profile.html",
        username=session["user_name"]
    )


# -----------------------
# Interview History
# -----------------------
@profile.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/")

    history = get_interview_history(session["user_id"])

    return render_template(
        "history.html",
        history=history
    )