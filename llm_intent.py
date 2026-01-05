from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GROQ_API")

llm=ChatGroq(model='openai/gpt-oss-120b',api_key=api_key)


llm_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an intent extraction agent with memory.

You can see previous conversation.
Use it to resolve references like:
- it
- that
- same thing

Allowed actions:
- open_whatapp
- open_chrome
- open_youtube
- chat
- unknown

Rules:
- If the user is just talking, asking questions, or chatting → action = chat
- If the intent is unclear → action = unknown
- For chat, query can be the full user message

Output ONLY valid JSON.

JSON format:
{{
  "action": "<action_name>",
  "query": "<extracted_query>"
}}
"""),
    ("human", """
Conversation History:
{history}

Current User Input:
{user_input}
""")
])
