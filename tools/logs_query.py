"""
Logs Query Tool

Query contract logs by topic and block range on supported networks.
"""

from web3 import Web3
from config import config


def logs_tool(contract_address: str, topic: str = None, from_block: int = None, to_block: int = None, network: str = "mainnet") -> dict:
    """
    Query contract logs by topic and block range.
    
    Args:
        contract_address: The contract address to query logs for
        topic: The event topic to filter by (optional)
        from_block: Starting block number (optional, defaults to latest - 1000)
        to_block: Ending block number (optional, defaults to latest)
        network: The network to query (mainnet, sepolia, etc.)
    
    Returns:
        Dictionary containing log information
    """
    try:
        if network not in config["rpc_urls"]:
            raise ValueError(f"Network {network} not supported")
        
        # Create Web3 instance
        w3 = Web3(Web3.HTTPProvider(config["rpc_urls"][network]))
        
        # Check if connected
        if not w3.is_connected():
            raise ConnectionError(f"Failed to connect to {network} network")
        
        # Get latest block if to_block not specified
        if to_block is None:
            to_block = w3.eth.block_number
        
        # Set from_block if not specified
        if from_block is None:
            from_block = max(0, to_block - 1000)  # Default to last 1000 blocks
        
        # Prepare filter parameters
        filter_params = {
            'fromBlock': from_block,
            'toBlock': to_block,
            'address': contract_address
        }
        
        # Add topic filter if provided
        if topic:
            filter_params['topics'] = [topic]
        
        # Get logs
        logs = w3.eth.get_logs(filter_params)
        
        # Format logs for output
        formatted_logs = []
        for log in logs:
            formatted_logs.append({
                "block_number": log.blockNumber,
                "transaction_hash": log.transactionHash.hex(),
                "log_index": log.logIndex,
                "topics": [topic.hex() for topic in log.topics],
                "data": log.data.hex(),
                "address": log.address
            })
        
        return {
            "contract_address": contract_address,
            "network": network,
            "from_block": from_block,
            "to_block": to_block,
            "topic_filter": topic,
            "logs_count": len(logs),
            "logs": formatted_logs
        }
        
    except Exception as e:
        return {
            "error": f"Error querying logs: {str(e)}",
            "contract_address": contract_address,
            "network": network
        }
