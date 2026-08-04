<div align="center">

# Custom MCP Router

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Architecture: MCP-Replica](https://img.shields.io/badge/architecture-MCP%20Replica-orange.svg)]()

</div>

**Custom MCP Router** is a  Light weight drop-in replica of the core Model Context Protocol (MCP) server execution loop. It dynamically generates and reads JSON configurations to function as an autonomous tool registry for SuperAgents—while remaining fully accessible and remotely triggerable via high-performance HTTP endpoints specially designed for custom mcp servers and localized edge ai.

---


## 📂 Core Components & Implementation
1. Modular Tool Tracing (@trace_tool): use this decoratore over any function and track logs ,file path, arguments.
```python
@trace_tool
def add(a, b):
    """this is an arithmetic addition tool"""
    return a + b
```
---

2. Log Writing Utility (writelogs)
The system captures and writes out the active registry configurations dynamically using utility handlers like writelogs(toolregistry, filename) to keep the JSON schema synchronized:

```Python
writelogs(toolregistry, filename)
```
---

3. Centralized Tool Registry (config.json)
The system decouples tool execution logic from the application core by utilizing a structured JSON configuration registry. Each entry defines the module, absolute storage path, and arguments just like an mcp configuration.json :

```JSON
[
  {
    "name": "add",
    "description": "this is an arithmetic addition tool",
    "module": "additiontool.py",
    "path": "c:\\Users\\HIMADRI\\Desktop\\mas evaluation system\\environment",
    "arguments": [3, 2]
  },
  {
    "name": "web_mas",
    "description": "this is a web researcher tool",
    "module": "testmultiagentsystem.py",
    "path": "c:\\Users\\HIMADRI\\Desktop\\mas evaluation system\\environment",
    "arguments": ["tell me about tajmahal"]
  }
]
```
---

4. FastAPI Endpoint & Execution Engine (main.py)
The server dynamically manages file loading, runtime argument typing (type(args[i]).__name__), and execution loops:

GET /logfile: Ingests and serves the active config.json registry state.

POST /toolname: Evaluates targeted tool chunks, inspects parameter types, and structures the payload.

POST /executetool: Handles dynamic module imports at runtime and executes functions safely with unpacked arguments.

---

## 🏗️ Architectural Overview

```text
+---------------------+         HTTP / JSON Request         +-----------------------+
|  AI Agent / Client  | ----------------------------------> |     FastAPI Server    |
+---------------------+                                     +-----------------------+
                                                                        |
                                       +--------------------------------+--------------------------------+
                                       |                                |                                |
                                       v                                v                                v
                             [ GET /logfile ]                  [ POST /toolname ]              [ POST /executetool ]
                                       |                                |                                |
                                       v                                v                                v
                              Reads config.json                Validates Data Types            Dynamic Runtime Import
                            (Centralized Registry)             & Parameter Schemas             & Function Execution

```

---

##| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Health check & engine status verification |
| `/logfile` | `GET` | Retrieves active tool registry configurations |
| `/toolname` | `POST` | Resolves specific tool chunks and inspects argument data types |
| `/executetool` | `POST` | Triggers dynamic script execution and returns processed results |

---
## 💡 Dual Use Cases
Internal SuperAgent Tool Registry: Directly integrates into local agent loops as an MCP-style tool registry using dynamically generated JSON configurations.

External HTTP Protocol Access: Exposes a clean FastAPI wrapper (/logfile, /toolname, /executetool) allowing external clients and systems to discover, validate, and execute local tools via HTTP requests.

## 🛠️ Setup & Running Locally
Clone the repository:

```Bash
git clone [https://github.com/your-username/lightweight-claude-desktop-engine-protocol.git](https://github.com/your-username/lightweight-claude-desktop-engine-protocol.git)
cd lightweight-claude-desktop-engine-protocol
```

Install dependencies:

```Bash
pip install fastapi uvicorn pydantic
```

Run the server:

```Bash
uvicorn main:app --reload
```


---

## 🏁 Conclusion

The **Lightweight Claude Desktop Engine Protocol (LCDEP)** bridges the gap between complex multi-agent system orchestration and lightweight local execution. By replicating the core principles of the Model Context Protocol without heavy transport overhead, LCDEP empowers developers to build modular, self-registering, and deeply integrated tool ecosystems for SuperAgents.

---

## 👨‍💻 Creator & Maintainer

* **Created by:** Himadri
* **Project Focus:** Multi-Agent Systems (MAS), Agentic AI Workflows, and Local Execution Runtimes.



