# Lightweight-Claude-Desktop-Engine-Protocol-LCDEP-
**Lightweight Claude Desktop Engine Protocol (LCDEP)** is a drop-in replica of the core Model Context Protocol (MCP) server execution loop. It dynamically generates and reads JSON configurations to function as an autonomous tool registry for SuperAgents—while remaining fully accessible and remotely triggerable via high-performance HTTP endpoints.

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
## 📂 Core Components & Implementation
1. Modular Tool Tracing (@trace_tool): use this decoratore over any function and track logs ,file path, arguments.
```python
@trace_tool
def add(a, b):
    """this is an arithmetic addition tool"""
    return a + b
```
2. Log Writing Utility (writelogs)
The system captures and writes out the active registry configurations dynamically using utility handlers like writelogs(toolregistry, filename) to keep the JSON schema synchronized:

```Python
writelogs(toolregistry, filename)
```
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
4. FastAPI Endpoint & Execution Engine (main.py)
The server dynamically manages file loading, runtime argument typing (type(args[i]).__name__), and execution loops:

GET /logfile: Ingests and serves the active config.json registry state.

POST /toolname: Evaluates targeted tool chunks, inspects parameter types, and structures the payload.

POST /executetool: Handles dynamic module imports at runtime and executes functions safely with unpacked arguments.



## ⚖️ Architecture Comparison: Claude Desktop vs. LCDEP

Here is the short and crisp architecture similarity comparison:

| Feature | Claude Desktop MCP Server | LCDEP (Your Architecture) |
| --- | --- | --- |
| **Configuration-Driven Discovery** | Uses local JSON configs to discover and map external tool servers. | Uses a centralized `config.json` registry to dynamically map local modules, paths, and arguments. |
| **Modular Isolation** | Runs independent local processes/scripts to keep tools decoupled from the core app. | Keeps each tool isolated in modular Python files (`.py`) for clean runtime imports. |
| **Standardized Protocol** | Uses standardized transport protocols (JSON-RPC) for client-server communication. | Uses a FastAPI-driven protocol (`/logfile`, `/toolname`, `/executetool`) for validation and execution. |
| **Ecosystem Agonistic** |Tied to Claude ecosystem | Open & universal—bridges OpenAI, Gemini, or custom multi-agent workflows |




