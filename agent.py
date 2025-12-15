from openai import OpenAI
from pydantic import BaseModel
from typing import Dict, Callable, List
import jso

from tools import (
    search_knowledge_base,
    summarize_text,
    generate_report,
    send_email
)


class Agent:
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.client = OpenAI()
        self.model = model

        self.tools: Dict[str, Callable] = {
            "search_knowledge_base": search_knowledge_base,
            "summarize_text": summarize_text,
            "generate_report": generate_report,
            "send_email": send_email,
        }

        self.system_prompt = (
            "You are a professional research assistant agent.\n"
            "You can search knowledge, summarize findings, generate reports, "
            "and send reports via email.\n"
            "Use tools when necessary. Follow logical steps."
        )

    def run(self, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        for _ in range(8):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self._tool_schemas(),
                tool_choice="auto"
            )

            message = response.choices[0].message

            # Final answer
            if message.tool_calls is None:
                return message.content

            # Tool calls
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                result = self.tools[tool_name](**tool_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result
                })

        return "Agent stopped (too many steps)."

    def _tool_schemas(self) -> List[dict]:
        """
        Explicit tool schemas (LLM contract).
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_knowledge_base",
                    "description": "Search internal knowledge",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "summarize_text",
                    "description": "Summarize text",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_report",
                    "description": "Generate a report",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "summary": {"type": "string"}
                        },
                        "required": ["title", "summary"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_email",
                    "description": "Send report via email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient": {"type": "string"},
                            "report": {"type": "string"}
                        },
                        "required": ["recipient", "report"]
                    }
                }
            }
        ]
