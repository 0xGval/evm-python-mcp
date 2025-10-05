"""
Token Metadata Tool

Get cached token metadata (name, symbol, decimals) for ERC20 tokens.
"""

from web3 import Web3
from config import config

# Standard ERC20 ABI for metadata
ERC20_METADATA_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]


def token_metadata_tool(token_address: str, network: str = "mainnet") -> dict:
    """
    Get token metadata for an ERC20 token.
    
    Args:
        token_address: The ERC20 token contract address
        network: The network to query (mainnet, sepolia, etc.)
    
    Returns:
        Dictionary containing token metadata
    """
    try:
        if network not in config["rpc_urls"]:
            raise ValueError(f"Network {network} not supported")
        
        # Create Web3 instance
        w3 = Web3(Web3.HTTPProvider(config["rpc_urls"][network]))
        
        # Check if connected
        if not w3.is_connected():
            raise ConnectionError(f"Failed to connect to {network} network")
        
        # Create contract instance
        contract = w3.eth.contract(address=token_address, abi=ERC20_METADATA_ABI)
        
        # Get token metadata
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call()
        
        # Format total supply
        total_supply_formatted = total_supply / (10 ** decimals)
        
        return {
            "token_address": token_address,
            "network": network,
            "name": name,
            "symbol": symbol,
            "decimals": decimals,
            "total_supply": str(total_supply),
            "total_supply_formatted": str(total_supply_formatted),
            "cached": True,
            "timestamp": w3.eth.get_block('latest').timestamp
        }
        
    except Exception as e:
        return {
            "error": f"Error getting token metadata: {str(e)}",
            "token_address": token_address,
            "network": network
        }
