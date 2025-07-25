"""
Character endpoint module for EVE Online ESI API

This module provides access to character-related endpoints including
character information, skills, assets, and other character-specific data.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class CharacterEndpoint:
    """
    Character endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character information, skills,
    assets, and other character-specific endpoints.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize character endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized CharacterEndpoint")
    
    def get_character_public_info(self, character_id: int) -> Dict[str, Any]:
        """
        Get public information about a character.
        
        Args:
            character_id: Character ID
            
        Returns:
            Character public information
        """
        endpoint = f'/characters/{character_id}/'
        return self.client.get(endpoint)
    
    def get_character_portrait(self, character_id: int) -> Dict[str, Any]:
        """
        Get character portrait URLs.
        
        Args:
            character_id: Character ID
            
        Returns:
            Portrait URLs for different sizes
        """
        endpoint = f'/characters/{character_id}/portrait/'
        return self.client.get(endpoint)
    
    def get_character_corporation_history(self, character_id: int) -> List[Dict[str, Any]]:
        """
        Get character's corporation history.
        
        Args:
            character_id: Character ID
            
        Returns:
            List of corporation history entries
        """
        endpoint = f'/characters/{character_id}/corporationhistory/'
        return self.client.get(endpoint)
    
    def get_character_attributes(self, character_id: str) -> Dict[str, Any]:
        """
        Get character attributes (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Character attributes
        """
        endpoint = f'/characters/{character_id}/attributes/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_implants(self, character_id: str) -> List[int]:
        """
        Get character's implants (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            List of implant type IDs
        """
        endpoint = f'/characters/{character_id}/implants/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_skills(self, character_id: str) -> Dict[str, Any]:
        """
        Get character skills (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Character skills information
        """
        endpoint = f'/characters/{character_id}/skills/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_skillqueue(self, character_id: str) -> List[Dict[str, Any]]:
        """
        Get character's skill queue (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            List of skills in training queue
        """
        endpoint = f'/characters/{character_id}/skillqueue/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_location(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's current location (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Character location information
        """
        endpoint = f'/characters/{character_id}/location/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_ship(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's current ship (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Current ship information
        """
        endpoint = f'/characters/{character_id}/ship/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_online(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's online status (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Online status information
        """
        endpoint = f'/characters/{character_id}/online/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_assets(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's assets (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character assets
        """
        endpoint = f'/characters/{character_id}/assets/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_blueprints(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's blueprints (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character blueprints
        """
        endpoint = f'/characters/{character_id}/blueprints/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_bookmarks(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's bookmarks (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character bookmarks
        """
        endpoint = f'/characters/{character_id}/bookmarks/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_contacts(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's contacts (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character contacts
        """
        endpoint = f'/characters/{character_id}/contacts/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def add_character_contacts(self, character_id: str, contact_ids: List[int], 
                              standing: float, label_ids: Optional[List[int]] = None,
                              watched: bool = False) -> None:
        """
        Add contacts for character (requires authentication).
        
        Args:
            character_id: Character ID as string
            contact_ids: List of character/corporation IDs to add
            standing: Standing value (-10.0 to 10.0)
            label_ids: Optional list of label IDs
            watched: Whether contacts should be watched
        """
        endpoint = f'/characters/{character_id}/contacts/'
        json_data = {
            'contact_ids': contact_ids,
            'standing': standing,
            'watched': watched
        }
        if label_ids:
            json_data['label_ids'] = label_ids
            
        return self.client.post(endpoint, character_id=character_id, json_data=json_data)
    
    def delete_character_contacts(self, character_id: str, contact_ids: List[int]) -> None:
        """
        Delete contacts for character (requires authentication).
        
        Args:
            character_id: Character ID as string
            contact_ids: List of contact IDs to delete
        """
        endpoint = f'/characters/{character_id}/contacts/'
        json_data = contact_ids
        return self.client.delete(endpoint, character_id=character_id, json_data=json_data)
