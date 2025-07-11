import asyncio
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from web_surfer_agent import MultimodalWebSurfer

async def main() -> None:
    web_surfer = MultimodalWebSurfer(
        name="MultimodalWebSurfer",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-2024-08-06"),
        headless=False,
        animate_actions=True,
        to_save_screenshots=True,
        debug_dir="./screenshots"
        # page_script_path="web_surfer_agent/page_script.js",
    )

    team = RoundRobinGroupChat([web_surfer], max_turns=3)
    stream = team.run_stream(task="Navigate to the Github login page and wait for user to enter his details and login and mention all repositories present in his github ")
    await Console(stream)
    await web_surfer.close()

asyncio.run(main())
