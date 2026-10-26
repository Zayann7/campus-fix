
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "campusfix-dev-key")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "campusfix.db"))

CATEGORIES = [
    "Classroom",
    "IT & Wi-Fi",
    "Electrical",
    "Plumbing",
    "Library",
    "Cleanliness",
    "Other"
]

STATUSES = ["Open", "In Progress", "Resolved"]
PRIORITIES = ["Low", "Medium", "High"]


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                reporter TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        count = db.execute(
            "SELECT COUNT(*) FROM issues"
        ).fetchone()[0]

        if count == 0:
            sample_issues = [
                (
                    "Projector not working",
                    "Classroom",
                    "Block B - Room 204",
                    "High",
                    "In Progress",
                    "Aarav Patil",
                    "The projector switches on but displays no image.",
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                ),
                (
                    "Unstable Wi-Fi connection",
                    "IT & Wi-Fi",
                    "Central Library",
                    "Medium",
                    "Open",
                    "Sara Khan",
                    "The Wi-Fi connection keeps disconnecting.",
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                ),
                (
                    "Leaking water tap",
                    "Plumbing",
                    "Ground Floor",
                    "Low",
                    "Resolved",
                    "Rohan Shah",
                    "The leaking tap was repaired.",
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                )
            ]

            db.executemany("""
                INSERT INTO issues (
                    title, category, location, priority,
                    status, reporter, description, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, sample_issues)


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "All")
    category_filter = request.args.get("category", "All")

    conditions = []
    parameters = []

    if search:
        conditions.append("""
            (title LIKE ? OR location LIKE ?
             OR reporter LIKE ? OR description LIKE ?)
        """)
        term = f"%{search}%"
        parameters.extend([term, term, term, term])

    if status_filter in STATUSES:
        conditions.append("status = ?")
        parameters.append(status_filter)

    if category_filter in CATEGORIES:
        conditions.append("category = ?")
        parameters.append(category_filter)

    query = "SELECT * FROM issues"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
        ORDER BY
        CASE status
            WHEN 'Open' THEN 1
            WHEN 'In Progress' THEN 2
            ELSE 3
        END,
        id DESC
    """

    with get_db() as db:
        issues = db.execute(query, parameters).fetchall()

        totals = {
            "all": db.execute(
                "SELECT COUNT(*) FROM issues"
            ).fetchone()[0],

            "open": db.execute(
                "SELECT COUNT(*) FROM issues WHERE status='Open'"
            ).fetchone()[0],

            "progress": db.execute(
                "SELECT COUNT(*) FROM issues WHERE status='In Progress'"
            ).fetchone()[0],

            "resolved": db.execute(
                "SELECT COUNT(*) FROM issues WHERE status='Resolved'"
            ).fetchone()[0]
        }

    return render_template(
        "index.html",
        issues=issues,
        totals=totals,
        search=search,
        status_filter=status_filter,
        category_filter=category_filter,
        statuses=STATUSES,
        categories=CATEGORIES
    )


@app.route("/issues", methods=["POST"])
def create_issue():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    location = request.form.get("location", "").strip()
    priority = request.form.get("priority", "").strip()
    reporter = request.form.get("reporter", "").strip()
    description = request.form.get("description", "").strip()

    if not all([
        title, category, location,
        priority, reporter, description
    ]):
        flash("Please complete all fields.", "error")

    elif category not in CATEGORIES or priority not in PRIORITIES:
        flash("Please select a valid category and priority.", "error")

    elif (
        len(title) > 100
        or len(location) > 120
        or len(reporter) > 80
        or len(description) > 1000
    ):
        flash("One or more fields exceed the allowed length.", "error")

    else:
        with get_db() as db:
            db.execute("""
                INSERT INTO issues (
                    title, category, location, priority,
                    status, reporter, description, created_at
                )
                VALUES (?, ?, ?, ?, 'Open', ?, ?, ?)
            """, (
                title,
                category,
                location,
                priority,
                reporter,
                description,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))

        flash("Your issue has been submitted successfully.", "success")

    return redirect(url_for("index"))


@app.route("/issues/<int:issue_id>/status", methods=["POST"])
def update_status(issue_id):
    status = request.form.get("status", "")

    if status not in STATUSES:
        flash("Invalid status selected.", "error")
    else:
        with get_db() as db:
            cursor = db.execute(
                "UPDATE issues SET status = ? WHERE id = ?",
                (status, issue_id)
            )

        if cursor.rowcount:
            flash("Issue status updated.", "success")
        else:
            flash("Issue not found.", "error")

    return redirect(url_for("index"))


@app.route("/issues/<int:issue_id>/delete", methods=["POST"])
def delete_issue(issue_id):
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM issues WHERE id = ?",
            (issue_id,)
        )

    if cursor.rowcount:
        flash("Issue deleted successfully.", "success")
    else:
        flash("Issue not found.", "error")

    return redirect(url_for("index"))


@app.route("/api/issues", methods=["GET"])
def api_issues():
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM issues ORDER BY id DESC"
        ).fetchall()

    return jsonify([dict(row) for row in rows])


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "application": "CampusFix",
        "status": "ok"
    }), 200


initialize_database()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
