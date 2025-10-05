# Onchain MCP Tools Documentation

This document provides detailed information about all available tools in the Onchain MCP Server.

## 📋 **Tools by Domain**

### **Balances** 
| Tool | Purpose | Parameters |
|------|---------|------------|
| `eth_balance_tool` | Get native ETH balance | `address`, `network` |
| `erc20_balance_tool` | Get ERC20 token balance | `address`, `token_address`, `network` |
| `nft_balance_tool` | Get NFT balance (ERC721/1155) | `address`, `nft_contract`, `token_id`, `network` |

### **Data Fetch**
| Tool | Purpose | Parameters |
|------|---------|------------|
| `tx_get_tool` | Fetch transaction details | `tx_hash`, `network` |
| `logs_tool` | Query contract event logs | `contract_address`, `topic`, `from_block`, `to_block`, `network` |

### **Metadata**
| Tool | Purpose | Parameters |
|------|---------|------------|
| `token_metadata_tool` | Get token metadata | `token_address`, `network` |

### **Security & Analysis**
| Tool | Purpose | Parameters |
|------|---------|------------|
| `contract_audit_tool` | Comprehensive contract analysis | `address`, `network` |

---

## 🔧 **Tool Descriptions**

### 1. **ETH Balance Tool** (`eth_balance_tool`)

**Purpose**: Get native ETH balance for any Ethereum address.

**Parameters**:
- `address` (string, required): The wallet address to check
- `network` (string, optional): Network to query → **defaults to "mainnet"**

**Return Schema**:
```json
{
  "address": "string",
  "network": "string", 
  "balance": "string",
  "raw_balance": "string",
  "unit": "ETH"
}
```

**Example**:
```python
result = eth_balance_tool("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "mainnet")
# Returns: {"address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "balance": "0.086", "unit": "ETH"}
```

---

### 2. **ERC20 Balance Tool** (`erc20_balance_tool`)

**Purpose**: Get ERC20 token balance for any address with full token metadata.

**Parameters**:
- `address` (string, required): The wallet address to check
- `token_address` (string, required): The ERC20 token contract address
- `network` (string, optional): Network to query → **defaults to "mainnet"**

**Return Schema**:
```json
{
  "address": "string",
  "token_address": "string",
  "network": "string",
  "token_name": "string",
  "token_symbol": "string", 
  "balance": "string",
  "raw_balance": "string",
  "decimals": "number"
}
```

**Example**:
```python
result = erc20_balance_tool("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "mainnet")
# Returns: {"token_name": "USD Coin", "token_symbol": "USDC", "balance": "2835.92", "decimals": 6}
```

---

### 3. **NFT Balance Tool** (`nft_balance_tool`)

**Purpose**: Get NFT balance for ERC721 or ERC1155 tokens.

**Parameters**:
- `address` (string, required): The wallet address to check
- `nft_contract` (string, required): The NFT contract address
- `token_id` (int, optional): Token ID for ERC1155 (not needed for ERC721)
- `network` (string, optional): Network to query → **defaults to "mainnet"**

**Return Schema**:
```json
{
  "address": "string",
  "nft_contract": "string",
  "network": "string",
  "nft_name": "string",
  "nft_symbol": "string",
  "balance": "string",
  "standard": "ERC721|ERC1155",
  "token_id": "number|null",
  "uri": "string|null"
}
```

**Example**:
```python
# ERC721 (Bored Ape Yacht Club)
result = nft_balance_tool("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", network="mainnet")

# ERC1155 (requires token_id)
result = nft_balance_tool("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "0x...", token_id=1, network="mainnet")
```

---

### 4. **Transaction Fetcher Tool** (`tx_get_tool`)

**Purpose**: Get detailed transaction information by hash.

**Parameters**:
- `tx_hash` (string, required): The transaction hash
- `network` (string, optional): Network to query → **defaults to "mainnet"**

**Return Schema**:
```json
{
  "tx_hash": "string",
  "network": "string",
  "block_number": "number",
  "block_hash": "string",
  "from": "string",
  "to": "string",
  "value": "string",
  "value_eth": "string",
  "gas_used": "number",
  "gas_price": "string",
  "gas_price_gwei": "string",
  "nonce": "number",
  "status": "success|failed",
  "timestamp": "number",
  "logs_count": "number",
  "contract_address": "string|null"
}
```

**Example**:
```python
result = tx_get_tool("0xe3769f745ff477de5853b7410e62d8c0c32ae4f87982928432562dfabe6440eb", "mainnet")
# Returns complete transaction details including gas usage, status, logs, etc.
```

---

### 5. **Logs Query Tool** (`logs_tool`)

**Purpose**: Query contract event logs with filtering capabilities.

**Parameters**:
- `contract_address` (string, required): The contract address to query
- `topic` (string, optional): Event topic to filter by
- `from_block` (int, optional): Starting block number → **defaults to latest - 1000**
- `to_block` (int, optional): Ending block number → **defaults to latest**
- `network` (string, optional): Network to query → **defaults to "mainnet"**

**⚠️ Block Range Limits**: **Max 2000 blocks per call** to prevent timeouts

**Return Schema**:
```json
{
  "contract_address": "string",
  "network": "string",
  "from_block": "number",
  "to_block": "number",
  "topic_filter": "string|null",
  "logs_count": "number",
  "logs": [
    {
      "block_number": "number",
      "transaction_hash": "string",
      "log_index": "number",
      "topics": ["string"],
      "data": "string",
      "address": "string"
    }
  ]
}
```

