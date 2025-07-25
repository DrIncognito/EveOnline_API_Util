"""
Sovereignty endpoint module for EVE Online ESI API

This module provides access to sovereignty-related endpoints including
sovereignty campaigns, map, and structures.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class SovereigntyEndpoint:
    """
    Sovereignty endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing sovereignty information including
    campaigns, map data, and structures.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize sovereignty endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized SovereigntyEndpoint")
    
    def get_sovereignty_campaigns(self) -> List[Dict[str, Any]]:
        """
        Get sovereignty campaigns.
        
        Returns:
            List of active sovereignty campaigns
        """
        return self.client.get('/sovereignty/campaigns/')
    
    def get_sovereignty_map(self) -> List[Dict[str, Any]]:
        """
        Get sovereignty map.
        
        Returns:
            List of systems with sovereignty information
        """
        return self.client.get('/sovereignty/map/')
    
    def get_sovereignty_structures(self) -> List[Dict[str, Any]]:
        """
        Get sovereignty structures.
        
        Returns:
            List of sovereignty structures
        """
        return self.client.get('/sovereignty/structures/')
