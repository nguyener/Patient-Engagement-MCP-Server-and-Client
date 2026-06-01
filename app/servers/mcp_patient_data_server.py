import uuid
from mcp.server.fastmcp import FastMCP
from app.db.database import get_connection
from datetime import datetime, date

mcp = FastMCP("PatientDataMCP")

@mcp.resource("policy://registration/washington-only")
def washington_registration_policy() -> str:
    return """
Patient Registration Policy

Only residents of Washington State are allowed to register.

Validation rule:
- state must be WA or Washington
- registration must be rejected for all other states
"""

@mcp.resource("policy://registration/adult-only")
def adult_registration_policy() -> str:
    return """
Patient Registration Policy

Only adults aged 18 or older may self-register.

Rules:
- Age must be >= 18
- Under 18 requires a parent or legal guardian
- Registration must be denied for minors
"""

@mcp.tool()
def register_patient(full_name: str, dob: str, phone: str, email: str, state: str) -> dict:
    print("REGISTER PATIENT CALLED")
    print(full_name)
    print(dob)
    print(phone)
    print(email)
    print(state)
    if not is_washington_resident(state):
        return {
            "success": False,
            "error": "Registration denied. Only Washington residents are allowed to register.",
            "policy": "policy://registration/washington-only"
        }
    
    age = calculate_age(dob)

    if age < 18:
        return {
            "success": False,
            "message":
                "Registration denied. Patient must be at least 18 years old.",
            "policy":
                "policy://registration/adult-only"
        }

    """Register a new patient."""
    patient_id = str(uuid.uuid4())[:8]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO patients (patient_id, full_name, dob, phone, email)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_id, full_name, dob, phone, email))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"Patient registered successfully. Patient ID: {patient_id}",
        "patient_id": patient_id
    }


@mcp.tool()
def get_patient(patient_id: str) -> dict:
    """Get patient profile by patient ID."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    row = cur.fetchone()

    conn.close()

    if not row:
        return {"success": False, "message": "Patient not found."}

    return {"success": True, "patient": dict(row)}


@mcp.tool()
def update_insurance(
    patient_id: str,
    provider: str,
    member_id: str,
    group_number: str
) -> dict:
    """Add or update patient insurance information."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT patient_id FROM patients WHERE patient_id = ?", (patient_id,))
    if not cur.fetchone():
        conn.close()
        return {"success": False, "message": "Patient ID not found."}

    cur.execute("""
        INSERT INTO insurance_records (patient_id, provider, member_id, group_number)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(patient_id)
        DO UPDATE SET
            provider = excluded.provider,
            member_id = excluded.member_id,
            group_number = excluded.group_number
    """, (patient_id, provider, member_id, group_number))

    conn.commit()
    conn.close()

    return {"success": True, "message": "Insurance updated successfully."}


@mcp.tool()
def get_insurance(patient_id: str) -> dict:
    """Get patient insurance information."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM insurance_records WHERE patient_id = ?", (patient_id,))
    row = cur.fetchone()

    conn.close()

    if not row:
        return {"success": False, "message": "No insurance record found."}

    return {"success": True, "insurance": dict(row)}

def is_washington_resident(state: str) -> bool:
    if not state:
        return False

    normalized = state.strip().lower()
    return normalized in {"wa", "washington"}

def calculate_age(dob: str) -> int:
    birth_date = datetime.strptime(dob, "%m/%d/%Y").date()

    today = date.today()

    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) <
           (birth_date.month, birth_date.day))
    )

if __name__ == "__main__":
    mcp.run()