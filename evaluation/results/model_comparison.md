# MCP Agent Evaluation Results

## Benchmark Configuration

- Test cases: 47
- Evaluation type: MCP tool selection
- Tools evaluated: 6
- Models evaluated: Qwen 3.6 27B, GPT-OSS 120B, Llama 3.3 70B

---

## Model Comparison

| Model | Correct | Wrong | Tool-call Failures | No Tool Selected | Accuracy | Reliability |
|---|---:|---:|---:|---:|---:|---:|
| Qwen 3.6 27B | 47 | 0 | 0 | 0 | **100.00%** | **100.00%** |
| GPT-OSS 120B | 46 | 1 | 0 | 0 | **97.87%** | **100.00%** |
| Llama 3.3 70B | 39 | 0 | 8 | 0 | **82.98%** | **82.98%** |

---

## Qwen 3.6 27B

### Overall

- Correct tools: 47/47
- Accuracy: **100.00%**
- Tool-call reliability: **100.00%**

### Per-tool accuracy

| Tool | Accuracy |
|---|---:|
| `get_user` | 100% |
| `list_users` | 100% |
| `get_user_roles` | 100% |
| `update_user_email` | 100% |
| `change_user_role` | 100% |
| `delete_user` | 100% |

---

## GPT-OSS 120B

### Overall

- Correct tools: 46/47
- Accuracy: **97.87%**
- Tool-call reliability: **100.00%**

### Error

```text
Request:
What is user 4's status?

Expected:
get_user

Selected:
get_user_roles