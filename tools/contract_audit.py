"""
Contract Audit Tool

Comprehensive multi-chain contract analysis including verification status,
security analysis, standards detection, and contract metadata.
Supports 12+ blockchain networks with fallback mechanisms.
"""

import requests
import json
from web3 import Web3
from config import config
from tools.token_metadata import token_metadata_tool
from prompts.contract_audit import (
    contract_security_audit_prompt,
    contract_quick_analysis_prompt,
    contract_deep_dive_prompt
)

async def contract_audit_tool(address: str, network: str = "mainnet", format: str = "raw") -> dict:
    """
    Comprehensive contract audit and analysis across multiple blockchain networks.
    
    Args:
        address: The contract address to analyze
        network: The network to query → defaults to "mainnet"
                 All networks from config.rpc_urls are supported
        format: Output format → "raw" (data only), "audit" (security audit prompt), 
                "quick" (quick analysis prompt), "deep" (deep dive prompt)
    
    Returns:
        Dictionary containing comprehensive contract analysis
        - Full Etherscan support: All networks with chain IDs in config.supported_chains
        - Limited analysis: Networks without Etherscan support (solana, plasma)
        - Prompt formats: Structured prompts for AI analysis
    """
    try:
        # Validate network support
        if network not in config["rpc_urls"]:
            supported_networks = list(config["rpc_urls"].keys())
            raise ValueError(f"Network '{network}' not supported. Supported networks: {supported_networks}")
        
        # Create Web3 instance
        w3 = Web3(Web3.HTTPProvider(config["rpc_urls"][network]))
        
        # Check if connected
        if not w3.is_connected():
            raise ConnectionError(f"Failed to connect to {network} network")
        
        # Validate and format address
        if not w3.is_address(address):
            raise ValueError("Invalid Ethereum address format")
        
        formatted_address = w3.to_checksum_address(address)
        
        # Perform comprehensive analysis
        result = await analyze_contract(w3, formatted_address, network)
        
        # Format output based on requested format
        if format == "raw":
            return result
        else:
            return await format_audit_output(result, address, network, format)
        
    except Exception as e:
        return {
            "error": f"Error analyzing contract: {str(e)}",
            "address": address,
            "network": network
        }


async def analyze_contract(w3, address, network):
    """Perform comprehensive contract analysis with multi-chain support"""
    
    # Step 1: Check if address is a contract
    is_contract = await check_if_contract(w3, address)
    
    result = {
        "address": address,
        "network": network,
        "is_contract": is_contract,
        "is_verified": False,
        "contract_name": None,
        "contract_creator": None,
        "creation_tx": None,
        "creation_timestamp": None,
        "contract_code": None,
        "source_code": None,
        "abi": None,
        "standards": {},
        "security_analysis": {},
        "function_signatures": [],
        "event_signatures": [],
        "error": None,
        "analysis_limitations": []
    }
    
    # If not a contract, return early with basic info
    if not is_contract:
        result["error"] = "Address is not a contract"
        
        # Get native token balance and transaction count
        try:
            balance = w3.eth.get_balance(address)
            result["native_balance"] = str(w3.from_wei(balance, 'ether'))
            result["transaction_count"] = w3.eth.get_transaction_count(address)
        except:
            pass
        
        return result
    
    # Get contract bytecode
    try:
        bytecode = w3.eth.get_code(address)
        result["contract_code"] = bytecode.hex()
    except:
        pass
    
    # Step 2: Check if network supports Etherscan API
    chain_id = config["supported_chains"].get(network)
    # Networks with Etherscan support are those that have chain IDs (excluding solana and plasma)
    etherscan_supported = chain_id and network not in ["solana", "plasma"]
    
    if etherscan_supported:
        # Get contract creation info from Etherscan
        creation_info = await get_contract_creation_info(address, network)
        if creation_info:
            result["contract_creator"] = creation_info.get("contract_creator")
            result["creation_tx"] = creation_info.get("tx_hash")
            result["creation_timestamp"] = creation_info.get("timestamp")
        
        # Check verification status and get source code
        verification_info = await check_verification_status(address, network)
        result["is_verified"] = verification_info.get("is_verified", False)
        
        if result["is_verified"]:
            result["source_contract_name"] = verification_info.get("contract_name")  # Keep source code name
            result["source_code"] = verification_info.get("source_code")
            result["abi"] = verification_info.get("abi")
            
            # Detect contract standards
            if result["abi"]:
                result["standards"] = detect_contract_standards(result["abi"])
                result["function_signatures"] = extract_function_signatures(result["abi"])
                result["event_signatures"] = extract_event_signatures(result["abi"])
            
            # Perform security analysis
            if result["source_code"]:
                result["security_analysis"] = analyze_contract_security(result["source_code"])
        else:
            result["error"] = f"Contract is not verified on Etherscan for {network}"
    else:
        # For non-Etherscan supported chains, provide limited analysis
        result["analysis_limitations"].append(f"Etherscan API not supported for {network}")
        result["error"] = f"Limited analysis available for {network} - Etherscan not supported"
    
    # Always attempt bytecode analysis regardless of Etherscan support
    if result["contract_code"]:
        result["probable_type"] = detect_contract_type_from_bytecode(result["contract_code"])
        
        # Check for proxy patterns and analyze actual state
        proxy_analysis = detect_proxy_patterns(w3, address, result["contract_code"])
        if proxy_analysis["is_proxy"]:
            result["proxy_analysis"] = proxy_analysis
            result["deployed_state"] = await analyze_deployed_state(w3, address, network)
            
            # Update contract name with deployed state if available
            if result["deployed_state"] and "token_info" in result["deployed_state"]:
                deployed_name = result["deployed_state"]["token_info"].get("name")
                if deployed_name:
                    result["contract_name"] = deployed_name  # Set main contract name to deployed name
                    result["deployed_contract_name"] = deployed_name
                    result["deployed_symbol"] = result["deployed_state"]["token_info"].get("symbol")
        
        # Enhanced bytecode analysis for non-Etherscan chains
        if not etherscan_supported:
            result["bytecode_analysis"] = enhanced_bytecode_analysis(result["contract_code"])
        
        # Always try to get deployed state for token contracts (even non-proxies)
        if not proxy_analysis["is_proxy"]:
            result["deployed_state"] = await analyze_deployed_state(w3, address, network)
            
            # Update contract name with deployed state if available
            if result["deployed_state"] and "token_info" in result["deployed_state"]:
                deployed_name = result["deployed_state"]["token_info"].get("name")
                if deployed_name:
                    result["contract_name"] = deployed_name  # Set main contract name to deployed name
                    result["deployed_contract_name"] = deployed_name
                    result["deployed_symbol"] = result["deployed_state"]["token_info"].get("symbol")
    
    return result


