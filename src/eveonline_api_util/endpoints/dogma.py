"""
Dogma endpoint module for EVE Online ESI API

This module provides access to dogma-related endpoints including
attributes, effects, and dynamic item information.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class DogmaEndpoint:
    """
    Dogma endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing dogma attributes, effects,
    and dynamic item information.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize dogma endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized DogmaEndpoint")
    
    def get_dogma_attributes(self) -> List[int]:
        """
        Get dogma attributes.
        
        Returns:
            List of attribute IDs
        """
        return self.client.get('/dogma/attributes/')
    
    def get_dogma_attribute(self, attribute_id: int) -> Dict[str, Any]:
        """
        Get information about a dogma attribute.
        
        Args:
            attribute_id: Attribute ID
            
        Returns:
            Attribute information
        """
        return self.client.get(f'/dogma/attributes/{attribute_id}/')
    
    def get_dogma_effects(self) -> List[int]:
        """
        Get dogma effects.
        
        Returns:
            List of effect IDs
        """
        return self.client.get('/dogma/effects/')
    
    def get_dogma_effect(self, effect_id: int) -> Dict[str, Any]:
        """
        Get information about a dogma effect.
        
        Args:
            effect_id: Effect ID
            
        Returns:
            Effect information
        """
        return self.client.get(f'/dogma/effects/{effect_id}/')
    
    def post_dogma_dynamic_items(self, character_id: str, item_id: int, type_id: int) -> Dict[str, Any]:
        """
        Get dynamic item information (requires authentication).
        
        Args:
            character_id: Character ID as string
            item_id: Item ID
            type_id: Type ID
            
        Returns:
            Dynamic item information with attributes and effects
        """
        endpoint = f'/dogma/dynamic/items/{type_id}/{item_id}/'
        return self.client.get(endpoint, character_id=character_id)
