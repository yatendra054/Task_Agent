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
    
def open_whatsapp_chat():
    subprocess.Popen(
        'explorer.exe shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App',
        shell=True
    )    
    
class LocalWorkFlow(TypedDict):
    user_input:str
    action:str
    path:str
    status:List[str]
    history:List[str]
    
    
def parse_intent(state:LocalWorkFlow):
    chain=local_prompt | llm
    response=chain.invoke({"user_input":state['user_input'],"history":state.get("history",[])})
    
    parse=json.loads(response.content)
    state["action"]=parse["action"]
    state["path"]=parse["path"]
    
    return state

def validate(state:LocalWorkFlow):
    allowed={
        "open_folder",
        "open_file",
        "open_vscode",
        "open_whatapp",
        "unknown"
    }
    
    if state["action"] not in allowed:
        raise Exception("This action is not allowed")
    
    return state


def execute(state:LocalWorkFlow):
    state["status"]=[]
    
    if state["action"] =="open_folder":
        openfoler(state["path"])
        state["status"].append(f"Open Folder name: {state["path"]}")
        
        
    elif state["action"] =="open_file":
        openfoler(state["path"])
        state["status"].append(f"Open File name: {state["path"]}")
        
        
    elif state["action"] =="vscode":
        openfoler(state["path"])
        state["status"].append(f"Open in Vscode: {state["path"]}")
        
    elif state["action"]=="open_whatapp":
        open_whatsapp_chat()
        state["status"].append("Whatapp is open")    
        
    elif state["action"]=="unknown":
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