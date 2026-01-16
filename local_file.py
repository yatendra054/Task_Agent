import os
import subprocess
from langgraph.graph import StateGraph,END
from path import PATHS
from local_llm_intent import llm,local_prompt
from typing import TypedDict,List
import os
import json


def openfoler(path:str):
    subprocess.Popen(['explorer',path])
    
def openfile(path:str):
    os.startfile(path)
    
def openvs(path:str):
    subprocess.Popen([PATHS["vscode"],path])
    
class LocalWorkFlow(TypedDict):
    user_input:str
    action:str
    path:str
    status:List[str]
    history:List[str]
    
    
def parse_intent(state:LocalWorkFlow):
    chain=llm | local_prompt
    response=chain.invoke({"user_input":state['user_input'],"history":state.get("history",[])})
    
    parse=json.load(response.content)
    state["action"]=parse["action"]
    state["path"]=parse["path"]
    
    return state

def validate(state:LocalWorkFlow):
    allowed={
        "open_folder",
        "open_file",
        "open_vscode",
        "unknown"
    }
    
    if state["action"] not in allowed:
        raise Exception("This action is not allowed")
    
    return state


def execute(state:LocalWorkFlow):
    state["status"]=[]
    
    if state["status"] =="open_folder":
        openfoler(state["path"])
        state["status"].append(f"Open Folder name: {state["path"]}")
        
        
    elif state["status"] =="open_file":
        openfoler(state["path"])
        state["status"].append(f"Open File name: {state["path"]}")
        
        
    elif state["status"] =="vscode":
        openfoler(state["path"])
        state["status"].append(f"Open in Vscode: {state["path"]}")
        
    elif state["status"]=="unknown":
        state["status"].append(f"Cannot not understand this command.")       
        
        
    return state

       
        
          
graph=StateGraph(LocalWorkFlow)

graph.add_node("parse_intent", parse_intent)
graph.add_node("validate", validate)
graph.add_node("execute", execute)

graph.set_entry_point("parse_intent")
graph.add_edge("parse_intent", "validate")
graph.add_edge("validate", "execute")
graph.add_edge("execute",END)

local_flow=graph.compile()