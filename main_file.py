import streamlit as st
from project import app  
st.set_page_config(
    page_title="AI Task Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Automation Agent")
st.caption("Control apps using natural language")

if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Enter your task (e.g. open dhurander trailer on youtube)")

if user_input:
    if user_input.lower() in {"stop", "quit", "exit"}:
        st.warning("Session stopped")
        st.stop()


    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Agent is thinking..."):
            try:
                result = app.invoke({"user_input": user_input,"history":st.session_state.messages})

                action = result.get("action", "unknown")
                query = result.get("query", "")
                status = result.get("status", [])

                response_text = f"""
**🧠 Intent Detected**
- **Action:** `{action}`
- **Query:** `{query}`

**⚙️ Execution Status**
"""
                for s in status:
                    response_text += f"- ✅ {s}\n"

            except Exception as e:
                response_text = f"❌ **Error:** {str(e)}"

        st.markdown(response_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })
