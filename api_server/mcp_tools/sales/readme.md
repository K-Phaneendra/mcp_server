# schema.json
This prevents agents from touching unknown columns.

# server.py
This is the only function agents ever call.

# executor.py
Validation + execution

# manifest.json
what agents load

# payload received from agent
```
{
  "metrics": ["total_sales"],
  "dimensions": ["product"],
  "filters": {"country": "Germany"},
  "time_range": {
    "start": "2025-12-01",
    "end": "2025-12-31"
  }
}
```

This MCP server exposes capabilities over sales data, not answers or queries — making it reusable in any agentic system.