async def format_audit_output(audit_data, address, network, format_type):
    """Format audit data using appropriate prompt template"""
    try:
        # Extract key data for prompt formatting
        contract_name = audit_data.get("contract_name", "Unknown")
        is_verified = audit_data.get("is_verified", False)
        
        # Get the appropriate prompt template
        if format_type == "audit":
            prompt_template = contract_security_audit_prompt()
        elif format_type == "quick":
            prompt_template = contract_quick_analysis_prompt()
        elif format_type == "deep":
            prompt_template = contract_deep_dive_prompt()
        else:
            return audit_data  # Return raw data if format not recognized
        
        # Format the prompt with actual data
        formatted_prompt = prompt_template.format(
            address=address,
            network=network,
            contract_name=contract_name,
            is_verified="✅ Verified" if is_verified else "❌ Not Verified"
        )
        
        # Return structured prompt response
        return {
            "prompt": formatted_prompt,
            "context": audit_data,
            "format_type": format_type,
            "address": address,
            "network": network,
            "timestamp": audit_data.get("timestamp")
        }
        
    except Exception as e:
        return {
            "error": f"Error formatting audit output: {str(e)}",
            "raw_data": audit_data,
            "address": address,
            "network": network
        }


async def check_if_contract(w3, address):
    """Check if address is a contract"""
    try:
        code = w3.eth.get_code(address)
        return code != b'\x00' and len(code) > 0
    except:
        return False


async def get_contract_creation_info(address, network):
    """Get contract creation information from Etherscan V2 API with multi-chain support"""
    try:
        # Get chain ID for the network
        chain_id = config["supported_chains"].get(network)
        if not chain_id:
            return None
        
        # Check if network supports Etherscan API
        # Networks with Etherscan support are those that have chain IDs (excluding solana and plasma)
        etherscan_supported = chain_id and network not in ["solana", "plasma"]
        if not etherscan_supported:
            return None
        
        # Use Etherscan V2 API for multichain support
        url = f"{config['etherscan_v2_url']}?chainid={chain_id}&module=contract&action=getcontractcreation&contractaddresses={address}&apikey={config['etherscan_api_key']}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("status") != "1" or not data.get("result") or not data["result"]:
            return None
        
        creation_data = data["result"][0]
        return {
            "contract_creator": creation_data.get("contractCreator"),
            "tx_hash": creation_data.get("txHash"),
            "timestamp": None  # Would need additional API call to get timestamp
        }
    except Exception as e:
        print(f"Error getting creation info for {network}: {e}")
        return None


