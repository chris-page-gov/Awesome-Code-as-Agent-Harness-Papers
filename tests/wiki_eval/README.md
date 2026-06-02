# LLM-Wiki Evaluation Fixtures

This directory stores reusable test scenarios for the LLM-Wiki pattern.

The current suite checks whether generated Claim Cards cover the three
evaluation examples used in the primary-source evaluation:

- MCP governance.
- Agent safety and sandboxing.
- Evidence, observability, and redress.

Run:

```bash
python3 tools/evaluate_llm_wiki.py --write-report
```
