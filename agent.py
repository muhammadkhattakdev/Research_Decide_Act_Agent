from openai import OpenAI
from pydantic import Field, BaseModel
from typing import Dict, Callable, List
import json

from tools import search_knowledge_base, summarize_text, generate_report, send_email


class Agent:

    def __init__(self, model:str = "gpt-4.1-mini"):

        self.model = model
        self.client = OpenAI()

        self.tools: Dict[str, Callable] = {
            "search_knowledge_base": search_knowledge_base,
            "summarized_text": summarize_text,
            "generate_report": generate_report,
            "send_email": send_email
        }

        self.system_prompt = """
            "You are a professional research assistant agent.\n"
            "You can search knowledge, summarize findings, generate reports, "
            "and send reports via email.\n"
            "Use tools when necessary. Follow logical steps."
        """

    def run(self, user_prompt: str ) -> str:

        messages = [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': user_prompt},
        ]

        for _ in range(8):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self._tool_schemas(),
                tool_choice="auto",
            )

            message = response.choices[0].message

            
            if message.tool_calls is None:
                return message.content
            
            messages.append(message)
            
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                result = self.tools[tool_name](**tool_args)

                messages.append({
                    'role': "tool",
                    'tool_call_id': tool_call.id,
                    'name': tool_name,
                    'content': result,
                })

        return "Agent stopped(too many steps)."
    
    def _tool_schemas(self) -> str:

        """Explicit tool schemas (LLM Contract)"""
        
        schema = [
            {
                'type': 'function'
            }
        ]



