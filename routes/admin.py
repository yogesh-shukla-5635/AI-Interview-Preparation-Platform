from flask import Blueprint, render_template, session, redirect
import sqlite3

admin = Blueprint("admin", __name__)

DATABASE = "users.db"


@admin.route("/admin")
def admin_dashboard():

    # Login check
    if "user_id" not in session:
        return redirect("/")

    # Admin check
    if session.get("role") != "admin":
        return redirect("/dashboard")

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Total Users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Total Interviews
    cursor.execute("SELECT COUNT(*) FROM interview_history")
    total_interviews = cursor.fetchone()[0]

    # Average Score
    cursor.execute("SELECT AVG(score) FROM interview_history")
    avg_score = cursor.fetchone()[0]

    if avg_score is None:
        avg_score = 0

    # Recent Users
    cursor.execute("""
        SELECT name, email
        FROM users
        ORDER BY id DESC
        LIMIT 5
    """)
    recent_users = cursor.fetchall()

    # Recent Interviews
    cursor.execute("""
        SELECT category, score, created_at
        FROM interview_history
        ORDER BY id DESC
        LIMIT 5
    """)
    recent_interviews = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_interviews=total_interviews,
        avg_score=round(avg_score, 2),
        recent_users=recent_users,
        recent_interviews=recent_interviews
    )