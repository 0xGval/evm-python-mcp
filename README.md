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
- **Solana**
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
   git clone https://github.com/yourusername/onchain-mcp.git
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

### Using with MCP Clients

The server provides tools that can be used with MCP-compatible clients like Cursor, Claude Desktop, or other MCP clients.

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