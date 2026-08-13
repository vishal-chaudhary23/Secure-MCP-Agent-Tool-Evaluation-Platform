
# 🔐 Secure MCP Agent — Tool Evaluation & Confirmation Platform

An enterprise-style **Model Context Protocol (MCP) agent** that connects an LLM to a MySQL-backed MCP server while enforcing **confirmation-based security for modification operations**.

The project also includes a **47-case evaluation framework** for measuring LLM MCP tool-selection accuracy, structured tool-call reliability, per-tool performance, and security-policy enforcement across multiple LLMs.

---

## 🚀 Overview

Modern AI agents can interact with external systems through tools. However, allowing an LLM to directly execute modification operations introduces security risks.

This project addresses that problem by introducing a security layer between the LLM and MCP tools.

### Core principle

> **Read operations can execute directly, while modification operations require explicit user confirmation.**

The system also evaluates how reliably different LLMs select the correct MCP tool.

---

## ✨ Key Features

- 🔌 **MCP server** built with FastMCP
- 🗄️ **MySQL-backed tools**
- 🤖 **LLM-powered MCP tool selection**
- 🔐 **Confirmation-based security policy**
- 👁️ Read-only operations execute without confirmation
- ✏️ Modification operations require confirmation
- ⚠️ High-risk operations such as deletion require confirmation
- 📊 **47-case MCP tool-selection benchmark**
- 🧪 Per-tool accuracy evaluation
- 📈 Multi-model comparison
- 🛠️ Structured tool-call reliability measurement
- 🚫 Rejected operations are blocked before MCP execution
- 📝 Execution and evaluation logging
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
                         │ Tool Selection   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Security       │
                         │     Policy       │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                  READ                        WRITE
                    │                           │
                    ▼                           ▼
              ┌───────────┐            ┌──────────────┐
              │  Execute  │            │ Confirmation  │
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

```markdown
## Evaluation

The platform includes a 47-case MCP tool-selection benchmark and a security evaluation suite.

### LLM Tool Selection

| Model | Accuracy | Tool-call Reliability |
|---|---:|---:|
| Qwen 3.6 27B | **100.00%** | **100.00%** |
| GPT-OSS 120B | **97.87%** | **100.00%** |
| Llama 3.3 70B | **82.98%** | **82.98%** |

### Security Evaluation

- Confirmation compliance: **100%**
- Rejected writes blocked: **3/3**
- Approved writes executed: **1/1**
- Unauthorized executions: **0**

The evaluation framework measures both LLM-specific MCP tool-selection behavior and security-policy enforcement before tool execution.
