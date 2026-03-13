"""
storage.py - Handles saving jobs to SQLite so we don't send duplicate emails.
"""

import sqlite3

DB_PATH = "jobs.db"


def init_db():
    """Creates the jobs table if it doesn't already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seen_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,          -- UNIQUE prevents duplicate entries
            title TEXT,
            company TEXT,
            source TEXT,
            date_found TEXT DEFAULT (DATE('now'))
        )
    """)
    conn.commit()
    conn.close()


def save_jobs(jobs: list[dict]):
    """Saves a list of new jobs to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for job in jobs:
        # INSERT OR IGNORE skips the row if the URL already exists
        cursor.execute("""
            INSERT OR IGNORE INTO seen_jobs (url, title, company, source)
            VALUES (?, ?, ?, ?)
        """, (job["url"], job["title"], job["company"], job["source"]))
    conn.commit()
    conn.close()


def get_new_jobs(jobs: list[dict]) -> list[dict]:
    """
    Filters out jobs we've already seen.
    Returns only jobs whose URLs are NOT in the database yet.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    new_jobs = []
    for job in jobs:
        cursor.execute("SELECT 1 FROM seen_jobs WHERE url = ?", (job["url"],))
        if cursor.fetchone() is None:  # not found in DB = new job
            new_jobs.append(job)

    conn.close()
    return new_jobs
