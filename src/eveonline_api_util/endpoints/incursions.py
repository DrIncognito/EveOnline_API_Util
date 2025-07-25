"""
Incursions endpoint module for EVE Online ESI API

This module provides access to incursion-related endpoints.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class IncursionsEndpoint:
    """
    Incursions endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing incursion information.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize incursions endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized IncursionsEndpoint")
    
    def get_incursions(self) -> List[Dict[str, Any]]:
        """
        Get incursions.
        
        Returns:
            List of active incursions
        """
        return self.client.get('/incursions/')
