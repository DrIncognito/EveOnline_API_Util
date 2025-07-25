"""
Wallet endpoint module for EVE Online ESI API

This module provides access to wallet-related endpoints including
character and corporation wallet information, transactions, and journal entries.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class WalletEndpoint:
    """
    Wallet endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing wallet balance, transactions,
    and journal entries for characters and corporations.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize wallet endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized WalletEndpoint")
    
    def get_character_wallet_balance(self, character_id: str) -> float:
        """
        Get character's wallet balance (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Wallet balance in ISK
        """
        endpoint = f'/characters/{character_id}/wallet/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_wallet_journal(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's wallet journal (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of wallet journal entries
        """
        endpoint = f'/characters/{character_id}/wallet/journal/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_wallet_transactions(self, character_id: str, from_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get character's wallet transactions (requires authentication).
        
        Args:
            character_id: Character ID as string
            from_id: Only show transactions after this transaction ID
            
        Returns:
            List of wallet transactions
        """
        endpoint = f'/characters/{character_id}/wallet/transactions/'
        params = {}
        if from_id:
            params['from_id'] = from_id
            
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_wallets(self, corporation_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get corporation wallet information (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            List of corporation wallet divisions
        """
        endpoint = f'/corporations/{corporation_id}/wallets/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_wallet_journal(self, corporation_id: int, division: int,
                                     character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation wallet journal (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            division: Wallet division (1-7)
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation wallet journal entries
        """
        endpoint = f'/corporations/{corporation_id}/wallets/{division}/journal/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_wallet_transactions(self, corporation_id: int, division: int,
                                          character_id: str, from_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get corporation wallet transactions (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            division: Wallet division (1-7)
            character_id: Character ID as string (must have corp roles)
            from_id: Only show transactions after this transaction ID
            
        Returns:
            List of corporation wallet transactions
        """
        endpoint = f'/corporations/{corporation_id}/wallets/{division}/transactions/'
        params = {}
        if from_id:
            params['from_id'] = from_id
            
        return self.client.get(endpoint, character_id=character_id, params=params)
