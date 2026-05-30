import sqlite3
from pathlib import Path

DB_PATH = Path("patient_engagement.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS insurance_records (
            patient_id TEXT PRIMARY KEY,
            provider TEXT NOT NULL,
            member_id TEXT NOT NULL,
            group_number TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id TEXT PRIMARY KEY,
            patient_id TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            provider TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
        )
    """)

    conn.commit()
    conn.close()


init_db()