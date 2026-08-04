import os
import asyncio

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    ResultMessage,
    AssistantMessage
)
from dotenv import load_dotenv

load_dotenv()

os.environ["ANTHROPIC_API_KEY"] = os.getenv("CLAUDE_API_KEY")
claude_model_name = os.getenv("CLAUDE_MODEL_NAME")

async def main():

    options = ClaudeAgentOptions(
        model = claude_model_name,
        cwd=os.getcwd(),
        setting_sources=["project"],
        skills=["marketing-review"]
    )

    async for message in query(
        prompt="""
Review and improve this LinkedIn announcement.

"We're unbelievably excited to launch the most revolutionary AI smartwatch ever created! Buy now before you miss out forever!"
""",
        options=options,
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