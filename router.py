from global_file import global_flow
from local_file import local_flow

def router_agent(agent_type: str, payload: dict):
    if agent_type=="local":
        return local_flow.invoke(payload)
    else:
        return global_flow.invoke(payload)
