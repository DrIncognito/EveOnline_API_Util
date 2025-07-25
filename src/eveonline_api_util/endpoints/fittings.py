"""
Fittings endpoint module for EVE Online ESI API

This module provides access to fitting-related endpoints including
character fittings management.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class FittingsEndpoint:
    """
    Fittings endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character fittings.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize fittings endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized FittingsEndpoint")
    
    def get_character_fittings(self, character_id: str) -> List[Dict[str, Any]]:
        """
        Get character's saved fittings (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            List of character's saved fittings
        """
        endpoint = f'/characters/{character_id}/fittings/'
        return self.client.get(endpoint, character_id=character_id)
    
    def post_character_fitting(self, character_id: str, fitting_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new fitting (requires authentication).
        
        Args:
            character_id: Character ID as string
            fitting_data: Fitting data including name, ship_type_id, and items
            
        Returns:
            Created fitting information
        """
        endpoint = f'/characters/{character_id}/fittings/'
        return self.client.post(endpoint, character_id=character_id, json_data=fitting_data)
    
    def delete_character_fitting(self, character_id: str, fitting_id: int) -> None:
        """
        Delete a fitting (requires authentication).
        
        Args:
            character_id: Character ID as string
            fitting_id: Fitting ID to delete
        """
        endpoint = f'/characters/{character_id}/fittings/{fitting_id}/'
        self.client.delete(endpoint, character_id=character_id)
