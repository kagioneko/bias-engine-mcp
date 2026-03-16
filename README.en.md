# bias-engine-mcp

**Dynamic cognitive bias management for AI agents**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-server-purple)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🇯🇵 [日本語版 README はこちら](README.md)

---

## What is this?

This is **not** a tool to "make AI biased."

It gives agents **consistent, human-like reasoning tendencies** — the kind of cognitive patterns that make a character feel coherent across conversations.

```
User makes a strong argument
    ↓
High confirmation_bias state
    ↓
Agent prioritizes information that supports its existing interpretation
    ↓
Response reflects that reasoning tendency
```

Biases don't directly change text generation. They influence the **policy layer** that shapes how the agent reasons.

---

## Use Cases

- **VTuber AI** — different characters with distinct thinking styles
- **Game NPCs** — judgment patterns that shift based on situation
- **Cognitive layer** — combine with NeuroState for full internal state modeling

---

## Installation

```bash
pip install mcp pydantic
```

---

## Quick Start

```python
from core.bias_engine import BiasEngine

engine = BiasEngine()

# Stack a bias
engine.push("confirmation_bias", weight=0.7)
engine.push("negativity_bias", weight=0.3)

# Get current bias profile
profile = engine.get_profile()
print(profile)

# Generate policy influence
policy = engine.to_policy()
print(policy)  # {"openness": 0.3, "defensiveness": 0.7, ...}
```

---

## Built-in Bias Types

| Bias | Description |
|------|-------------|
| `confirmation_bias` | Prioritizes information supporting existing beliefs |
| `negativity_bias` | Weights negative information more heavily |
| `hostile_attribution_bias` | Interprets ambiguous actions as hostile |
| `optimism_bias` | Underestimates risk, overestimates positive outcomes |
| `authority_bias` | Defers to perceived authority figures |
| `recency_bias` | Weights recent information more heavily |

---

## Integration with NeuroState

When paired with [neurostate-engine](https://github.com/kagioneko/neurostate-engine), bias weights adjust automatically based on internal state:

```python
# High stress → confirmation_bias and hostile_attribution_bias rise
# High dopamine → optimism_bias rises
# Low serotonin → negativity_bias rises
```

---

## MCP Server

```bash
python3 bias_mcp/server.py
```

### Available Tools

| Tool | Description |
|------|-------------|
| `push_bias` | Add a bias to the stack |
| `pop_bias` | Remove a bias from the stack |
| `get_bias_profile` | Get current bias weights |
| `clear_biases` | Reset all biases |
| `sync_with_neurostate` | Auto-adjust biases from NeuroState values |

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "bias-engine": {
      "command": "python3",
      "args": ["/path/to/bias-engine-mcp/bias_mcp/server.py"]
    }
  }
}
```

---

## Related Projects

- [neurostate-engine](https://github.com/kagioneko/neurostate-engine) — Emotional state (pairs with BiasEngine)
- [cognitive-layer](https://github.com/kagioneko/cognitive-layer) — Integrates NeuroState + BiasEngine → policy
- [neurostate-sdk](https://github.com/kagioneko/neurostate-sdk) — Unified SDK for the full stack

---

## License

MIT © [Emilia Lab](https://kagioneko.com/emilia_lab/)
