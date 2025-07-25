"""
Bookmarks endpoint module for EVE Online ESI API

This module provides access to bookmark-related endpoints including
character and corporation bookmarks and folders.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class BookmarksEndpoint:
    """
    Bookmarks endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character and corporation
    bookmarks and bookmark folders.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize bookmarks endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized BookmarksEndpoint")
    
    def get_character_bookmarks(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's bookmarks (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character's bookmarks
        """
        endpoint = f'/characters/{character_id}/bookmarks/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_bookmark_folders(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's bookmark folders (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character's bookmark folders
        """
        endpoint = f'/characters/{character_id}/bookmarks/folders/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_bookmarks(self, corporation_id: int, character_id: str,
                                page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation's bookmarks (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation's bookmarks
        """
        endpoint = f'/corporations/{corporation_id}/bookmarks/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_bookmark_folders(self, corporation_id: int, character_id: str,
                                       page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation's bookmark folders (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation's bookmark folders
        """
        endpoint = f'/corporations/{corporation_id}/bookmarks/folders/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
