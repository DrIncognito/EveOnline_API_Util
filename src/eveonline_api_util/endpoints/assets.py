"""
Assets endpoint module for EVE Online ESI API

This module provides access to asset-related endpoints including
character and corporation asset lists, names, and locations.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class AssetsEndpoint:
    """
    Assets endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character and corporation assets,
    their names, and locations.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize assets endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized AssetsEndpoint")
    
    def get_character_assets(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's assets (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character's assets
        """
        endpoint = f'/characters/{character_id}/assets/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_asset_locations(self, character_id: str, item_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get locations of specific character assets (requires authentication).
        
        Args:
            character_id: Character ID as string
            item_ids: List of item IDs to get locations for
            
        Returns:
            List of asset locations
        """
        endpoint = f'/characters/{character_id}/assets/locations/'
        return self.client.post(endpoint, character_id=character_id, json_data=item_ids)
    
    def get_character_asset_names(self, character_id: str, item_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get names of specific character assets (requires authentication).
        
        Args:
            character_id: Character ID as string
            item_ids: List of item IDs to get names for
            
        Returns:
            List of asset names
        """
        endpoint = f'/characters/{character_id}/assets/names/'
        return self.client.post(endpoint, character_id=character_id, json_data=item_ids)
    
    def get_corporation_assets(self, corporation_id: int, character_id: str,
                             page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation's assets (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation's assets
        """
        endpoint = f'/corporations/{corporation_id}/assets/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_asset_locations(self, corporation_id: int, character_id: str,
                                      item_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get locations of specific corporation assets (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            item_ids: List of item IDs to get locations for
            
        Returns:
            List of asset locations
        """
        endpoint = f'/corporations/{corporation_id}/assets/locations/'
        return self.client.post(endpoint, character_id=character_id, json_data=item_ids)
    
    def get_corporation_asset_names(self, corporation_id: int, character_id: str,
                                  item_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get names of specific corporation assets (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            item_ids: List of item IDs to get names for
            
        Returns:
            List of asset names
        """
        endpoint = f'/corporations/{corporation_id}/assets/names/'
        return self.client.post(endpoint, character_id=character_id, json_data=item_ids)
