import asyncio
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from web_surfer_agent import MultimodalWebSurfer
from typing import List
from autogen_agentchat.messages import  BaseChatMessage,TextMessage




# Define the state schema
class BrowserState(TypedDict):
    task: str
    status: str
    result: Dict[str, Any]
    scratch_pad: List[...]
    playwright_actions: List[...]
    error: str | None


async def feature_file_generation(state: BrowserState) -> BrowserState:
    
    state["task"] = """
    Feature: Registration Page Experience Selection

  Scenario: User selects Senior Level experience during registration
    Given the user navigates to "https://jovial-clafoutis-56d393.netlify.app/"
    When the user selects "Senior Level (6–10 years)" from the "Experience Level" dropdown
    Then the selected experience level should be "Senior Level (6–10 years)"

    """
    return state

# Single node to execute the full task
async def execute_task(state: BrowserState) -> BrowserState:
    # Initialize the web surfer
    web_surfer = MultimodalWebSurfer(
        name="MultimodalWebSurfer",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-2024-08-06"),
        headless=False,
        animate_actions=True,
        # to_save_screenshots=True,
        debug_dir="./screenshots",
        state=state
    )
    print(f"Executing task: {state['task'].strip()}...")
    try:
        stream =await web_surfer.on_messages(messages=[TextMessage(source="user",content=state["task"])],cancellation_token=None)
        print("These are the playwright actions")
        print(state["playwright_actions"])
        state["status"] = "completed"
        state["result"] = {"task_execution": "success"}
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
    return state

# Define the LangGraph workflow
def create_workflow():
    workflow = StateGraph(BrowserState)
    workflow.add_node("feature_file_node",feature_file_generation)
    workflow.add_node("execute_task", execute_task)
    workflow.add_edge("feature_file_node","execute_task")
    workflow.add_edge("execute_task", END)
    workflow.set_entry_point("feature_file_node")
    return workflow.compile()

# Main function
async def main() -> None:
    try:
        initial_state: BrowserState = {
            "task": "",
            "status": "initial",
            "result": {},
            "error": None,
            "scratch_pad": [],
            "playwright_actions": []
        }
        workflow = create_workflow()
        # Use astream if available, otherwise fall back to manual iteration
        try:
            async for state in workflow.astream(initial_state):
                print("Execution Done")
              
        except AttributeError:
            # Fallback for older versions or if astream is unavailable
            stream = workflow.stream(initial_state)
            while True:
                try:
                    state = await anext(stream)
                except StopAsyncIteration:
                    break
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())