"""
Alliance endpoint module for EVE Online ESI API

This module provides access to alliance-related endpoints including
alliance information, corporations, and contacts.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class AllianceEndpoint:
    """
    Alliance endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing alliance information, member corporations,
    and alliance-related data.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize alliance endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized AllianceEndpoint")
    
    def get_alliances(self) -> List[int]:
        """
        Get a list of all alliance IDs.
        
        Returns:
            List of alliance IDs
        """
        return self.client.get('/alliances/')
    
    def get_alliance_info(self, alliance_id: int) -> Dict[str, Any]:
        """
        Get public information about an alliance.
        
        Args:
            alliance_id: Alliance ID
            
        Returns:
            Alliance information
        """
        return self.client.get(f'/alliances/{alliance_id}/')
    
    def get_alliance_corporations(self, alliance_id: int) -> List[int]:
        """
        Get member corporations of an alliance.
        
        Args:
            alliance_id: Alliance ID
            
        Returns:
            List of corporation IDs in the alliance
        """
        return self.client.get(f'/alliances/{alliance_id}/corporations/')
    
    def get_alliance_icon(self, alliance_id: int) -> Dict[str, Any]:
        """
        Get alliance icon URLs.
        
        Args:
            alliance_id: Alliance ID
            
        Returns:
            Alliance icon URLs for different sizes
        """
        return self.client.get(f'/alliances/{alliance_id}/icons/')
    
    def get_alliance_contacts(self, alliance_id: int, character_id: str, 
                            page: int = 1) -> List[Dict[str, Any]]:
        """
        Get alliance contacts (requires authentication and alliance role).
        
        Args:
            alliance_id: Alliance ID
            character_id: Character ID as string (must have alliance roles)
            page: Page number for pagination
            
        Returns:
            List of alliance contacts
        """
        endpoint = f'/alliances/{alliance_id}/contacts/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_alliance_contact_labels(self, alliance_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get alliance contact labels (requires authentication and alliance role).
        
        Args:
            alliance_id: Alliance ID
            character_id: Character ID as string (must have alliance roles)
            
        Returns:
            List of alliance contact labels
        """
        endpoint = f'/alliances/{alliance_id}/contacts/labels/'
        return self.client.get(endpoint, character_id=character_id)
