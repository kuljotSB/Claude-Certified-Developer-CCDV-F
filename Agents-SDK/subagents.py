# pip install claude-agent-sdk==0.2.129

# import statements
import asyncio
from claude_agent_sdk import (
    query, 
    ClaudeAgentOptions, 
    AssistantMessage, 
    AgentDefinition,
    ResultMessage
)
import os
from dotenv import load_dotenv
import asyncio
from typing import Any

load_dotenv()

os.environ["ANTHROPIC_API_KEY"] = os.getenv("CLAUDE_API_KEY")
claude_model_name = os.getenv("CLAUDE_MODEL_NAME")


# Define the Agents
MARKETING_AGENTS = {
    "market-researcher": AgentDefinition(
      description="Expert in market research and customer analysis.",

        prompt="""
You are a senior market research consultant.

Your responsibilities include:

- Identifying target audiences
- Creating buyer personas
- Performing competitor analysis
- Identifying customer pain points

Provide concise business recommendations.
""",

        tools=[]
    ),

    "content-creator": AgentDefinition(
        description="Expert in marketing content creation.",

        prompt="""
You are an experienced content marketing specialist.

Create engaging:

- LinkedIn posts
- Product announcements
- Marketing copy
- Promotional content

Keep your writing concise, professional, and persuasive.
""",

        tools=[]
    )
}


# Declare the main function block

async def main():
    async for message in query(
            prompt="""
Use the market-researcher agent to identify the target audience
for an AI-powered fitness smartwatch.

After that, use the content-creator agent to write a professional
LinkedIn product launch announcement.
""",
            options=ClaudeAgentOptions(
                model=claude_model_name,
                allowed_tools=["Agent"],
                agents = MARKETING_AGENTS
            ),
        ):
    
            if isinstance(message, AssistantMessage):

                for block in message.content:

                    if hasattr(block, "text") and block.text:
                        print(block.text)

                    elif hasattr(block, "name"):
                        print(f"\n Tool Used: {block.name}")

            elif isinstance(message, ResultMessage):

                print("\n" + "=" * 80)
                print("FINAL RESPONSE")
                print("=" * 80)

                print(message.result)

                print("\nCompleted:", message.subtype)


asyncio.run(main())