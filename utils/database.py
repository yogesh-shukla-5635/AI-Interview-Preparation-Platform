import sqlite3

DATABASE = "users.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    """)

    # Interview History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        score INTEGER,
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# -------------------------------
# User Functions
# -------------------------------

def create_user(name, email, password, role="user"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
INSERT INTO users(name,email,password,role)
VALUES(?,?,?,?)
""",(name,email,password,role))

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    return user
# -------------------------------
# Interview History
# -------------------------------

def save_interview(user_id, category, score, feedback):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO interview_history
    (user_id, category, score, feedback)
    VALUES (?, ?, ?, ?)
    """, (user_id, category, score, feedback))

    conn.commit()
    conn.close()


def get_interview_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM interview_history
    WHERE user_id = ?
    ORDER BY created_at DESC
    """, (user_id,))

    history = cursor.fetchall()

    conn.close()

    return history

def get_dashboard_stats(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) as total,
            MAX(score) as best,
            AVG(score) as average
        FROM interview_history
        WHERE user_id = ?
    """, (user_id,))

    stats = cursor.fetchone()

    conn.close()

    return {
        "total": stats["total"] or 0,
        "best": stats["best"] or 0,
        "average": round(stats["average"] or 0, 1)
    }