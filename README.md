# AI Automation Agent (Local & Chrome Agent)

A **natural-language-driven automation system** that lets you control **local system tasks** and **web (Chrome) tasks** using simple human language.  
Built with **Streamlit**, **LangGraph**, **LangChain**, and **Groq LLM API**.

---

## Features

### Local Agent
- Open folders from **any drive** (C, D, F, etc.)
- Open files (PDF, TXT, DOCX, images, etc.)
- Open projects/folders directly in **VS Code**
- Open **WhatsApp Desktop**
- Supports **hierarchical folder navigation** (step-by-step order)

### Chrome Agent
- Open Chrome with Google search
- Search and play YouTube videos
- Perform general browser-based tasks

---

## Architecture & Flow

The app uses a **router agent** to decide which workflow to run:

- **Local Agent** → local OS actions  
- **Chrome Agent** → browser actions  

Each agent follows a **LangGraph workflow**:
1. Parse intent using LLM
2. Validate allowed action
3. Execute task
4. End workflow

---

## Instructions (Must Read)

### 1. Local Agent Usage
- Handles **local system operations**
- Works with **any drive** (C, D, F, etc.)
- To open a project in **VS Code**, ensure the VS Code path is correctly set in `path.py`

### 2. Use Exact Names
- Folder and file names must match **exactly** as they exist on your system
- Correct **spelling**, **capitalization**, and **order** are required

### 3.Hierarchical Folder Navigation
- When opening **deeply nested folders or files**, always specify the folder order clearly
- The hierarchy must follow the **exact directory structure** on your system

#### Open Folder Example
```text
Open Folder_name folder inside C drive in order
1. Users
2. Next_name
3. OneDrive
4. Pictures
5. Folder_name
```

C -> Users -> Next_name -> OneDrive -> Pictures -> Folder_name


## Path Configuration (IMPORTANT)

Update `path.py` with the correct executable paths for Chrome and VS Code.  
Ensure these paths match your system, otherwise related actions may fail.

```python
PATHS = {
  "CHROME_PATH": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
  "vscode": r"C:\Users\Your_name\AppData\Local\Programs\Microsoft VS Code\Code.exe"
}

```

## Technologies Used

- **Frontend**: Streamlit  
- **Agent Orchestration**: LangGraph  
- **LLM Framework**: LangChain  
- **LLM Provider**: Groq API  
- **OS Automation**: Python (`os`, `subprocess`)  
- **Env Management**: .env`

---

## Setup & Installation

```bash
pip install streamlit langgraph langchain langchain-groq python-dotenv
```


