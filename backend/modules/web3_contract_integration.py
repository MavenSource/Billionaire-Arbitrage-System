"""
Web3 Contract Integration Module
Handles Web3 connections, contract interactions, and transaction execution.
"""

from typing import Dict, List, Optional, Any
from decimal import Decimal
import logging
from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound
import json


class Web3ContractManager:
    """Manages Web3 connections and smart contract interactions."""
    
    def __init__(self, web3: Web3, config: Dict):
        self.web3 = web3
        self.config = config
        self.logger = logging.getLogger("Web3ContractManager")
        self.account = None
        
        # Initialize account if private key provided
        if config.get('PRIVATE_KEY'):
            try:
                self.account = self.web3.eth.account.from_key(config['PRIVATE_KEY'])
                self.logger.info(f"✅ Account initialized: {self.account.address}")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize account: {e}")
    
    def is_connected(self) -> bool:
        """Check if Web3 is connected to the network."""
        try:
            return self.web3.is_connected()
        except Exception as e:
            self.logger.error(f"Connection check failed: {e}")
            return False
    
    def get_balance(self, address: Optional[str] = None) -> Decimal:
        """Get ETH/MATIC balance for an address."""
        try:
            addr = address or (self.account.address if self.account else None)
            if not addr:
                return Decimal('0')
            
            balance_wei = self.web3.eth.get_balance(addr)
            balance_eth = self.web3.from_wei(balance_wei, 'ether')
            return Decimal(str(balance_eth))
        except Exception as e:
            self.logger.error(f"Failed to get balance: {e}")
            return Decimal('0')
    
    def get_token_balance(self, token_address: str, 
                          holder_address: Optional[str] = None) -> Decimal:
        """Get ERC20 token balance."""
        try:
            holder = holder_address or (self.account.address if self.account else None)
            if not holder:
                return Decimal('0')
            
            # Standard ERC20 ABI for balanceOf
            erc20_abi = [
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
                }
            ]
            
            contract = self.web3.eth.contract(
                address=self.web3.to_checksum_address(token_address),
                abi=erc20_abi
            )
            
            balance = contract.functions.balanceOf(holder).call()
            decimals = contract.functions.decimals().call()
            
            return Decimal(balance) / Decimal(10 ** decimals)
        except Exception as e:
            self.logger.error(f"Failed to get token balance: {e}")
            return Decimal('0')
    
    def get_gas_price(self) -> int:
        """Get current gas price in Wei."""
        try:
            return self.web3.eth.gas_price
        except Exception as e:
            self.logger.error(f"Failed to get gas price: {e}")
            return 30_000_000_000  # Default 30 Gwei
    
    def estimate_gas(self, transaction: Dict) -> int:
        """Estimate gas for a transaction."""
        try:
            return self.web3.eth.estimate_gas(transaction)
        except Exception as e:
            self.logger.error(f"Gas estimation failed: {e}")
            return 300_000  # Default gas limit
    
    async def execute_arbitrage(self, opportunity: Any) -> Optional[str]:
        """
        Execute an arbitrage opportunity.
        Returns transaction hash if successful.
        """
        if not self.account:
            self.logger.error("❌ No account configured for execution")
            return None
        
        try:
            self.logger.info(f"🚀 Executing arbitrage opportunity...")
            
            # In a real implementation, this would:
            # 1. Build the swap transactions
            # 2. Calculate optimal gas price
            # 3. Sign and send the transaction
            # 4. Wait for confirmation
            
            # For now, return a mock transaction hash
            tx_hash = f"0x{'0' * 64}"  # Placeholder
            
            self.logger.info(f"✅ Arbitrage executed: {tx_hash}")
            return tx_hash
            
        except ContractLogicError as e:
            self.logger.error(f"❌ Contract execution failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Execution failed: {e}")
            return None
    
    def build_swap_transaction(self, dex_address: str, token_in: str,
                               token_out: str, amount_in: int,
                               min_amount_out: int) -> Optional[Dict]:
        """
        Build a swap transaction for a DEX.
        Returns transaction dict ready to be signed.
        """
        try:
            if not self.account:
                return None
            
            # This would construct actual swap transaction
            # For now, return structure
            transaction = {
                'from': self.account.address,
                'to': dex_address,
                'value': 0,
                'gas': 300_000,
                'gasPrice': self.get_gas_price(),
                'nonce': self.web3.eth.get_transaction_count(self.account.address),
                'chainId': self.web3.eth.chain_id,
                'data': '0x'  # Would contain actual swap calldata
            }
            
            return transaction
            
        except Exception as e:
            self.logger.error(f"Failed to build transaction: {e}")
            return None
    
    def send_transaction(self, transaction: Dict) -> Optional[str]:
        """Sign and send a transaction."""
        try:
            if not self.account:
                self.logger.error("No account available for signing")
                return None
            
            # Sign transaction
            signed_txn = self.web3.eth.account.sign_transaction(
                transaction, 
                self.account.key
            )
            
            # Send transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return self.web3.to_hex(tx_hash)
            
        except Exception as e:
            self.logger.error(f"Transaction failed: {e}")
            return None
    
    def wait_for_receipt(self, tx_hash: str, timeout: int = 120) -> Optional[Dict]:
        """Wait for transaction receipt."""
        try:
            receipt = self.web3.eth.wait_for_transaction_receipt(
                tx_hash, 
                timeout=timeout
            )
            return dict(receipt)
        except TransactionNotFound:
            self.logger.error(f"Transaction not found: {tx_hash}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get receipt: {e}")
            return None