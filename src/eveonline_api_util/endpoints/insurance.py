"""
Insurance endpoint module for EVE Online ESI API

This module provides access to insurance-related endpoints.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class InsuranceEndpoint:
    """
    Insurance endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing insurance information.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize insurance endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized InsuranceEndpoint")
    
    def get_insurance_prices(self, accept_language: str = 'en') -> List[Dict[str, Any]]:
        """
        Get insurance prices.
        
        Args:
            accept_language: Language to return names in
            
        Returns:
            List of insurance prices for ship types
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get('/insurance/prices/', headers=headers)
