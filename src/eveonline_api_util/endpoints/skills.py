"""
Skills endpoint module for EVE Online ESI API

This module provides access to skill-related endpoints including
character skills, skill queue, and attributes.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class SkillsEndpoint:
    """
    Skills endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character skills, skill queue,
    and attributes information.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize skills endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized SkillsEndpoint")
    
    def get_character_attributes(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's attributes (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Character's attributes
        """
        endpoint = f'/characters/{character_id}/attributes/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_skills(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's skills (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Character's skills and skill points
        """
        endpoint = f'/characters/{character_id}/skills/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_skillqueue(self, character_id: str) -> List[Dict[str, Any]]:
        """
        Get character's skill queue (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Character's skill queue
        """
        endpoint = f'/characters/{character_id}/skillqueue/'
        return self.client.get(endpoint, character_id=character_id)
