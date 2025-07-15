import asyncio
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from web_surfer_agent import MultimodalWebSurfer

# Define the state schema
class BrowserState(TypedDict):
    task: str
    status: str
    result: Dict[str, Any]
    error: str | None

# Initialize the web surfer
web_surfer = MultimodalWebSurfer(
    name="MultimodalWebSurfer",
    model_client=OpenAIChatCompletionClient(model="gpt-4o-2024-08-06"),
    headless=False,
    animate_actions=True,
    to_save_screenshots=True,
    debug_dir="./screenshots"
)

# Single node to execute the full task
async def execute_task(state: BrowserState) -> BrowserState:
    print(f"Executing task: {state['task'].strip()}...")
    try:
        stream = web_surfer.run_stream(task=state["task"])
        await Console(stream)
        state["status"] = "completed"
        state["result"] = {"task_execution": "success"}
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
    return state

# Define the LangGraph workflow
def create_workflow():
    workflow = StateGraph(BrowserState)
    workflow.add_node("execute_task", execute_task)
    workflow.add_edge("execute_task", END)
    workflow.set_entry_point("execute_task")
    return workflow.compile()

# Main function
async def main() -> None:
    try:
        initial_state: BrowserState = {
            "task": """
            Open the registration page by navigating to https://jovial-clafoutis-56d393.netlify.app/
            From the Experience Level dropdown select Senior Level (6–10 years)
            """,
            "status": "initial",
            "result": {},
            "error": None
        }
        workflow = create_workflow()
        # Use astream if available, otherwise fall back to manual iteration
        try:
            async for state in workflow.astream(initial_state):
                print(f"Current state: {state}")
        except AttributeError:
            # Fallback for older versions or if astream is unavailable
            stream = workflow.stream(initial_state)
            while True:
                try:
                    state = await anext(stream)
                    print(f"Current state: {state}")
                except StopAsyncIteration:
                    break
    finally:
        await web_surfer.close()

if __name__ == "__main__":
    asyncio.run(main())