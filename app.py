
from flask import Flask, render_template, request, jsonify
from database import get_connection, init_db, seed_db

app = Flask(__name__)


def fetch_all(query):
    conn = get_connection()
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.route("/")
def index():
    skills = fetch_all("SELECT * FROM skills ORDER BY sort_order")
    projects = fetch_all("SELECT * FROM projects ORDER BY sort_order")
    certifications = fetch_all("SELECT * FROM certifications ORDER BY sort_order")
    education = fetch_all("SELECT * FROM education ORDER BY sort_order")

    
    for project in projects:
        project["tech"] = [t.strip() for t in project["tech"].split(",")]

    return render_template(
        "index.html",
        skills=skills,
        projects=projects,
        certifications=certifications,
        education=education,
    )


@app.route("/api/projects")
def api_projects():
    projects = fetch_all("SELECT * FROM projects ORDER BY sort_order")
    for project in projects:
        project["tech"] = [t.strip() for t in project["tech"].split(",")]
    return jsonify(projects)


@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"status": "error", "detail": "name, email, and message are all required"}), 400

    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message),
    )
    conn.commit()
    conn.close()

    return jsonify({"status": " ", "detail": " Thanks for reaching out."}), 201


if __name__ == "__main__":
    init_db()
    seed_db()
    app.run(debug=True)
