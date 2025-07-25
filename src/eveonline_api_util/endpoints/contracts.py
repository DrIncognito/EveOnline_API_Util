"""
Contracts endpoint module for EVE Online ESI API

This module provides access to contract-related endpoints including
character and corporation contracts, contract items, and bids.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class ContractsEndpoint:
    """
    Contracts endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character and corporation contracts,
    contract details, items, and bids.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize contracts endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized ContractsEndpoint")
    
    def get_character_contracts(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character contracts (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character contracts
        """
        endpoint = f'/characters/{character_id}/contracts/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_contract_bids(self, character_id: str, contract_id: int) -> List[Dict[str, Any]]:
        """
        Get character contract bids (requires authentication).
        
        Args:
            character_id: Character ID as string
            contract_id: Contract ID
            
        Returns:
            List of contract bids
        """
        endpoint = f'/characters/{character_id}/contracts/{contract_id}/bids/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_contract_items(self, character_id: str, contract_id: int) -> List[Dict[str, Any]]:
        """
        Get character contract items (requires authentication).
        
        Args:
            character_id: Character ID as string
            contract_id: Contract ID
            
        Returns:
            List of contract items
        """
        endpoint = f'/characters/{character_id}/contracts/{contract_id}/items/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_contracts(self, corporation_id: int, character_id: str,
                                page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation contracts (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation contracts
        """
        endpoint = f'/corporations/{corporation_id}/contracts/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_contract_bids(self, corporation_id: int, contract_id: int,
                                    character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation contract bids (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            contract_id: Contract ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of contract bids
        """
        endpoint = f'/corporations/{corporation_id}/contracts/{contract_id}/bids/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_contract_items(self, corporation_id: int, contract_id: int,
                                     character_id: str) -> List[Dict[str, Any]]:
        """
        Get corporation contract items (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            contract_id: Contract ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            List of contract items
        """
        endpoint = f'/corporations/{corporation_id}/contracts/{contract_id}/items/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_public_contracts(self, region_id: int, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get public contracts for a region.
        
        Args:
            region_id: Region ID
            page: Page number for pagination
            
        Returns:
            List of public contracts
        """
        endpoint = f'/contracts/public/{region_id}/'
        params = {'page': page}
        return self.client.get(endpoint, params=params)
    
    def get_public_contract_bids(self, contract_id: int, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get public contract bids.
        
        Args:
            contract_id: Contract ID
            page: Page number for pagination
            
        Returns:
            List of contract bids
        """
        endpoint = f'/contracts/public/bids/{contract_id}/'
        params = {'page': page}
        return self.client.get(endpoint, params=params)
    
    def get_public_contract_items(self, contract_id: int, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get public contract items.
        
        Args:
            contract_id: Contract ID
            page: Page number for pagination
            
        Returns:
            List of contract items
        """
        endpoint = f'/contracts/public/items/{contract_id}/'
        params = {'page': page}
        return self.client.get(endpoint, params=params)
