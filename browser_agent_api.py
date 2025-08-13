from fastapi import FastAPI, HTTPException
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import Dict, Any
from pydantic import BaseModel
import os
import sqlite3
from langgraph.types import interrupt,Command
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the State schema
class State(Dict[str, Any]):
    jira_key: str = ""
    feature_file: str = ""
    status: str = ""
    approved: bool = False

# Pydantic models for request validation
class WorkflowInput(BaseModel):
    thread_id: str = ""

class ResumeInput(BaseModel):
    thread_id: str
    approved: bool = True
    feature_file: str

# Define node functions
def get_jira_key(state: State) -> State:
    state["status"] = "Jira key fetched"
    return state

def get_feature_file(state: State) -> State:
    state["feature_file"] = f"feature_{state['jira_key']}.txt"
    state["status"] = "Feature file retrieved"
    return state

def human_in_loop(state: State) -> State:
    if not state["approved"]:
        human_input = interrupt("Needs Approval Brother")  # <— on resume, returns your dict
        # merge the human_input into state explicitly
        state["approved"] = human_input.get("approved", state.get("approved", False))
        if "feature_file" in human_input:
            state["feature_file"] = human_input["feature_file"]
        state["status"] = "Manually approved" if state["approved"] else "Approval denied"
    
    return state
    


def execute_task(state: State) -> State:
    state["status"] = f"Task executed for {state['feature_file']}"
    return state

# Define the workflow
workflow = StateGraph(State)
workflow.add_node("jira_node", get_jira_key)
workflow.add_node("feature_node", get_feature_file)
workflow.add_node("execute_task", execute_task)
workflow.add_node("human_in_loop", human_in_loop)
workflow.add_edge("jira_node", "feature_node")
workflow.add_edge("feature_node", "human_in_loop")
workflow.add_edge("human_in_loop", "execute_task")
workflow.add_edge("execute_task", END)
workflow.set_entry_point("jira_node")

# Initialize checkpointer and compile graph once at startup
checkpointer = SqliteSaver(sqlite3.connect("checkpointer.db", check_same_thread=False))
graph = workflow.compile(checkpointer=checkpointer)

@app.get("/get-userId")
async def get_userId():
    thread_id =f"user-{os.urandom(3).hex()}"
    return {"userId": thread_id}

@app.post("/start-workflow/user/{user_id}/jira/{jira_key}")
async def start_workflow(user_id: str,jira_key: str):
    # Convert Pydantic model to dict for LangGraph
    initial_state= {
        "jira_key": jira_key,
        "feature_file":"",
        "status": "",
        "approved": False
    }
    
    config = {"configurable": {"thread_id": user_id}}
    
    try:
        # Run the workflow until human review
        result = graph.invoke(initial_state, config=config)
        return {"feature_file": result["feature_file"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {str(e)}")

@app.put("/resume-workflow")
async def resume_workflow(input: ResumeInput):
    config = {"configurable": {"thread_id": input.thread_id}}
    print("This is the input which I have got")
    print(input)
    # Get the current state
    checkpoint = graph.get_state(config)
    if not checkpoint:
        raise HTTPException(status_code=404, detail=f"No checkpoint found for thread_id: {input.thread_id}")
    
    # current_state = checkpoint.values
    # # Update state with human input
    # current_state["approved"] = input.approved
    # current_state["feature_file"] = input.feature_file
    # current_state["status"] = "Manually approved" if input.approved else "Approval denied"
    # print("This is the Current State")
    # print(current_state)
    try:
        # Resume execution
        result = graph.invoke(
            Command(
                resume={
                    "approved": input.approved,
                    "feature_file": input.feature_file,
                    "status": "Manually approved" if input.approved else "Approval denied",
                }
            ),
            config=config,
        )
        return {"state": result, "thread_id": input.thread_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume failed: {str(e)}")

@app.on_event("shutdown")
def shutdown_event():
    # Close the SQLite connection when the app shuts down
    if hasattr(checkpointer, 'conn'):
        checkpointer.conn.close()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)