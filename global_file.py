import subprocess
from typing import TypedDict, List
from langgraph.graph import END,StateGraph
from path import PATHS
from llm_intent import llm , llm_prompt
import urllib
import json

def open_whatsapp_chat():
    subprocess.Popen(
        'explorer.exe shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App',
        shell=True
    )

def open_chrome_youtube_search(query:str):
    search_query = urllib.parse.quote(query)
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"

    subprocess.Popen([PATHS["CHROME_PATH"], youtube_url])
    
def open_chorme(query:str):
    search=urllib.parse.quote(query)
    chrome_url=f"https://www.google.com/search?q={search}"
    
    subprocess.Popen([PATHS["CHROME_PATH"], chrome_url])        


class WorkflowState(TypedDict):
    user_input: str
    query:str
    action:str
    status: List[str]
    history: List[str]
    
def parse_intent(state: WorkflowState):
    chain=llm_prompt | llm
    
    response=chain.invoke({"user_input":state['user_input'], "history":state.get("history",[])})
    
    parsed=json.loads(response.content)
    
    state["action"]=parsed["action"]
    state["query"]=parsed["query"]
    
    return state


def validate_steps(state: WorkflowState):
    allowed = {
        "open_whatapp",
        "open_chrome",
        "open_youtube",
        "chat",
        "unknown"
    }
    
    if state["action"] not in allowed:
        raise Exception("This action is not allowed")
    return state

def execute_steps(state: WorkflowState):
    state["status"] = []
            
    if state["action"] == "open_youtube":
        open_chrome_youtube_search(state["query"])
        state["status"].append(f"YouTube opened video: {state['query']} ")
        
    elif state["action"] == "open_chrome":
        open_chorme(state["query"])
        state["status"].append(f"Chrome opened with search result: {state['query']}")   
    
    elif state["action"]=="open_whatapp":
        open_whatsapp_chat()
        state["status"].append("Whatapp is open")
        
    elif state["action"] == "chat":
        response = llm.invoke(state["query"])
        state["status"].append(response.content)

    elif state["action"] == "unknown":
        state["status"].append("I didn’t understand. You can chat or give a command.")
            
    return state



graph = StateGraph(WorkflowState)

graph.add_node("parse_intent", parse_intent)
graph.add_node("validate", validate_steps)
graph.add_node("execute", execute_steps)

graph.set_entry_point("parse_intent")
graph.add_edge("parse_intent", "validate")
graph.add_edge("validate", "execute")
graph.add_edge("execute",END)

global_flow = graph.compile()

