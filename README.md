# Onchain MCP Server

A comprehensive Model Context Protocol (MCP) server that provides tools for querying onchain data across multiple blockchain networks. This server supports 12+ blockchain networks and provides tools for ETH balances, ERC20 token balances, NFT balances, transaction analysis, and contract auditing.

## Features

### 🔗 Multi-Chain Support
- **Ethereum** (Mainnet, Sepolia)
- **Polygon**
- **Arbitrum**
- **Optimism**
- **BSC (Binance Smart Chain)**
- **Avalanche**
- **Base**
- **Scroll**
- **Blast**
- **Hyperliquid**
- **Plasma**

### 🛠️ Available Tools

1. **ETH Balance Tool** - Get native token balances
2. **ERC20 Balance Tool** - Token balance queries
3. **NFT Balance Tool** - ERC721/ERC1155 NFT balances
4. **Transaction Fetcher** - Detailed transaction analysis with ERC-20 transfer detection
5. **Logs Query Tool** - Event log analysis
6. **Token Metadata Tool** - Token information and metadata
7. **Contract Audit Tool** - Comprehensive contract analysis and security auditing

### 📋 Available Prompts

1. **Contract Security Audit** - AI-powered security analysis
2. **Quick Analysis** - Fast contract overview
3. **Deep Dive Analysis** - Comprehensive contract examination

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/0xGval/onchain-mcp.git
   cd onchain-mcp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   ```bash
   cp config_example.py config.py
   # Edit config.py with your API keys
   ```

## Configuration

### Required API Keys

- **Alchemy API Key** - For RPC endpoints
- **Etherscan API Key** - For contract verification and source code

### Environment Variables

Set your API keys as environment variables:

```bash
export ETHERSCAN_API_KEY="your_etherscan_api_key"
```

Or add them directly to `config.py`:

```python
"etherscan_api_key": "your_etherscan_api_key"
```

## Usage

### Running the Server

```bash
python server.py
```

### Using with Claude Desktop

To use this MCP server with Claude Desktop, you need to configure it in your Claude Desktop settings:

1. **Open Claude Desktop Settings**
2. **Go to "Developers" tab**
3. **Add a new MCP server** with these settings:

```json
{
  "mcpServers": {
    "onchain-mcp": {
      "command": "python",
      "args": ["path/to/your/onchain-mcp/server.py"],
      "env": {
        "ETHERSCAN_API_KEY": "your_etherscan_api_key"
      }
    }
  }
}
```

4. **Replace the path** with your actual server.py location
5. **Add your API keys** to the environment variables
6. **Restart Claude Desktop**

### Using with Other MCP Clients

The server provides tools that can be used with MCP-compatible clients like Cursor, or other MCP clients. The server exposes these tools via the MCP protocol.

### How to Use the Tools with Claude

Once configured, you can use the tools directly in your conversations with Claude:

**Example Prompts:**
- "Get the ETH balance for address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
- "Check the USDC balance for this address: 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
- "Analyze this transaction: 0xe3769f745ff477de5853b7410e62d8c0c32ae4f87982928432562dfabe6440eb"
- "Audit this contract: 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
- "Get the metadata for this token: 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

**Available Commands:**
- `eth_balance_tool` - Check ETH balances
- `erc20_balance_tool` - Check token balances  
- `nft_balance_tool` - Check NFT holdings
- `tx_get_tool` - Analyze transactions
- `contract_audit_tool` - Audit smart contracts
- `token_metadata_tool` - Get token information
- `logs_tool` - Query blockchain events

### Troubleshooting Claude Desktop

**Common Issues:**

1. **Server not starting**: Make sure Python is in your PATH and all dependencies are installed
2. **API key errors**: Verify your API keys are correct and have sufficient quota
3. **Network errors**: Check your internet connection and RPC endpoint availability
4. **Permission errors**: Ensure Claude Desktop has permission to run Python scripts

**Debug Steps:**
1. Test the server manually: `python server.py`
2. Check Claude Desktop logs for error messages
3. Verify the server path in your MCP configuration
4. Ensure all environment variables are set correctly

## API Documentation

### Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `eth_balance_tool` | Get ETH balance | `address`, `network` |
| `erc20_balance_tool` | Get ERC20 token balance | `address`, `token_address`, `network` |
| `nft_balance_tool` | Get NFT balance | `address`, `nft_contract`, `token_id`, `network` |
| `tx_get_tool` | Fetch transaction details | `tx_hash`, `network` |
| `logs_tool` | Query event logs | `address`, `topics`, `from_block`, `to_block`, `network` |
| `token_metadata_tool` | Get token metadata | `address`, `network` |
| `contract_audit_tool` | Analyze contract | `address`, `network`, `format` |

### Prompts

| Prompt | Description | Parameters |
|--------|-------------|------------|
| `contract_security_audit_prompt` | Security audit analysis | Contract data |
| `contract_quick_analysis_prompt` | Quick contract overview | Contract data |
| `contract_deep_dive_prompt` | Comprehensive analysis | Contract data |

## Examples

### Get ETH Balance
```python
result = eth_balance_tool("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "mainnet")
```

### Get ERC20 Balance
```python
result = erc20_balance_tool(
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", 
    "mainnet"
)
```

### Analyze Transaction
```python
result = tx_get_tool("0xe3769f745ff477de5853b7410e62d8c0c32ae4f87982928432562dfabe6440eb", "mainnet")
```

### Contract Audit
```python
result = contract_audit_tool("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "mainnet", "audit")
```

## Network Support

The server supports multiple blockchain networks with different capabilities:

- **Full Support**: Ethereum, Polygon, Arbitrum, Optimism, BSC, Avalanche, Base, Scroll, Blast
- **Limited Support**: Solana, Plasma (basic functionality)

## Security

- API keys are stored in environment variables
- Rate limiting is implemented to prevent abuse
- Input validation for all parameters
- Error handling for network failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.
