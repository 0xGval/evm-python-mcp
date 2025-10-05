# Prompts for Onchain MCP Server

This directory contains prompt templates for various blockchain analysis tasks.

## Structure

```
prompts/
├── __init__.py
├── contract_audit.py    # Contract analysis prompts
├── token_analysis.py    # Token research prompts (future)
├── defi_analysis.py     # DeFi protocol prompts (future)
└── README.md           # This file
```

## Usage

### Contract Audit Prompts

The contract audit tool now supports multiple output formats:

#### 1. Raw Data (Default)
```python
result = contract_audit_tool(address, network, format="raw")
# Returns: Raw JSON data
```

#### 2. Security Audit Prompt
```python
result = contract_audit_tool(address, network, format="audit")
# Returns: Structured security audit prompt
```

#### 3. Quick Analysis Prompt
```python
result = contract_audit_tool(address, network, format="quick")
# Returns: Quick assessment prompt
```

#### 4. Deep Dive Prompt
```python
result = contract_audit_tool(address, network, format="deep")
# Returns: Comprehensive analysis prompt
```

## Prompt Response Format

When using prompt formats, the response includes:

```json
{
  "prompt": "Formatted prompt template with data filled in",
  "context": { /* Raw audit data */ },
  "format_type": "audit|quick|deep",
  "address": "0x...",
  "network": "base",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Adding New Prompts

1. Create a new prompt file in this directory
2. Define prompt functions that return formatted strings
3. Import and register in `server.py`
4. Update tools to use the new prompts

Example:
```python
# prompts/token_analysis.py
def token_research_prompt():
    return "Research this token: {address} on {network}..."

# server.py
from prompts.token_analysis import token_research_prompt
mcp.prompt()(token_research_prompt)
```
