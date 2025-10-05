"""
Enhanced Transaction Fetcher Tool

Get detailed transaction information including ERC-20 transfers, contract interactions, and decoded data.
"""

from web3 import Web3
import json
from config import config


def tx_get_tool(tx_hash: str, network: str = "mainnet") -> dict:
    """
    Get enhanced transaction details including ERC-20 transfers and decoded data.
    
    Args:
        tx_hash: The transaction hash to fetch
        network: The network to query (mainnet, sepolia, etc.)
    
    Returns:
        Dictionary containing detailed transaction information
    """
    try:
        if network not in config["rpc_urls"]:
            raise ValueError(f"Network {network} not supported")
        
        # Create Web3 instance
        w3 = Web3(Web3.HTTPProvider(config["rpc_urls"][network]))
        
        # Check if connected
        if not w3.is_connected():
            raise ConnectionError(f"Failed to connect to {network} network")
        
        # Get transaction details
        tx = w3.eth.get_transaction(tx_hash)
        tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
        
        # Get block details
        block = w3.eth.get_block(tx_receipt.blockNumber)
        
        # Calculate transaction fee
        gas_fee = tx_receipt.gasUsed * tx['gasPrice']
        gas_fee_eth = w3.from_wei(gas_fee, 'ether')
        
        # Decode transaction input data
        input_data = tx.get('input', b'')
        if hasattr(input_data, 'hex'):
            input_data = input_data.hex()
        elif isinstance(input_data, bytes):
            input_data = input_data.hex()
        
        decoded_input = decode_transaction_input(input_data)
        
        # Analyze logs for ERC-20 transfers
        erc20_transfers = analyze_erc20_transfers(w3, tx_receipt.logs)
        
        # Get token metadata if it's a token interaction
        token_metadata = None
        if erc20_transfers:
            token_metadata = get_token_metadata(w3, erc20_transfers[0]['token_address'])
        
        return {
            "tx_hash": tx_hash,
            "network": network,
            "block_number": tx_receipt.blockNumber,
            "block_hash": tx_receipt.blockHash.hex(),
            "from": tx['from'],
            "to": tx['to'],
            "value": str(tx['value']),
            "value_eth": str(w3.from_wei(tx['value'], 'ether')),
            "gas_used": tx_receipt.gasUsed,
            "gas_price": str(tx['gasPrice']),
            "gas_price_gwei": str(w3.from_wei(tx['gasPrice'], 'gwei')),
            "gas_fee_eth": str(gas_fee_eth),
            "gas_fee_usd": estimate_usd_value(gas_fee_eth),
            "nonce": tx['nonce'],
            "status": "success" if tx_receipt.status == 1 else "failed",
            "timestamp": block.timestamp,
            "logs_count": len(tx_receipt.logs),
            "contract_address": tx_receipt.contractAddress.hex() if tx_receipt.contractAddress else None,
            "input_data": input_data,
            "decoded_input": decoded_input,
            "erc20_transfers": erc20_transfers,
            "token_metadata": token_metadata,
            "transaction_type": determine_transaction_type(tx, erc20_transfers)
        }
        
    except Exception as e:
        return {
            "error": f"Error getting transaction: {str(e)}",
            "tx_hash": tx_hash,
            "network": network
        }


def decode_transaction_input(input_data):
    """Decode transaction input data"""
    if not input_data or input_data == '0x':
        return None
    
    try:
        # Common function selectors
        function_selectors = {
            'a9059cbb': 'transfer(address,uint256)',
            '23b872dd': 'transferFrom(address,address,uint256)',
            '095ea7b3': 'approve(address,uint256)',
            '70a08231': 'balanceOf(address)',
            '18160ddd': 'totalSupply()',
            '06fdde03': 'name()',
            '95d89b41': 'symbol()',
            '313ce567': 'decimals()'
        }
        
        if len(input_data) >= 10:
            selector = input_data[:10]
            function_name = function_selectors.get(selector, f'Unknown function (0x{selector})')
            
            return {
                "function_selector": selector,
                "function_name": function_name,
                "raw_input": input_data
            }
    except:
        pass
    
    return None


def analyze_erc20_transfers(w3, logs):
    """Analyze logs for ERC-20 transfer events"""
    transfers = []
    
    # ERC-20 Transfer event signature
    transfer_topic = 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
    
    for log in logs:
        try:
            # Convert topics to hex strings
            topics_hex = [topic.hex() for topic in log.topics]
            
            if len(topics_hex) >= 3 and topics_hex[0] == transfer_topic:
                # Decode transfer event
                from_addr = '0x' + topics_hex[1][26:]  # Remove padding
                to_addr = '0x' + topics_hex[2][26:]   # Remove padding
                
                # Get token address
                token_address = log.address
                
                # Decode amount from data
                data_hex = log.data.hex()
                if data_hex.startswith('0x'):
                    data_hex = data_hex[2:]
                amount = int(data_hex, 16) if data_hex else 0
                
                # Get token decimals
                decimals = get_token_decimals(w3, token_address)
                formatted_amount = amount / (10 ** decimals) if decimals else amount
                
                transfers.append({
                    "token_address": token_address,
                    "from": from_addr,
                    "to": to_addr,
                    "amount": str(amount),
                    "amount_formatted": str(formatted_amount),
                    "decimals": decimals
                })
        except Exception as e:
            print(f"Error processing log: {e}")
            continue
    
    return transfers


def get_token_decimals(w3, token_address):
    """Get token decimals"""
    try:
        # ERC-20 decimals() function
        decimals_abi = {
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "stateMutability": "view",
            "type": "function"
        }
        
        contract = w3.eth.contract(address=token_address, abi=[decimals_abi])
        return contract.functions.decimals().call()
    except:
        return 18  # Default to 18 decimals


def get_token_metadata(w3, token_address):
    """Get basic token metadata"""
    try:
        # ERC-20 standard functions
        abi = [
            {"inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"}
        ]
        
        contract = w3.eth.contract(address=token_address, abi=abi)
        
        return {
            "name": contract.functions.name().call(),
            "symbol": contract.functions.symbol().call(),
            "decimals": contract.functions.decimals().call()
        }
    except:
        return None


def determine_transaction_type(tx, erc20_transfers):
    """Determine the type of transaction"""
    if tx['value'] > 0:
        return "ETH Transfer"
    elif erc20_transfers:
        if len(erc20_transfers) == 1:
            return f"ERC-20 Transfer ({erc20_transfers[0].get('token_symbol', 'Token')})"
        else:
            return "Multiple ERC-20 Transfers"
    elif tx['to'] and tx['input'] and tx['input'] != '0x':
        return "Contract Interaction"
    else:
        return "Unknown"


def estimate_usd_value(eth_amount):
    """Estimate USD value (placeholder - would need price API)"""
    # This is a placeholder - in a real implementation, you'd fetch current ETH price
    eth_price_usd = 3000  # Placeholder price
    return f"${float(eth_amount) * eth_price_usd:.2f}"
