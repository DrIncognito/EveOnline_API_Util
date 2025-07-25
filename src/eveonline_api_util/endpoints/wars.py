"""
Wars endpoint module for EVE Online ESI API

This module provides access to war-related endpoints including
active wars, war details, and killmails.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class WarsEndpoint:
    """
    Wars endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing war information including
    active wars, war details, and war killmails.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize wars endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized WarsEndpoint")
    
    def get_wars(self, max_war_id: Optional[int] = None) -> List[int]:
        """
        Get all wars.
        
        Args:
            max_war_id: Only return wars with ID smaller than this
            
        Returns:
            List of war IDs
        """
        params = {}
        if max_war_id:
            params['max_war_id'] = max_war_id
        return self.client.get('/wars/', params=params)
    
    def get_war(self, war_id: int) -> Dict[str, Any]:
        """
        Get information about a war.
        
        Args:
            war_id: War ID
            
        Returns:
            War information
        """
        return self.client.get(f'/wars/{war_id}/')
    
    def get_war_killmails(self, war_id: int, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get killmails for a war.
        
        Args:
            war_id: War ID
            page: Page number for pagination
            
        Returns:
            List of war killmails
        """
        params = {'page': page}
        return self.client.get(f'/wars/{war_id}/killmails/', params=params)
