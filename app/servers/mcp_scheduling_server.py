import uuid
from mcp.server.fastmcp import FastMCP
from app.db.database import get_connection

mcp = FastMCP("SchedulingMCP")


@mcp.tool()
def schedule_appointment(
    patient_id: str,
    date: str,
    time: str,
    provider: str
) -> dict:
    """Schedule a patient appointment."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT patient_id FROM patients WHERE patient_id = ?", (patient_id,))
    if not cur.fetchone():
        conn.close()
        return {"success": False, "message": "Patient ID not found."}

    appointment_id = str(uuid.uuid4())[:8]

    cur.execute("""
        INSERT INTO appointments (
            appointment_id, patient_id, date, time, provider, status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        appointment_id,
        patient_id,
        date,
        time,
        provider,
        "scheduled"
    ))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"Appointment scheduled successfully. Appointment ID: {appointment_id}",
        "appointment_id": appointment_id
    }


@mcp.tool()
def cancel_appointment(appointment_id: str) -> dict:
    """Cancel an existing appointment."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM appointments WHERE appointment_id = ?", (appointment_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return {"success": False, "message": "Appointment ID not found."}

    cur.execute("""
        UPDATE appointments
        SET status = ?
        WHERE appointment_id = ?
    """, ("cancelled", appointment_id))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Appointment cancelled successfully."
    }


@mcp.tool()
def reschedule_appointment(
    appointment_id: str,
    new_date: str,
    new_time: str
) -> dict:
    """Reschedule an existing appointment."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM appointments WHERE appointment_id = ?", (appointment_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return {"success": False, "message": "Appointment ID not found."}

    cur.execute("""
        UPDATE appointments
        SET date = ?, time = ?, status = ?
        WHERE appointment_id = ?
    """, (new_date, new_time, "rescheduled", appointment_id))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Appointment rescheduled successfully."
    }


@mcp.tool()
def view_appointments(patient_id: str) -> dict:
    """View appointments for a patient."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM appointments
        WHERE patient_id = ?
        ORDER BY date, time
    """, (patient_id,))

    rows = cur.fetchall()
    conn.close()

    return {
        "success": True,
        "appointments": [dict(row) for row in rows]
    }


if __name__ == "__main__":
    mcp.run()