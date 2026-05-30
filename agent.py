print("here 1")
import json
import asyncio
from openai import OpenAI
from config import SYSTEM_PROMPT, MODEL
from mcp_client import MCPToolClient

client = OpenAI()

print("here 2")
class PatientEngagementAgent:
    def __init__(self):
        self.mcp_client = MCPToolClient()

        self.conversation = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        self.tools = [
            {
                "type": "function",
                "name": "register_patient",
                "description": "Register a new patient.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "full_name": {"type": "string"},
                        "dob": {"type": "string"},
                        "phone": {"type": "string"},
                        "email": {"type": "string"}
                    },
                    "required": ["full_name", "dob", "phone", "email"],
                    "additionalProperties": False
                }
            },
            {
                "type": "function",
                "name": "update_insurance",
                "description": "Update patient insurance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {"type": "string"},
                        "provider": {"type": "string"},
                        "member_id": {"type": "string"},
                        "group_number": {"type": "string"}
                    },
                    "required": ["patient_id", "provider", "member_id", "group_number"],
                    "additionalProperties": False
                }
            },
            {
                "type": "function",
                "name": "schedule_appointment",
                "description": "Schedule appointment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {"type": "string"},
                        "date": {"type": "string"},
                        "time": {"type": "string"},
                        "provider": {"type": "string"}
                    },
                    "required": ["patient_id", "date", "time", "provider"],
                    "additionalProperties": False
                }
            },
            {
                "type": "function",
                "name": "cancel_appointment",
                "description": "Cancel appointment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {"type": "string"}
                    },
                    "required": ["appointment_id"],
                    "additionalProperties": False
                }
            },
            {
                "type": "function",
                "name": "reschedule_appointment",
                "description": "Reschedule appointment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {"type": "string"},
                        "new_date": {"type": "string"},
                        "new_time": {"type": "string"}
                    },
                    "required": ["appointment_id", "new_date", "new_time"],
                    "additionalProperties": False
                }
            },
            {
                "type": "function",
                "name": "view_appointments",
                "description": "View appointments.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "patient_id": {"type": "string"}
                    },
                    "required": ["patient_id"],
                    "additionalProperties": False
                }
            }
        ]

        self.tool_to_server = {
            "register_patient": "patient",
            "update_insurance": "patient",
            "get_patient": "patient",
            "get_insurance": "patient",
            "schedule_appointment": "scheduling",
            "cancel_appointment": "scheduling",
            "reschedule_appointment": "scheduling",
            "view_appointments": "scheduling",
        }

    def handle_message(self, user_input: str) -> str:
        self.conversation.append({
            "role": "user",
            "content": user_input
        })

        response = client.responses.create(
            model=MODEL,
            input=self.conversation,
            tools=self.tools
        )

        self.conversation += response.output

        for item in response.output:
            if item.type == "function_call":
                tool_name = item.name
                arguments = json.loads(item.arguments)

                server_name = self.tool_to_server[tool_name]

                tool_result = asyncio.run(
                    self.mcp_client.call_tool(
                        server_name=server_name,
                        tool_name=tool_name,
                        arguments=arguments
                    )
                )

                self.conversation.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": tool_result
                })

                final_response = client.responses.create(
                    model=MODEL,
                    input=self.conversation,
                    tools=self.tools
                )

                self.conversation += final_response.output
                return final_response.output_text

        return response.output_text