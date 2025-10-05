"""
NFT Balance Tool

Get ERC721/ERC1155 NFT balances for any address on supported networks.
"""

from web3 import Web3
from config import config

# ERC721 ABI for balanceOf
ERC721_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
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
    }
]

# ERC1155 ABI for balanceOf
ERC1155_ABI = [
    {
        "constant": True,
        "inputs": [
            {"name": "account", "type": "address"},
            {"name": "id", "type": "uint256"}
        ],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "id", "type": "uint256"}],
        "name": "uri",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]


def nft_balance_tool(address: str, nft_contract: str, token_id: int = None, network: str = "mainnet") -> dict:
    """
    Get NFT balance for a given address.
    
    Args:
        address: The wallet address to check balance for
        nft_contract: The NFT contract address (ERC721 or ERC1155)
        token_id: Token ID for ERC1155 (optional for ERC721)
        network: The network to query (mainnet, sepolia, etc.)
    
    Returns:
        Dictionary containing NFT balance information
    """
    try:
        if network not in config["rpc_urls"]:
            raise ValueError(f"Network {network} not supported")
        
        # Create Web3 instance
        w3 = Web3(Web3.HTTPProvider(config["rpc_urls"][network]))
        
        # Check if connected
        if not w3.is_connected():
            raise ConnectionError(f"Failed to connect to {network} network")
        
        # Try ERC721 first
        try:
            contract = w3.eth.contract(address=nft_contract, abi=ERC721_ABI)
            balance = contract.functions.balanceOf(address).call()
            name = contract.functions.name().call()
            symbol = contract.functions.symbol().call()
            
            return {
                "address": address,
                "nft_contract": nft_contract,
                "network": network,
                "nft_name": name,
                "nft_symbol": symbol,
                "balance": str(balance),
                "standard": "ERC721",
                "token_id": None
            }
            
        except Exception as erc721_error:
            # Try ERC1155 if ERC721 fails
            if token_id is None:
                return {
                    "error": f"ERC721 failed: {str(erc721_error)}. For ERC1155, token_id is required.",
                    "address": address,
                    "nft_contract": nft_contract,
                    "network": network
                }
            
            try:
                contract = w3.eth.contract(address=nft_contract, abi=ERC1155_ABI)
                balance = contract.functions.balanceOf(address, token_id).call()
                uri = contract.functions.uri(token_id).call()
                
                return {
                    "address": address,
                    "nft_contract": nft_contract,
                    "network": network,
                    "balance": str(balance),
                    "standard": "ERC1155",
                    "token_id": token_id,
                    "uri": uri
                }
                
            except Exception as erc1155_error:
                return {
                    "error": f"Both ERC721 and ERC1155 failed. ERC721: {str(erc721_error)}, ERC1155: {str(erc1155_error)}",
                    "address": address,
                    "nft_contract": nft_contract,
                    "network": network
                }
        
    except Exception as e:
        return {
            "error": f"Error getting NFT balance: {str(e)}",
            "address": address,
            "nft_contract": nft_contract,
            "network": network
        }