**Example**:
```python
# Get all USDC transfer events from last 1000 blocks
result = logs_tool("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", from_block=18000000, to_block=18001000, network="mainnet")

# Filter by specific event topic (Transfer event)
result = logs_tool("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", topic="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef", network="mainnet")
```

---

### 6. **Token Metadata Tool** (`token_metadata_tool`)

**Purpose**: Get cached token metadata for ERC20 tokens.

**Parameters**:
- `token_address` (string, required): The ERC20 token contract address
- `network` (string, optional): Network to query → **defaults to "mainnet"**

**Return Schema**:
```json
{
  "token_address": "string",
  "network": "string",
  "name": "string",
  "symbol": "string",
  "decimals": "number",
  "total_supply": "string",
  "total_supply_formatted": "string",
  "cached": "boolean",
  "timestamp": "number"
}
```

**Example**:
```python
result = token_metadata_tool("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "mainnet")
# Returns: {"name": "USD Coin", "symbol": "USDC", "decimals": 6, "total_supply_formatted": "48024049359.52926"}
```

---

### 7. **Contract Audit Tool** (`contract_audit_tool`)

**Purpose**: Comprehensive contract analysis including verification status, security analysis, standards detection, and contract metadata.

**Parameters**:
- `address` (string, required): The contract address to analyze
- `network` (string, optional): Network to query → **defaults to "mainnet"**

**⚠️ Requirements**: Requires Etherscan API key for full analysis

**Return Schema**:
```json
{
  "address": "string",
  "network": "string",
  "is_contract": "boolean",
  "is_verified": "boolean",
  "contract_name": "string|null",
  "contract_creator": "string|null",
  "creation_tx": "string|null",
  "creation_timestamp": "number|null",
  "contract_code": "string|null",
  "source_code": "string|null",
  "abi": "array|null",
  "standards": {
    "is_erc20": "boolean",
    "is_erc721": "boolean", 
    "is_erc1155": "boolean"
  },
  "security_analysis": {
    "issues_found": "boolean",
    "issues": "array"
  },
  "function_signatures": "array",
  "event_signatures": "array",
  "probable_type": "string|null",
  "eth_balance": "string|null",
  "transaction_count": "number|null",
  "error": "string|null"
}
```

**Example**:
```python
result = contract_audit_tool("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "mainnet")
# Returns comprehensive contract analysis including verification status, standards, security issues, etc.
```

---

## 🌐 **Supported Networks**

All tools support the following networks (defaults to **mainnet** if omitted):

### **EVM Chains (50+ supported via Etherscan V2 API)**
- **mainnet**: Ethereum Mainnet (Chain ID: 1)
- **sepolia**: Ethereum Sepolia Testnet (Chain ID: 11155111)
- **polygon**: Polygon Mainnet (Chain ID: 137)
- **arbitrum**: Arbitrum One (Chain ID: 42161)
- **optimism**: Optimism Mainnet (Chain ID: 10)
- **bsc**: Binance Smart Chain (Chain ID: 56)
- **avalanche**: Avalanche C-Chain (Chain ID: 43114)
- **base**: Base (Chain ID: 8453)
- **scroll**: Scroll (Chain ID: 534352)
- **blast**: Blast (Chain ID: 81457)

### **Multichain Support**
- ✅ **Single API Key**: Use one Etherscan API key for all 50+ chains
- ✅ **Unified Experience**: Same API calls work across all chains
- ✅ **Contract Verification**: Works across all supported chains
- ✅ **Transaction Fetching**: Cross-chain transaction data

---

## 🔧 **Common Event Topics**

### ERC20 Events:
- **Transfer**: `0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef`
- **Approval**: `0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925`

### ERC721 Events:
- **Transfer**: `0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef`
- **Approval**: `0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925`
- **ApprovalForAll**: `0x17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31`

---

## 🚀 **Usage Examples**

### Get Vitalik's ETH Balance:
```python
eth_balance_tool("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "mainnet")
```

### Check USDC Balance:
```python
erc20_balance_tool("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "mainnet")
```

### Get BAYC NFT Balance:
```python
nft_balance_tool("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", network="mainnet")
```

### Fetch Transaction Details:
```python
tx_get_tool("0xe3769f745ff477de5853b7410e62d8c0c32ae4f87982928432562dfabe6440eb", "mainnet")
```

### Query USDC Transfer Events:
```python
logs_tool("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", from_block=18000000, to_block=18001000, network="mainnet")
```

### Get Token Information:
```python
token_metadata_tool("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "mainnet")
```

---

## ⚡ **Performance Notes**

- **Caching**: Token metadata is cached for performance
- **Rate Limits**: Configurable in `config.py`
- **Timeouts**: 30-second default timeout
- **Batch Queries**: Logs tool can handle large block ranges efficiently

---

## 🔒 **Security & Best Practices**

1. **RPC URLs**: Use your own RPC endpoints for production
2. **Rate Limiting**: Configure appropriate limits in `config.py`
3. **Error Handling**: All tools include comprehensive error handling
4. **Validation**: Address checksums are validated automatically

---

## 📊 **Real-World Use Cases**

- **Portfolio Tracking**: Monitor ETH and token balances
- **NFT Analytics**: Track NFT ownership and transfers
- **Transaction Analysis**: Investigate specific transactions
- **Event Monitoring**: Track smart contract events
- **Token Research**: Get token metadata and supply information
- **DeFi Analytics**: Analyze protocol interactions and flows
