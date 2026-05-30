import uuid
from mcp.server.fastmcp import FastMCP
from database import get_connection

mcp = FastMCP("PatientDataMCP")


@mcp.tool()
def register_patient(full_name: str, dob: str, phone: str, email: str) -> dict:
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


if __name__ == "__main__":
    mcp.run()