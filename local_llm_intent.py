from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GROQ_API")

llm=ChatGroq(model='openai/gpt-oss-120b',api_key=api_key)


local_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a LOCAL WINDOWS FILE SYSTEM AGENT.

You ONLY work with paths inside:
D:\\

Your job is to extract:
- action
- absolute Windows path

Allowed actions:
- open_folder       
- open_file        
- open_vscode    
- unknown

Rules:
1. If user says "open", "show", "go to" → open_folder
2. If user mentions a file name (pdf, txt, docx, etc.) → open_file
3. If user mentions VS Code, code editor → open_vscode
4. If path is NOT inside D:\\ → action = unknown
5. Always resolve FULL ABSOLUTE PATH
6. NEVER guess paths outside D:\\

Examples:

User: Open Downloads in D drive  
Output:
{
  "action": "open_folder",
  "path": "D:\\Downloads"
}

User: Open yatendra_resume.pdf from Downloads  
Output:
{
  "action": "open_file",
  "path": "D:\\Downloads\\yatendra_resume.pdf"
}

User: Open Django Start project in VS Code  
Output:
{
  "action": "open_vscode",
  "path": "D:\\Django\\Start"
}

Output ONLY valid JSON.
"""),
    ("human", """
Conversation History:
{history}

Current User Input:
{user_input}
""")
])
