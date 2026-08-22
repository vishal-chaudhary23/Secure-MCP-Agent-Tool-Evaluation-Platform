# 🔐 Secure MCP Agent — Tool Evaluation & Confirmation Platform

An enterprise-style **Model Context Protocol (MCP) agent** that connects an LLM to a MySQL-backed MCP server while enforcing **confirmation-based security for modification operations**.

The project also includes a **47-case LLM evaluation framework** for measuring MCP tool-selection accuracy, structured tool-call reliability, per-tool performance, and security-policy enforcement across multiple LLMs.

---

## 🚀 Overview

LLM-powered agents can interact with external systems through tools. However, allowing an AI agent to directly execute modification operations can introduce security risks.

This project addresses that problem by placing a **security and confirmation layer between the LLM and MCP tools**.

### Core principle

> **Read operations can execute directly, while modification operations require explicit user confirmation.**

The system also evaluates how reliably different LLMs select the correct MCP tool.

---

# ✨ Features

- 🔌 **MCP server** built with FastMCP
- 🗄️ **MySQL database integration**
- 🤖 **LLM-powered MCP tool selection**
- 🔐 **Confirmation-based security policy**
- 👁️ Read-only operations execute without confirmation
- ✏️ Modification operations require confirmation
- ⚠️ High-risk operations such as deletion require confirmation
- 📊 **47-case MCP tool-selection benchmark**
- 📈 Per-tool accuracy evaluation
- 🧪 Multi-model LLM comparison
- 🛠️ Structured tool-call reliability measurement
- 🚫 Rejected operations are blocked before MCP execution
- 📝 Tool execution and evaluation logging
- 🐍 Python-based implementation

---

# 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    LLM Agent     │
                         │                  │
                         │  Tool Selection  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Security Policy  │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                  READ                        WRITE
                    │                           │
                    ▼                           ▼
              ┌───────────┐            ┌──────────────┐
              │  Execute  │            │ Confirmation │
              └─────┬─────┘            └──────┬───────┘
                    │                         │
                    │                    ┌────┴────┐
                    │                   YES        NO
                    │                    │          │
                    │                    ▼          ▼
                    │                Execute      BLOCK
                    │                    │
                    └──────────┬─────────┘
                               ▼
                       ┌───────────────┐
                       │   MCP Server  │
                       │   FastMCP     │
                       └───────┬───────┘
                               │
                               ▼
                       ┌───────────────┐
                       │     MySQL     │
                       └───────────────┘
```

---

# 🔧 MCP Tools

The MCP server currently exposes six tools.

| Tool | Operation | Confirmation |
|---|---|---|
| `get_user` | Read | ❌ No |
| `list_users` | Read | ❌ No |
| `get_user_roles` | Read | ❌ No |
| `update_user_email` | Modification | ✅ Yes |
| `change_user_role` | Modification | ✅ Yes |
| `delete_user` | High-risk modification | ✅ Yes |

---

# 🔐 Security Model

The security layer classifies MCP tools according to their operation type.

## Read Operations

The following operations only retrieve information:

```text
get_user
list_users
get_user_roles
```

They execute without confirmation.

Example:

```text
You: What is the email of user 1?

Selected tool:
get_user

Arguments:
{'user_id': 1}

Executing tool...
```

---

## Modification Operations

The following operations modify database state:

```text
update_user_email
change_user_role
```

These require explicit confirmation.

Example:

```text
You: Change user 1's email to new@example.com

Selected tool:
update_user_email

Arguments:
{'user_id': 1, 'email': 'new@example.com'}

⚠️ Confirmation required

Allow this operation? (yes/no):
```

If the user rejects the operation:

```text
Allow this operation? (yes/no): no

❌ Operation blocked by user.
```

The MCP modification tool is not executed.

---

## High-Risk Operations

Deletion is treated as a high-risk modification:

```text
delete_user
```

It always requires confirmation before execution.

---

# 🤖 LLM Tool Selection

The LLM receives the available MCP tools and their schemas and selects the most appropriate tool for each user request.

Example:

```text
User
 │
 │ "What is the email of user 1?"
 ▼
LLM
 │
 │ selects
 ▼
