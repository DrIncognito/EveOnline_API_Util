"""
Industry endpoint module for EVE Online ESI API

This module provides access to industry-related endpoints including
industry jobs, facilities, and blueprints.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class IndustryEndpoint:
    """
    Industry endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing industry jobs, facilities,
    and system cost indices.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize industry endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized IndustryEndpoint")
    
    def get_character_industry_jobs(self, character_id: str, include_completed: bool = False) -> List[Dict[str, Any]]:
        """
        Get character's industry jobs (requires authentication).
        
        Args:
            character_id: Character ID as string
            include_completed: Include completed jobs
            
        Returns:
            List of character's industry jobs
        """
        endpoint = f'/characters/{character_id}/industry/jobs/'
        params = {'include_completed': include_completed}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_mining(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's mining ledger (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character's mining activities
        """
        endpoint = f'/characters/{character_id}/mining/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_industry_jobs(self, corporation_id: int, character_id: str,
                                    include_completed: bool = False, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation's industry jobs (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            include_completed: Include completed jobs
            page: Page number for pagination
            
        Returns:
            List of corporation's industry jobs
        """
        endpoint = f'/corporations/{corporation_id}/industry/jobs/'
        params = {'include_completed': include_completed, 'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_mining_extractions(self, corporation_id: int, character_id: str,
                                         page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation's mining extractions (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation's mining extractions
        """
        endpoint = f'/corporations/{corporation_id}/mining/extractions/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_mining_observers(self, corporation_id: int, character_id: str,
                                       page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation's mining observers (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation's mining observers
        """
        endpoint = f'/corporations/{corporation_id}/mining/observers/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_mining_observer_details(self, corporation_id: int, observer_id: int,
                                              character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get mining observer details (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            observer_id: Observer ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of observer mining details
        """
        endpoint = f'/corporations/{corporation_id}/mining/observers/{observer_id}/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_industry_facilities(self) -> List[Dict[str, Any]]:
        """
        Get industry facilities.
        
        Returns:
            List of industry facilities
        """
        return self.client.get('/industry/facilities/')
    
    def get_industry_systems(self) -> List[Dict[str, Any]]:
        """
        Get industry system cost indices.
        
        Returns:
            List of systems with cost indices
        """
        return self.client.get('/industry/systems/')
