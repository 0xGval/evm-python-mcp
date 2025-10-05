"""
ETH Balance Tool

Get native ETH balance for any address on supported networks.
"""

from web3 import Web3
from config import config


def eth_balance_tool(address: str, network: str = "mainnet") -> dict:
    """
    Get ETH balance for a given address.
    
    Args:
        address: The wallet address to check balance for
        network: The network to query (mainnet, sepolia, etc.)
    
    Returns:
        Dictionary containing balance information
    """
    try:
        if network not in config["rpc_urls"]:
            raise ValueError(f"Network {network} not supported")
        
        # Create Web3 instance
        w3 = Web3(Web3.HTTPProvider(config["rpc_urls"][network]))
        
        # Check if connected
        if not w3.is_connected():
            raise ConnectionError(f"Failed to connect to {network} network")
        
        # Get balance in wei
        balance_wei = w3.eth.get_balance(address)
        
        # Convert to ETH
        balance_eth = w3.from_wei(balance_wei, 'ether')
        
        return {
            "address": address,
            "network": network,
            "balance": str(balance_eth),
            "raw_balance": str(balance_wei),
            "unit": "ETH"
        }
        
    except Exception as e:
        return {
            "error": f"Error getting ETH balance: {str(e)}",
            "address": address,
            "network": network
        }
