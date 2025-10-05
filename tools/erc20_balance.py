"""
ERC20 Balance Tool

Get ERC20 token balance for any address on supported networks.
"""

from web3 import Web3
from config import config

# Standard ERC20 ABI for common functions
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
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
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]


def erc20_balance_tool(address: str, token_address: str, network: str = "mainnet") -> dict:
    """
    Get ERC20 token balance for a given address.
    
    Args:
        address: The wallet address to check balance for
        token_address: The ERC20 token contract address
        network: The network to query (mainnet, sepolia, etc.)
    
    Returns:
        Dictionary containing token balance information
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
        contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
        
        # Get token information and balance
        balance_wei = contract.functions.balanceOf(address).call()
        decimals = contract.functions.decimals().call()
        symbol = contract.functions.symbol().call()
        name = contract.functions.name().call()
        
        # Convert balance to human readable format
        balance_formatted = balance_wei / (10 ** decimals)
        
        return {
            "address": address,
            "token_address": token_address,
            "network": network,
            "token_name": name,
            "token_symbol": symbol,
            "balance": str(balance_formatted),
            "raw_balance": str(balance_wei),
            "decimals": decimals
        }
        
    except Exception as e:
        return {
            "error": f"Error getting ERC20 balance: {str(e)}",
            "address": address,
            "token_address": token_address,
            "network": network
        }