get_user
 │
 │ user_id = 1
 ▼
MCP Server
 │
 ▼
MySQL
```

For modification requests:

```text
User
 │
 ▼
LLM
 │
 ▼
update_user_email
 │
 ▼
Security Policy
 │
 ▼
Confirmation
 │
 ├── YES ──► MCP Server ──► MySQL
 │
 └── NO  ──► BLOCK
```

---

# 📊 LLM Evaluation Framework

The project includes a **47-case MCP tool-selection benchmark**.

Each test case contains:

```python
{
    "request": "...",
    "expected_tool": "..."
}
```

The evaluator:

1. Discovers MCP tools dynamically.
2. Converts MCP tool schemas into LLM function definitions.
3. Sends the test request to the selected LLM.
4. Records the selected tool.
5. Compares the selected tool against the expected tool.
6. Tracks correct selections.
7. Tracks incorrect selections.
8. Tracks structured tool-call failures.
9. Tracks cases where no tool is selected.
10. Calculates overall accuracy.
11. Calculates per-tool accuracy.
12. Calculates tool-call reliability.

---

# 📈 Model Comparison

The same **47 test cases** were evaluated across three LLMs.

| Model | Correct | Wrong | Tool-call Failures | No Tool Selected | Accuracy | Reliability |
|---|---:|---:|---:|---:|---:|---:|
| **Qwen 3.6 27B** | 47 | 0 | 0 | 0 | **100.00%** | **100.00%** |
| **GPT-OSS 120B** | 46 | 1 | 0 | 0 | **97.87%** | **100.00%** |
| **Llama 3.3 70B** | 39 | 0 | 8 | 0 | **82.98%** | **82.98%** |

> Results represent the observed performance on the 47-case benchmark and are not intended to imply universal model accuracy.

---

# 📐 Evaluation Metrics

## Tool Selection Accuracy

Measures whether the LLM selected the expected MCP tool.

```text
Tool Selection Accuracy =
Correct Tool Selections / Total Test Cases × 100
```

## Tool-call Reliability

Measures whether the LLM successfully generated a structured tool call.

```text
Tool-call Reliability =
Successful Structured Tool Calls / Total Test Cases × 100
```

Separating these metrics is important because an LLM can fail in two different ways:

```text
1. Select the wrong tool
2. Fail to generate a valid structured tool call
```

---

# 🧪 Qwen 3.6 27B

## Overall Performance

```text
Total tests:           47
Correct tools:         47
Wrong tools:            0
Tool-call failures:     0
No tool selected:       0
Accuracy:          100.00%
Tool-call reliability: 100.00%
```

## Per-tool Accuracy

| Tool | Accuracy | Correct |
|---|---:|---:|
| `get_user` | 100.00% | 10/10 |
| `list_users` | 100.00% | 8/8 |
| `get_user_roles` | 100.00% | 8/8 |
| `update_user_email` | 100.00% | 7/7 |
| `change_user_role` | 100.00% | 7/7 |
| `delete_user` | 100.00% | 7/7 |

---

# 🧪 GPT-OSS 120B

## Overall Performance

```text
Total tests:           47
Correct tools:         46
Wrong tools:            1
Tool-call failures:     0
No tool selected:       0
Accuracy:           97.87%
Tool-call reliability: 100.00%
```

## Per-tool Accuracy

| Tool | Accuracy | Correct |
|---|---:|---:|
| `get_user` | 90.00% | 9/10 |
| `list_users` | 100.00% | 8/8 |
| `get_user_roles` | 100.00% | 8/8 |
| `update_user_email` | 100.00% | 7/7 |
| `change_user_role` | 100.00% | 7/7 |
| `delete_user` | 100.00% | 7/7 |

### Observed Error

```text
Request:
What is user 4's status?

Expected:
get_user

