"""
Corporation endpoint module for EVE Online ESI API

This module provides access to corporation-related endpoints including
corporation information, members, structures, and various corporation data.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class CorporationEndpoint:
    """
    Corporation endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing corporation information, members,
    structures, and other corporation-related data.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize corporation endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized CorporationEndpoint")
    
    def get_corporation_info(self, corporation_id: int) -> Dict[str, Any]:
        """
        Get public information about a corporation.
        
        Args:
            corporation_id: Corporation ID
            
        Returns:
            Corporation information
        """
        return self.client.get(f'/corporations/{corporation_id}/')
    
    def get_corporation_alliance_history(self, corporation_id: int) -> List[Dict[str, Any]]:
        """
        Get corporation's alliance history.
        
        Args:
            corporation_id: Corporation ID
            
        Returns:
            List of alliance history entries
        """
        return self.client.get(f'/corporations/{corporation_id}/alliancehistory/')
    
    def get_corporation_blueprints(self, corporation_id: int, character_id: str,
                                 page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation blueprints (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation blueprints
        """
        endpoint = f'/corporations/{corporation_id}/blueprints/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_contacts(self, corporation_id: int, character_id: str,
                               page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation contacts (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation contacts
        """
        endpoint = f'/corporations/{corporation_id}/contacts/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_contact_labels(self, corporation_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get corporation contact labels (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            List of corporation contact labels
        """
        endpoint = f'/corporations/{corporation_id}/contacts/labels/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_containers_logs(self, corporation_id: int, character_id: str,
                                      page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation container logs (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of container log entries
        """
        endpoint = f'/corporations/{corporation_id}/containers/logs/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_divisions(self, corporation_id: int, character_id: str) -> Dict[str, Any]:
        """
        Get corporation divisions (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            Corporation divisions information
        """
        endpoint = f'/corporations/{corporation_id}/divisions/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_facilities(self, corporation_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get corporation facilities (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            List of corporation facilities
        """
        endpoint = f'/corporations/{corporation_id}/facilities/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_icons(self, corporation_id: int) -> Dict[str, Any]:
        """
        Get corporation icon URLs.
        
        Args:
            corporation_id: Corporation ID
            
        Returns:
            Corporation icon URLs for different sizes
        """
        return self.client.get(f'/corporations/{corporation_id}/icons/')
    
    def get_corporation_medals(self, corporation_id: int, character_id: str,
                             page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation medals (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation medals
        """
        endpoint = f'/corporations/{corporation_id}/medals/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_medals_issued(self, corporation_id: int, character_id: str,
                                    page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation medals issued (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of issued corporation medals
        """
        endpoint = f'/corporations/{corporation_id}/medals/issued/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_members(self, corporation_id: int, character_id: str) -> List[int]:
        """
        Get corporation members (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            List of member character IDs
        """
        endpoint = f'/corporations/{corporation_id}/members/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_members_limit(self, corporation_id: int, character_id: str) -> int:
        """
        Get corporation member limit (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            Corporation member limit
        """
        endpoint = f'/corporations/{corporation_id}/members/limit/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_members_titles(self, corporation_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get corporation member titles (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            List of member titles
        """
        endpoint = f'/corporations/{corporation_id}/members/titles/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_membertracking(self, corporation_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get corporation member tracking (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            List of member tracking information
        """
        endpoint = f'/corporations/{corporation_id}/membertracking/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_roles(self, corporation_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get corporation roles (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            List of corporation roles
        """
        endpoint = f'/corporations/{corporation_id}/roles/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_corporation_roles_history(self, corporation_id: int, character_id: str,
                                    page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation roles history (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of role history entries
        """
        endpoint = f'/corporations/{corporation_id}/roles/history/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_shareholders(self, corporation_id: int, character_id: str,
                                   page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation shareholders (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation shareholders
        """
        endpoint = f'/corporations/{corporation_id}/shareholders/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_standings(self, corporation_id: int, character_id: str,
                                page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation standings (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation standings
        """
        endpoint = f'/corporations/{corporation_id}/standings/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_starbases(self, corporation_id: int, character_id: str,
                                page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation starbases (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation starbases
        """
        endpoint = f'/corporations/{corporation_id}/starbases/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_starbase_detail(self, corporation_id: int, starbase_id: int,
                                      system_id: int, character_id: str) -> Dict[str, Any]:
        """
        Get starbase details (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            starbase_id: Starbase ID
            system_id: Solar system ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            Starbase details
        """
        endpoint = f'/corporations/{corporation_id}/starbases/{starbase_id}/'
        params = {'system_id': system_id}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_structures(self, corporation_id: int, character_id: str,
                                 page: int = 1, language: str = 'en') -> List[Dict[str, Any]]:
        """
        Get corporation structures (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            language: Language for localized strings
            
        Returns:
            List of corporation structures
        """
        endpoint = f'/corporations/{corporation_id}/structures/'
        params = {'page': page, 'language': language}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_titles(self, corporation_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get corporation titles (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            
        Returns:
            List of corporation titles
        """
        endpoint = f'/corporations/{corporation_id}/titles/'
        return self.client.get(endpoint, character_id=character_id)