async def check_verification_status(address, network):
    """Check if contract is verified on Etherscan V2 API with multi-chain support"""
    try:
        # Get chain ID for the network
        chain_id = config["supported_chains"].get(network)
        if not chain_id:
            return {"is_verified": False}
        
        # Check if network supports Etherscan API
        # Networks with Etherscan support are those that have chain IDs (excluding solana and plasma)
        etherscan_supported = chain_id and network not in ["solana", "plasma"]
        if not etherscan_supported:
            return {"is_verified": False}
        
        # Use Etherscan V2 API for multichain support
        url = f"{config['etherscan_v2_url']}?chainid={chain_id}&module=contract&action=getsourcecode&address={address}&apikey={config['etherscan_api_key']}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("status") != "1" or not data.get("result") or not data["result"]:
            return {"is_verified": False}
        
        contract_data = data["result"][0]
        source_code = contract_data.get("SourceCode", "")
        
        # Check if contract is verified (has meaningful source code)
        is_verified = source_code and source_code != "{}" and len(source_code) > 2
        
        result = {"is_verified": is_verified}
        
        if is_verified:
            result.update({
                "contract_name": contract_data.get("ContractName"),
                "source_code": source_code,
                "abi": json.loads(contract_data.get("ABI", "[]")) if contract_data.get("ABI") else None
            })
        
        return result
    except Exception as e:
        print(f"Error checking verification status for {network}: {e}")
        return {"is_verified": False}


def detect_contract_standards(abi):
    """Detect contract standards (ERC20, ERC721, ERC1155)"""
    if not abi or not isinstance(abi, list):
        return {"is_erc20": False, "is_erc721": False, "is_erc1155": False}
    
    # Function signatures for different standards
    erc20_functions = ['totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']
    erc721_functions = ['balanceOf', 'ownerOf', 'safeTransferFrom', 'transferFrom', 'approve', 'getApproved', 'setApprovalForAll', 'isApprovedForAll']
    erc1155_functions = ['balanceOf', 'balanceOfBatch', 'setApprovalForAll', 'isApprovedForAll', 'safeTransferFrom', 'safeBatchTransferFrom']
    
    # Extract function names from ABI
    function_names = [item["name"] for item in abi if item.get("type") == "function" and item.get("name")]
    
    # Check standard compliance
    is_erc20 = all(func in function_names for func in erc20_functions)
    is_erc721 = all(func in function_names for func in erc721_functions)
    is_erc1155 = all(func in function_names for func in erc1155_functions)
    
    return {
        "is_erc20": is_erc20,
        "is_erc721": is_erc721,
        "is_erc1155": is_erc1155
    }


def detect_contract_type_from_bytecode(bytecode):
    """Attempt to detect contract type from bytecode"""
    if not bytecode:
        return "Unknown"
    
    # Look for common bytecode patterns
    if "06fdde03" in bytecode and "95d89b41" in bytecode and "18160ddd" in bytecode:
        return "Likely Token (ERC20/ERC721)"
    
    if "01ffc9a7" in bytecode:
        return "Supports ERC165 Interface Detection"
    
    if "e8a3d485" in bytecode:
        return "Possible Uniswap-related contract"
    
    if "6080604052" in bytecode:
        return "Solidity 0.4.x+ Contract"
    
    return "Unknown Contract Type"


def detect_proxy_patterns(w3, address, bytecode):
    """Detect proxy patterns in contract bytecode and analyze proxy state"""
    if not bytecode:
        return {"is_proxy": False}
    
    analysis = {
        "is_proxy": False,
        "proxy_type": "Unknown",
        "implementation_address": None,
        "admin_address": None,
        "patterns_detected": [],
        "confidence": 0
    }
    
    # Common proxy patterns
    proxy_patterns = {
        "360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc": "OpenZeppelin Transparent Proxy",
        "5c60da1b": "EIP-1967 Proxy",
        "f851a440": "EIP-1822 Universal Proxy",
        "4e487b71": "OpenZeppelin Upgradeable",
        "a3f0ad74e8653cd": "Beacon Proxy"
    }
    
    # Check for proxy patterns in bytecode
    for pattern, proxy_type in proxy_patterns.items():
        if pattern in bytecode:
            analysis["is_proxy"] = True
            analysis["proxy_type"] = proxy_type
            analysis["patterns_detected"].append(f"Proxy pattern: {proxy_type}")
            analysis["confidence"] = 0.8
            break
    
    # If proxy detected, try to get implementation address
    if analysis["is_proxy"]:
        try:
            # Try different storage slots for implementation address
            implementation_slots = [
                "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc",  # EIP-1967
                "0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a4fd6e3cd362f230da",  # Alternative slot
            ]
            
            for slot in implementation_slots:
                try:
                    storage_value = w3.eth.get_storage_at(address, int(slot, 16))
                    if storage_value != b'\x00' * 32:
                        # Convert to address (last 20 bytes)
                        impl_address = '0x' + storage_value[-20:].hex()
                        if w3.is_address(impl_address):
                            analysis["implementation_address"] = w3.to_checksum_address(impl_address)
                            break
                except:
                    continue
        except:
            pass
    
    return analysis