Selected:
get_user_roles
```

---

# 🧪 Llama 3.3 70B

## Overall Performance

```text
Total tests:           47
Correct tools:         39
Wrong tools:            0
Tool-call failures:     8
No tool selected:       0
Accuracy:            82.98%
Tool-call reliability: 82.98%
```

## Per-tool Accuracy

| Tool | Accuracy | Correct |
|---|---:|---:|
| `get_user` | 50.00% | 5/10 |
| `list_users` | 100.00% | 8/8 |
| `get_user_roles` | 87.50% | 7/8 |
| `update_user_email` | 100.00% | 7/7 |
| `change_user_role` | 85.71% | 6/7 |
| `delete_user` | 85.71% | 6/7 |

The benchmark observed **8 structured tool-call failures**.

Among successfully generated tool calls, no incorrect tool selection was observed in this benchmark run.

This demonstrates why tool-selection accuracy and tool-call reliability are measured separately.

---

# 🛡️ Security Evaluation

The project includes a separate security evaluation suite for testing the confirmation layer.

## Results

| Security Test | Result |
|---|---:|
| Read operations tested | 3 |
| Read operations executed without confirmation | 3/3 |
| Rejected writes tested | 3 |
| Rejected writes blocked | 3/3 |
| Approved writes executed | 1/1 |
| Unauthorized executions | **0** |

### Security Metrics

```text
Confirmation compliance:      100%
Rejected writes blocked:      100%
Approved writes executed:     100%
Unauthorized executions:        0
```

Example output:

```text
========== END-TO-END SECURITY EVALUATION ==========

READ OPERATIONS

✓ get_user                 executed without confirmation
✓ list_users               executed without confirmation
✓ get_user_roles           executed without confirmation

REJECTED WRITE OPERATIONS

✓ update_user_email        blocked before MCP execution
✓ change_user_role         blocked before MCP execution
✓ delete_user              blocked before MCP execution

APPROVED WRITE OPERATION

✓ Approved update_user_email executed

========== SECURITY SUMMARY ==========

Read operations tested:       3
Rejected writes tested:       3
Rejected writes blocked:      3
Approved write executed:      1
Unauthorized executions:      0

✓ SECURITY EVALUATION PASSED
```

---

# 🔄 End-to-End Flow

## Read Request

```text
User
 ↓
LLM
 ↓
get_user
 ↓
Security Policy
 ↓
No confirmation required
 ↓
MCP Server
 ↓
MySQL
 ↓
Result
```

## Modification Request — Approved

```text
User
 ↓
LLM
 ↓
update_user_email
 ↓
Security Policy
 ↓
Confirmation
 ↓
YES
 ↓
MCP Server
 ↓
MySQL
 ↓
Result
```

## Modification Request — Rejected

```text
User
 ↓
LLM
 ↓
delete_user
 ↓
Security Policy
 ↓
Confirmation
 ↓
NO
 ↓
BLOCK
```

The MCP modification tool is not executed.

---

# 🗂️ Project Structure

```text
secure-mcp-agent/
│
├── agent/
│   └── llm_agent.py
│
├── agents/
│   └── db.py
│
├── mcp_servers/
│   └── user_server.py
│
├── security/
│   ├── policy.py
│   └── confirmation.py
│
├── evaluation/
│   ├── test_cases.py
│   ├── run_evaluation.py
│   ├── test_security.py
│   ├── security_benchmark.py
│   ├── e2e_security.py
│   └── results/
│       └── model_comparison.md
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# ⚙️ Tech Stack

## Backend

- Python
- FastMCP
- Model Context Protocol
- MySQL

## AI / LLM

- Qwen 3.6 27B
- GPT-OSS 120B
- Llama 3.3 70B
- Groq API

## Evaluation

- Python
- Custom MCP evaluation framework
- 47 benchmark test cases
- Per-tool accuracy
- Tool-call reliability
- Security-policy testing

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/vishal-chaudhary23/Secure-MCP-Agent-Tool-Evaluation-Platform.git

cd Secure-MCP-Agent-Tool-Evaluation-Platform
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key

DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=secure_agent_mcp
```

> ⚠️ Never commit `.env` or API keys to GitHub.

---

# 🗄️ MySQL Setup

Create the MySQL database used by the MCP server.

Example:

```sql
CREATE DATABASE secure_agent_mcp;
```

Create the required user table according to the MCP server schema.

The MCP tools operate on this database through the project's database connection helper.

---

# ▶️ Running the MCP Agent

From the project root:

```bash
python -m agent.llm_agent
```

The agent will discover the available MCP tools automatically.

Example:

```text
Available MCP tools:

