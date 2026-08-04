import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
)

# Load Environment Variables
load_dotenv()

os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL_NAME = os.getenv("CLAUDE_MODEL_NAME")


app = FastAPI(
    title="Claude Agent SDK API",
    description="Expose a Claude Agent via FastAPI",
    version="1.0"
)

# Request Model
class ChatRequest(BaseModel):
    prompt: str

# Chat Endpoint
@app.post("/chat")
async def chat(request: ChatRequest):

    response_text = ""
    tool_calls = []

    async for message in query(

        prompt=request.prompt,

        options=ClaudeAgentOptions(

            model=CLAUDE_MODEL_NAME,

            mcp_servers={
                "MSLearnMCPServer": {
                    "type": "http",
                    "url": "https://learn.microsoft.com/api/mcp"
                }
            },

            allowed_tools=[
                "mcp__MSLearnMCPServer__*",
                "Read",
                "Edit",
                "Glob",
                "WebSearch",
                "WebFetch"
            ]
        ),
    ):

        if isinstance(message, AssistantMessage):

            for block in message.content:

                # Capture streamed assistant text
                if hasattr(block, "text") and block.text:
                    response_text += block.text

                # Capture tool invocations
                elif hasattr(block, "name"):
                    tool_calls.append(block.name)

        elif isinstance(message, ResultMessage):

            if message.result:
                response_text = message.result

    return {
        "response": response_text,
        "tools_used": tool_calls
    }