# PatientEngagement AI Agent

An Agentic AI healthcare assistant built with Python, Flask, OpenAI Function Calling, MCP (Model Context Protocol), and SQLite.

The system helps patients perform common self-service healthcare operations such as:

* Patient Registration
* Insurance Management
* Appointment Scheduling
* Appointment Rescheduling
* Appointment Cancellation
* Appointment Lookup

The application demonstrates a modern AI architecture where an LLM orchestrates business operations through MCP servers instead of directly calling backend services.

---

## Architecture

```text
Browser UI
    |
    v
Flask Web Application
    |
    v
PatientEngagement Agent
    |
    v
OpenAI LLM
    |
    v
MCP Client
    |
    +-------------------+
    |                   |
    v                   v
PatientDataMCP     SchedulingMCP
    |                   |
    +---------+---------+
              |
              v
          SQLite
```

### Components

#### PatientEngagement Agent

The agent:

* Maintains conversation history
* Understands patient intent
* Collects missing information
* Selects the correct tool
* Calls MCP services
* Generates patient-friendly responses

#### PatientData MCP Server

Responsible for:

* Registering patients
* Retrieving patient information
* Updating insurance information
* Retrieving insurance information

#### Scheduling MCP Server

Responsible for:

* Scheduling appointments
* Rescheduling appointments
* Canceling appointments
* Viewing appointments

#### SQLite Database

Stores:

* Patient profiles
* Insurance records
* Appointment information

---

## Technology Stack

### Backend

* Python 3.11+
* Flask
* SQLite

### AI

* OpenAI API
* Function Calling
* Agentic Workflow

### Integration

* MCP (Model Context Protocol)
* FastMCP

### Frontend

* HTML
* CSS
* JavaScript

---

## Project Structure

```text
patient-engagement/
│
├── app.py
├── agent.py
├── config.py
├── database.py
├── mcp_client.py
│
├── mcp_patient_data_server.py
├── mcp_scheduling_server.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── app.js
│   └── style.css
│
├── patient_engagement.db
│
├── requirements.txt
└── README.md
```

---

## Features

### Register a New Patient

Example:

```text
User:
I would like to register.

Agent:
What is your full name?

User:
John Doe

Agent:
What is your date of birth?

...

Agent:
Registration completed successfully.
Your patient ID is abc12345.
```

---

### Update Insurance

Example:

```text
User:
I need to update my insurance.

Agent:
What is your patient ID?

User:
abc12345

Agent:
Who is your insurance provider?

...
```

---

### Schedule Appointment

Example:

```text
User:
I need to schedule an appointment.

Agent:
What is your patient ID?

User:
abc12345

Agent:
What date would you like?

...
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/nguyener/PatientEngagement-AI-Agent.git

cd PatientEngagement-AI-Agent
```

### Create Virtual Environment

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask openai mcp
```

---

## Configure OpenAI

Set your API key:

### Mac/Linux

```bash
export OPENAI_API_KEY="your_api_key"
```

### Windows

```cmd
set OPENAI_API_KEY=your_api_key
```

---

## Running the Application

### Terminal 1

Start Patient Data MCP Server:

```bash
python mcp_patient_data_server.py
```

### Terminal 2

Start Scheduling MCP Server:

```bash
python mcp_scheduling_server.py
```

### Terminal 3

Start Flask Application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Database

SQLite database file:

```text
patient_engagement.db
```

Inspect data:

```bash
sqlite3 patient_engagement.db
```

List tables:

```sql
.tables
```

View patients:

```sql
SELECT * FROM patients;
```

View appointments:

```sql
SELECT * FROM appointments;
```

Exit:

```sql
.quit
```

---

## Why MCP?

Instead of allowing the LLM to directly call backend functions, MCP provides:

* Standardized tool discovery
* Tool isolation
* Multi-server architecture
* Easier integration with future AI agents
* Better separation of concerns

This architecture mirrors how enterprise AI systems are being designed.

---

## Future Enhancements

* Patient lookup by phone number
* Insurance eligibility verification
* Provider search
* Appointment slot search
* SMS notifications
* Email notifications
* Contact preference management
* Authentication and authorization
* Integration with Electronic Health Records (EHR)
* Integration with Oracle Health / Cerner APIs
* Deployment to AWS, Azure, or OCI

---

## Disclaimer

This project is intended for educational and demonstration purposes.

It does not provide medical advice, diagnosis, or treatment. For medical emergencies, call 911 or visit the nearest emergency room.
