"""
Locations endpoint module for EVE Online ESI API

This module provides access to location-related endpoints including
character location, ship, and online status.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class LocationsEndpoint:
    """
    Locations endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character location information
    including current location, ship, and online status.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize locations endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized LocationsEndpoint")
    
    def get_character_location(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's current location (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Character's current location
        """
        endpoint = f'/characters/{character_id}/location/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_online(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's online status (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Character's online status
        """
        endpoint = f'/characters/{character_id}/online/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_ship(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's current ship (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Character's current ship information
        """
        endpoint = f'/characters/{character_id}/ship/'
        return self.client.get(endpoint, character_id=character_id)
