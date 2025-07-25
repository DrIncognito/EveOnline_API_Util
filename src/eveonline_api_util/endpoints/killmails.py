"""
Killmails endpoint module for EVE Online ESI API

This module provides access to killmail-related endpoints including
character and corporation killmails and killmail details.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class KillmailsEndpoint:
    """
    Killmails endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character and corporation killmails
    and retrieving detailed killmail information.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize killmails endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized KillmailsEndpoint")
    
    def get_character_killmails_recent(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's recent killmails (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character's recent killmails
        """
        endpoint = f'/characters/{character_id}/killmails/recent/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_killmails_recent(self, corporation_id: int, character_id: str,
                                       page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation's recent killmails (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation's recent killmails
        """
        endpoint = f'/corporations/{corporation_id}/killmails/recent/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_killmail(self, killmail_id: int, killmail_hash: str) -> Dict[str, Any]:
        """
        Get killmail details.
        
        Args:
            killmail_id: Killmail ID
            killmail_hash: Killmail hash for verification
            
        Returns:
            Killmail details
        """
        endpoint = f'/killmails/{killmail_id}/{killmail_hash}/'
        return self.client.get(endpoint)
