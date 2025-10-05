"""
Onchain MCP Server

A Model Context Protocol server that provides tools for querying onchain data
including ETH balances and ERC20 token balances.
"""

import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from config import config

# Create the MCP server
mcp = FastMCP("onchain-mcp")

# Import and register tools
from tools.eth_balance import eth_balance_tool
from tools.erc20_balance import erc20_balance_tool
from tools.nft_balance import nft_balance_tool
from tools.tx_get import tx_get_tool
from tools.logs_query import logs_tool
from tools.token_metadata import token_metadata_tool
from tools.contract_audit import contract_audit_tool

# Import prompts
from prompts.contract_audit import (
    contract_security_audit_prompt,
    contract_quick_analysis_prompt,
    contract_deep_dive_prompt
)

# Register tools with the server
mcp.tool()(eth_balance_tool)
mcp.tool()(erc20_balance_tool)
mcp.tool()(nft_balance_tool)
mcp.tool()(tx_get_tool)
mcp.tool()(logs_tool)
mcp.tool()(token_metadata_tool)
mcp.tool()(contract_audit_tool)

# Register prompts with the server
mcp.prompt()(contract_security_audit_prompt)
mcp.prompt()(contract_quick_analysis_prompt)
mcp.prompt()(contract_deep_dive_prompt)

if __name__ == "__main__":
    # Run the server
    mcp.run()
