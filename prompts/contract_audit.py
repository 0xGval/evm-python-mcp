"""
Contract Audit Prompts

Professional prompt templates for smart contract security analysis and auditing.
"""

def contract_security_audit_prompt():
    """
    Comprehensive security audit prompt for smart contracts.
    
    Returns:
        str: Formatted prompt template for contract security analysis
    """
    return """
🔍 **SMART CONTRACT SECURITY AUDIT**

Please analyze the following smart contract and provide a comprehensive security audit:

**Contract Details:**
- Address: {address}
- Network: {network}
- Contract Name: {contract_name}
- Verification Status: {is_verified}

**Required Analysis:**

## 1. **Contract Overview**
- Contract type and primary purpose
- Verification status and source code availability
- Deployed state vs source code differences (if proxy/upgradeable)
- Network-specific considerations

## 2. **Security Assessment**
### Critical Issues (🔴)
- Reentrancy vulnerabilities
- Access control bypasses
- Integer overflow/underflow
- Unprotected critical functions
- Self-destruct vulnerabilities

### Medium Risk Issues (🟡)
- Centralization risks
- Upgrade mechanisms
- External call dependencies
- Gas optimization issues
- Event emission gaps

### Low Risk Observations (🟢)
- Code quality issues
- Documentation gaps
- Best practice deviations
- Gas efficiency improvements

## 3. **Tokenomics Analysis** (if applicable)
- Token supply and distribution
- Tax mechanisms and rates
- Access controls and permissions
- Upgrade patterns and risks
- Liquidity management

## 4. **Risk Rating**
- **Overall Risk Level:** [LOW/MEDIUM/HIGH/CRITICAL]
- **Specific Concerns:** List top 3-5 risks
- **Recommendations:** Actionable security improvements

## 5. **User Guidance**
- **Safe to interact with?** [YES/NO/CAUTION]
- **What to watch for:** Key risks for users
- **Red flags to avoid:** Specific warning signs
- **Best practices:** How to interact safely

## 6. **Technical Details**
- Standards compliance (ERC20, ERC721, etc.)
- Function signatures and capabilities
- Event emissions and logging
- Gas consumption patterns

**Format the output as a professional security audit report with clear sections, risk ratings, and actionable recommendations. Use emojis and formatting to make it readable and professional.**
"""


def contract_quick_analysis_prompt():
    """
    Quick contract analysis prompt for rapid assessment.
    
    Returns:
        str: Formatted prompt template for quick contract analysis
    """
    return """
⚡ **QUICK CONTRACT ANALYSIS**

Provide a rapid assessment of this contract:

**Contract:** {address} on {network}
**Name:** {contract_name}

**Quick Assessment:**
1. **Contract Type:** [Token/DeFi/NFT/Other]
2. **Risk Level:** [LOW/MEDIUM/HIGH]
3. **Key Features:** [List 3-5 main functions]
4. **Main Risks:** [Top 3 concerns]
5. **Safe to Use?** [YES/NO/CAUTION]

**One-liner Summary:** [Brief description of what this contract does and main risk]

Keep it concise but informative!
"""


def contract_deep_dive_prompt():
    """
    Deep dive analysis prompt for comprehensive contract examination.
    
    Returns:
        str: Formatted prompt template for deep contract analysis
    """
    return """
🔬 **DEEP DIVE CONTRACT ANALYSIS**

Conduct a thorough examination of this contract:

**Contract:** {address} on {network}
**Name:** {contract_name}

**Deep Analysis Required:**

## 1. **Architecture Analysis**
- Design patterns used
- Inheritance hierarchy
- Interface implementations
- Upgrade mechanisms
- Proxy patterns

## 2. **Code Quality Assessment**
- Solidity version and compiler
- Code organization and structure
- Documentation coverage
- Testing considerations
- Gas optimization

## 3. **Security Deep Dive**
- Access control mechanisms
- Reentrancy protection
- Integer safety
- External call safety
- State management
- Event emission completeness

## 4. **Economic Security**
- Tokenomics design
- Incentive mechanisms
- Governance structures
- Economic attack vectors
- Value flow analysis

## 5. **Integration Analysis**
- DEX compatibility
- Bridge interactions
- Oracle dependencies
- External protocol risks
- Network-specific considerations

## 6. **Operational Security**
- Admin controls
- Emergency procedures
- Upgrade processes
- Key management
- Monitoring capabilities

**Provide detailed technical analysis with code references, risk assessments, and comprehensive recommendations.**
"""