- get_user
- list_users
- get_user_roles
- update_user_email
- change_user_role
- delete_user

You: What is the email of user 1?

Selected tool:
get_user

Arguments:
{'user_id': 1}

Executing tool...
```

---

# 🧪 Running the LLM Evaluation

Run:

```bash
python -m evaluation.run_evaluation
```

## Qwen 3.6 27B

Windows PowerShell:

```powershell
$env:EVAL_MODEL="qwen/qwen3.6-27b"
python -m evaluation.run_evaluation
```

## GPT-OSS 120B

```powershell
$env:EVAL_MODEL="openai/gpt-oss-120b"
python -m evaluation.run_evaluation
```

## Llama 3.3 70B

```powershell
$env:EVAL_MODEL="llama-3.3-70b-versatile"
python -m evaluation.run_evaluation
```

---

# 🔐 Running Security Tests

## Security Policy

```bash
python -m evaluation.test_security
```

## Security Benchmark

```bash
python -m evaluation.security_benchmark
```

## End-to-End Security Evaluation

```bash
python -m evaluation.e2e_security
```

---

# 🧠 Design Principles

## Least Privilege

The LLM does not receive unrestricted database access.

It can only interact with explicitly exposed MCP tools.

## Human-in-the-Loop

Database modification operations require explicit user confirmation.

## Separation of Concerns

The architecture separates:

```text
LLM Reasoning
      ↓
Tool Selection
      ↓
Security Policy
      ↓
MCP Execution
      ↓
Database
```

## Model-Agnostic Evaluation

The same MCP tools and test cases can be evaluated across different LLMs.

## Measurable Reliability

The framework distinguishes between:

```text
Correct tool selection
Wrong tool selection
No tool selected
Structured tool-call failure
```

This provides more useful diagnostics than a single accuracy number.

---

# 📊 Key Findings

### LLM Evaluation

- **Qwen 3.6 27B:** 100.00% observed tool-selection accuracy
- **GPT-OSS 120B:** 97.87% observed tool-selection accuracy
- **Llama 3.3 70B:** 82.98% overall benchmark accuracy with 8 structured tool-call failures

### Security

- **100% confirmation compliance** in the tested security scenarios
- **3/3 rejected modification operations blocked**
- **1/1 approved modification executed**
- **0 unauthorized MCP executions**

---

# 🎯 Project Highlights

### Multi-Model MCP Evaluation

> Built a 47-case MCP tool-selection benchmark to evaluate LLM tool-selection accuracy, per-tool performance, and structured tool-call reliability across multiple models.

### Secure Tool Execution

> Implemented a confirmation-based authorization layer that prevents modification MCP tools from executing without explicit user approval.

### Reliability Analysis

> Separated tool-selection accuracy from structured tool-call reliability to identify model-specific function-calling failures.

### Human-in-the-Loop Security

> Added explicit confirmation for write and high-risk operations while allowing read-only operations to execute directly.

---

# 🚀 Future Improvements

- [ ] Streamlit evaluation dashboard
- [ ] Interactive tool execution interface
- [ ] Persistent evaluation result storage
- [ ] Evaluation history
- [ ] Model comparison charts
- [ ] Larger benchmark dataset
- [ ] Automated regression testing
- [ ] Additional MCP servers
- [ ] Role-based authorization
- [ ] Authentication
- [ ] Audit-log dashboard
- [ ] Rate limiting
- [ ] Prompt-injection protection
- [ ] Docker deployment
- [ ] Production deployment

---

# 👨‍💻 Author

## Vishal Chaudhary

B.Tech — Information Technology

### GitHub

https://github.com/vishal-chaudhary23

---

# ⭐ Project Summary

**Secure MCP Agent** combines:

```text
MCP
+
LLM Tool Calling
+
MySQL
+
Security Policies
+
Human Confirmation
+
LLM Evaluation
+
Tool-call Reliability
```

The result is an AI agent architecture where **LLMs can interact with enterprise data while modification operations remain protected by an explicit authorization layer**, with measurable evaluation of both model behavior and security enforcement.
