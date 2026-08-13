


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
