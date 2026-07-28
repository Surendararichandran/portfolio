"""
database.py
Defines the SQLite schema for the portfolio site and seeds it with
Surendar's real resume content. Run directly to (re)build portfolio.db:

    python database.py
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "portfolio.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    items TEXT NOT NULL,
    sort_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method TEXT NOT NULL,          -- e.g. POST, GET (design motif: shown as an HTTP verb badge)
    route TEXT NOT NULL,           -- e.g. /projects/job-portal-webapp
    status TEXT NOT NULL,          -- e.g. "201 Created"
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    tech TEXT NOT NULL,            -- comma-separated tech chips
    sort_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    org TEXT NOT NULL,
    sort_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school TEXT NOT NULL,
    degree TEXT NOT NULL,
    year TEXT NOT NULL,
    sort_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

SKILLS = [
    ("Language", "Python", 1),
    ("Backend", "Flask, REST APIs, CRUD Operations", 2),
    ("Databases", "MySQL, SQLite, SQL", 3),
    ("Web", "HTML, CSS","Javascript", 4),
    ("Tools", "Git, GitHub, VS Code, MS Office", 5),
]

PROJECTS = [
    (
        "POST", "/projects/job-portal-webapp", "201 Created",
        "Job Portal Web Application",
        "Backend supporting three user roles \u2014 Admin, Employer, and Job Seeker \u2014 "
        "with REST APIs for job posting, search, filtering, and application management. "
        "Session-based authentication and a relational schema keep users, jobs, and "
        "applications consistent.",
        "Python,Flask,SQLite,REST APIs",
        1,
    ),
    (
        "POST", "/projects/car-service-management", "200 OK",
        "Car Service Center Management System",
        "A backend system to manage customers, vehicles, services, invoices, and service "
        "history, on a relational MySQL schema with efficient CRUD operations. Input "
        "validation and exception handling keep it reliable, with an emphasis on modular, "
        "reusable code.",
        "Python,MySQL,CRUD",
        2,
    ),
    (
        "GET", "/projects/ev-charging-system", "Patent Filed",
        "Automatic E-Vehicle Charging System",
        "An automatic charging mechanism using solenoid actuation, triggered by vehicle "
        "weight detection during parking. Patent application no. 202241020246 \u2014 the "
        "hardware project that bridges the mechanical engineering background with the "
        "systems thinking behind it.",
        "Hardware,Automation,Patent App. 202241020246",
        3,
    ),
]

CERTIFICATIONS = [
    ("Python with SQL", "Besant Technologies, Chennai", 1),
    ("SAP Certified Application Associate", "Procurement \u2014 SAP ERP 6.0 EhP7", 2),
    ("Advanced SolidWorks", "Internshala", 3),
    ("ANSYS FLUENT", "Sigma Engineering Service, Coimbatore", 4),
]

EDUCATION = [
    ("M. Kumarasamy College of Engineering", "B.E. Mechanical Engineering", "2023", 1),
    ("Ramasamy Pillai Higher Secondary School", "HSC", "2019", 2),
    ("Sri Parasakthi Vidyalaya CBSE School", "SSLC", "2017", 3),
]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def seed_db():
    """Populate tables only if they're empty, so re-running is safe."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM skills")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO skills (category, items, sort_order) VALUES (?, ?, ?)",
            SKILLS,
        )

    cur.execute("SELECT COUNT(*) FROM projects")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            """INSERT INTO projects
               (method, route, status, title, description, tech, sort_order)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            PROJECTS,
        )

    cur.execute("SELECT COUNT(*) FROM certifications")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO certifications (name, org, sort_order) VALUES (?, ?, ?)",
            CERTIFICATIONS,
        )

    cur.execute("SELECT COUNT(*) FROM education")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO education (school, degree, year, sort_order) VALUES (?, ?, ?, ?)",
            EDUCATION,
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_db()
    print(f"Database ready at portfolio.db")