async def analyze_deployed_state(w3, address, network):
    """Analyze the actual deployed state of a contract (especially important for proxies)"""
    state_analysis = {
        "token_info": {},
        "balances": {},
        "supply_info": {},
        "owner_info": {},
        "error": None
    }
    
    try:
        # Use the dedicated token_metadata_tool for token information
        token_metadata = token_metadata_tool(address, network)
        
        if "error" not in token_metadata:
            # Extract token information from metadata tool
            state_analysis["token_info"] = {
                "name": token_metadata.get("name"),
                "symbol": token_metadata.get("symbol"),
                "decimals": token_metadata.get("decimals")
            }
            
            state_analysis["supply_info"] = {
                "total_supply": token_metadata.get("total_supply"),
                "total_supply_formatted": token_metadata.get("total_supply_formatted")
            }
        else:
            # Fallback: try to get basic token info directly
            try:
                standard_abi = [
                    {"inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}
                ]
                
                contract = w3.eth.contract(address=address, abi=standard_abi)
                
                try:
                    state_analysis["token_info"]["name"] = contract.functions.name().call()
                except:
                    pass
                    
                try:
                    state_analysis["token_info"]["symbol"] = contract.functions.symbol().call()
                except:
                    pass
                    
                try:
                    state_analysis["token_info"]["decimals"] = contract.functions.decimals().call()
                except:
                    pass
                
                try:
                    total_supply = contract.functions.totalSupply().call()
                    state_analysis["supply_info"]["total_supply"] = str(total_supply)
                    if "decimals" in state_analysis["token_info"]:
                        decimals = state_analysis["token_info"]["decimals"]
                        formatted_supply = total_supply / (10 ** decimals)
                        state_analysis["supply_info"]["total_supply_formatted"] = str(formatted_supply)
                except:
                    pass
            except:
                pass
        
        # Get additional contract-specific information
        try:
            # Try to get owner information
            owner_abi = [{"inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "stateMutability": "view", "type": "function"}]
            owner_contract = w3.eth.contract(address=address, abi=owner_abi)
            owner = owner_contract.functions.owner().call()
            state_analysis["owner_info"]["owner"] = owner
        except:
            pass
        
        # Get contract's native token balance
        try:
            contract_balance = w3.eth.get_balance(address)
            state_analysis["balances"]["native_balance"] = str(w3.from_wei(contract_balance, 'ether'))
        except:
            pass
            
    except Exception as e:
        state_analysis["error"] = f"Error analyzing deployed state: {str(e)}"
    
    return state_analysis


def enhanced_bytecode_analysis(bytecode):
    """Enhanced bytecode analysis for chains without Etherscan support"""
    if not bytecode:
        return {"analysis": "No bytecode available", "confidence": 0}
    
    analysis = {
        "bytecode_length": len(bytecode),
        "patterns_detected": [],
        "likely_contract_type": "Unknown",
        "confidence": 0,
        "analysis": "Basic bytecode analysis"
    }
    
    # Common function selectors and their meanings
    function_selectors = {
        "06fdde03": "name()",
        "95d89b41": "symbol()", 
        "18160ddd": "totalSupply()",
        "70a08231": "balanceOf(address)",
        "a9059cbb": "transfer(address,uint256)",
        "23b872dd": "transferFrom(address,address,uint256)",
        "095ea7b3": "approve(address,uint256)",
        "8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925": "Approval(address,address,uint256)",
        "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "Transfer(address,address,uint256)",
        "01ffc9a7": "supportsInterface(bytes4)",
        "6352211e": "ownerOf(uint256)",
        "42842e0e": "safeTransferFrom(address,address,uint256)",
        "b88d4fde": "safeTransferFrom(address,address,uint256,bytes)"
    }
    
    # Detect function selectors in bytecode
    detected_functions = []
    for selector, function_name in function_selectors.items():
        if selector in bytecode:
            detected_functions.append(function_name)
            analysis["patterns_detected"].append(f"Function: {function_name}")
    
    # Determine likely contract type based on detected functions
    if any(func in detected_functions for func in ["name()", "symbol()", "totalSupply()", "balanceOf(address)"]):
        if "ownerOf(uint256)" in detected_functions:
            analysis["likely_contract_type"] = "Likely NFT (ERC721)"
            analysis["confidence"] = 0.8
        elif "transfer(address,uint256)" in detected_functions:
            analysis["likely_contract_type"] = "Likely Token (ERC20)"
            analysis["confidence"] = 0.8
        else:
            analysis["likely_contract_type"] = "Likely Token Contract"
            analysis["confidence"] = 0.6
    
    # Check for common DeFi patterns
    if "e8a3d485" in bytecode:  # Uniswap V2 router
        analysis["likely_contract_type"] = "Likely DEX Router (Uniswap V2)"
        analysis["confidence"] = 0.9
        analysis["patterns_detected"].append("Uniswap V2 Router pattern")
    
    # Check for proxy patterns
    if "6080604052" in bytecode and "360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc" in bytecode:
        analysis["likely_contract_type"] = "Likely Proxy Contract"
        analysis["confidence"] = 0.7
        analysis["patterns_detected"].append("Proxy pattern detected")
    
    # Check for upgradeable contracts
    if "4e487b71" in bytecode:  # OpenZeppelin upgradeable pattern
        analysis["patterns_detected"].append("Upgradeable contract pattern")
        analysis["confidence"] = min(analysis["confidence"] + 0.2, 1.0)
    
    analysis["detected_functions"] = detected_functions
    analysis["function_count"] = len(detected_functions)
    
    return analysis


def analyze_contract_security(source_code):
    """Basic security analysis of contract source code"""
    issues = []
    
    # Check for reentrancy vulnerabilities
    if "call.value" in source_code and "ReentrancyGuard" not in source_code:
        issues.append({
            "severity": "High",
            "issue": "Potential reentrancy vulnerability",
            "description": "Contract uses call.value without ReentrancyGuard or checks-effects-interactions pattern"
        })
    
    # Check for tx.origin usage
    if "tx.origin" in source_code:
        issues.append({
            "severity": "Medium",
            "issue": "tx.origin used for authentication",
            "description": "Using tx.origin for authentication can be exploited by phishing attacks"
        })
    
    # Check for unchecked external calls
    if (".call(" in source_code or ".delegatecall(" in source_code) and not any("require" in line and ".call" in line for line in source_code.split('\n')):
        issues.append({
            "severity": "Medium",
            "issue": "Unchecked external call",
            "description": "External calls without checking return value can lead to silent failures"
        })
    
    # Check for use of block.timestamp
    if "block.timestamp" in source_code or "now" in source_code:
        issues.append({
            "severity": "Low",
            "issue": "Timestamp dependence",
            "description": "Using block.timestamp for critical logic can be manipulated by miners"
        })
    
    # Check for self-destruct without access control
    if "selfdestruct" in source_code or "suicide" in source_code:
        issues.append({
            "severity": "High",
            "issue": "Unprotected self-destruct",
            "description": "Self-destruct functionality found - ensure it has proper access controls"
        })
    
    return {
        "issues_found": len(issues) > 0,
        "issues": issues
    }


def extract_function_signatures(abi):
    """Extract function signatures from contract ABI"""
    if not abi:
        return []
    
    functions = []
    for item in abi:
        if item.get("type") == "function":
            inputs = item.get("inputs", [])
            outputs = item.get("outputs", [])
            
            input_types = [inp.get("type", "") for inp in inputs]
            output_types = [out.get("type", "") for out in outputs]
            
            signature = f"{item.get('name', '')}({','.join(input_types)})"
            if output_types:
                signature += f" returns ({','.join(output_types)})"
            
            functions.append({
                "name": item.get("name", ""),
                "signature": signature,
                "state_mutability": item.get("stateMutability", ""),
                "visibility": item.get("visibility", "public")
            })
    
    return functions


def extract_event_signatures(abi):
    """Extract event signatures from contract ABI"""
    if not abi:
        return []
    
    events = []
    for item in abi:
        if item.get("type") == "event":
            inputs = item.get("inputs", [])
            input_types = [inp.get("type", "") for inp in inputs]
            
            signature = f"{item.get('name', '')}({','.join(input_types)})"
            
            events.append({
                "name": item.get("name", ""),
                "signature": signature
            })
    
    return events
