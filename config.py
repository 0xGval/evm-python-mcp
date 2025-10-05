"""
Configuration for the Onchain MCP Server
"""

import os

config = {
    "rpc_urls": {
        "mainnet": "https://eth-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "sepolia": "https://eth-sepolia.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "polygon": "https://polygon-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "arbitrum": "https://arb-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "optimism": "https://opt-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "bsc": "https://bsc-dataseed.binance.org",
        "avalanche": "https://api.avax.network/ext/bc/C/rpc",
        "base": "https://base-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "scroll": "https://scroll-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "blast": "https://blast-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "hyperliquid": "https://hyperliquid-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "solana": "https://solana-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
        "plasma": "https://plasma-mainnet.g.alchemy.com/v2/rakkIKoM_yIqnkA_rnpxzAzuDnOodFKC",
    },
    "limits": {
        "max_requests_per_minute": 100,
        "max_concurrent_requests": 10,
        "request_timeout": 30,  # seconds
    },
    "default_network": "mainnet",
    "etherscan_api_key": os.getenv("ETHERSCAN_API_KEY", "HV6EWTABDZCWPZHHNKX13VFCQAVQZUK4V2"),
    "etherscan_v2_url": "https://api.etherscan.io/v2/api",
    "supported_chains": {
        "mainnet": 1,
        "sepolia": 11155111,
        "polygon": 137,
        "arbitrum": 42161,
        "optimism": 10,
        "bsc": 56,
        "avalanche": 43114,
        "base": 8453,
        "scroll": 534352,
        "blast": 81457,
        "hyperliquid": 999,  # Hyperliquid uses Arbitrum-compatible chain ID
        "solana": 101,  # Solana mainnet
        "plasma": 9745,  # Plasma uses Ethereum-compatible chain ID
    },
}
