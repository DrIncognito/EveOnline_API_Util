"""
Fleet endpoint module for EVE Online ESI API

This module provides access to fleet-related endpoints including
fleet information, members, and fleet management operations.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class FleetEndpoint:
    """
    Fleet endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing fleet information, managing fleet
    members, and performing fleet operations.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize fleet endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized FleetEndpoint")
    
    def get_character_fleet_info(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's current fleet information (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Fleet information if character is in a fleet
        """
        endpoint = f'/characters/{character_id}/fleet/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_fleet_info(self, fleet_id: int, character_id: str) -> Dict[str, Any]:
        """
        Get fleet information (requires authentication and fleet role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet member)
            
        Returns:
            Fleet information
        """
        endpoint = f'/fleets/{fleet_id}/'
        return self.client.get(endpoint, character_id=character_id)
    
    def update_fleet_info(self, fleet_id: int, character_id: str,
                         is_free_move: Optional[bool] = None,
                         motd: Optional[str] = None) -> None:
        """
        Update fleet information (requires authentication and fleet commander role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet commander)
            is_free_move: Whether fleet members can move freely
            motd: Fleet message of the day
        """
        endpoint = f'/fleets/{fleet_id}/'
        json_data = {}
        
        if is_free_move is not None:
            json_data['is_free_move'] = is_free_move
        if motd is not None:
            json_data['motd'] = motd
            
        return self.client.put(endpoint, character_id=character_id, json_data=json_data)
    
    def get_fleet_members(self, fleet_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get fleet members (requires authentication and fleet role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet member)
            
        Returns:
            List of fleet members
        """
        endpoint = f'/fleets/{fleet_id}/members/'
        return self.client.get(endpoint, character_id=character_id)
    
    def invite_to_fleet(self, fleet_id: int, character_id: str,
                       invitee_id: int, role: str = 'squad_member',
                       squad_id: Optional[int] = None, wing_id: Optional[int] = None) -> None:
        """
        Invite character to fleet (requires authentication and fleet role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must have invite permissions)
            invitee_id: Character ID to invite
            role: Fleet role (squad_member, squad_commander, wing_commander, fleet_commander)
            squad_id: Squad ID (required for squad roles)
            wing_id: Wing ID (required for wing/squad roles)
        """
        endpoint = f'/fleets/{fleet_id}/members/'
        json_data = {
            'character_id': invitee_id,
            'role': role
        }
        
        if squad_id is not None:
            json_data['squad_id'] = squad_id
        if wing_id is not None:
            json_data['wing_id'] = wing_id
            
        return self.client.post(endpoint, character_id=character_id, json_data=json_data)
    
    def kick_from_fleet(self, fleet_id: int, character_id: str, member_id: int) -> None:
        """
        Kick member from fleet (requires authentication and fleet role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must have kick permissions)
            member_id: Character ID to kick from fleet
        """
        endpoint = f'/fleets/{fleet_id}/members/{member_id}/'
        return self.client.delete(endpoint, character_id=character_id)
    
    def move_fleet_member(self, fleet_id: int, character_id: str, member_id: int,
                         role: str, squad_id: Optional[int] = None,
                         wing_id: Optional[int] = None) -> None:
        """
        Move fleet member to different position (requires authentication and fleet role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must have move permissions)
            member_id: Character ID to move
            role: New fleet role
            squad_id: Squad ID (required for squad roles)
            wing_id: Wing ID (required for wing/squad roles)
        """
        endpoint = f'/fleets/{fleet_id}/members/{member_id}/'
        json_data = {'role': role}
        
        if squad_id is not None:
            json_data['squad_id'] = squad_id
        if wing_id is not None:
            json_data['wing_id'] = wing_id
            
        return self.client.put(endpoint, character_id=character_id, json_data=json_data)
    
    def get_fleet_wings(self, fleet_id: int, character_id: str) -> List[Dict[str, Any]]:
        """
        Get fleet wings (requires authentication and fleet role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet member)
            
        Returns:
            List of fleet wings and squads
        """
        endpoint = f'/fleets/{fleet_id}/wings/'
        return self.client.get(endpoint, character_id=character_id)
    
    def create_fleet_wing(self, fleet_id: int, character_id: str) -> Dict[str, Any]:
        """
        Create new fleet wing (requires authentication and fleet commander role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet commander)
            
        Returns:
            Created wing information
        """
        endpoint = f'/fleets/{fleet_id}/wings/'
        return self.client.post(endpoint, character_id=character_id, json_data={})
    
    def delete_fleet_wing(self, fleet_id: int, character_id: str, wing_id: int) -> None:
        """
        Delete fleet wing (requires authentication and fleet commander role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet commander)
            wing_id: Wing ID to delete
        """
        endpoint = f'/fleets/{fleet_id}/wings/{wing_id}/'
        return self.client.delete(endpoint, character_id=character_id)
    
    def rename_fleet_wing(self, fleet_id: int, character_id: str, wing_id: int, name: str) -> None:
        """
        Rename fleet wing (requires authentication and fleet commander role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet commander)
            wing_id: Wing ID to rename
            name: New wing name
        """
        endpoint = f'/fleets/{fleet_id}/wings/{wing_id}/'
        json_data = {'name': name}
        return self.client.put(endpoint, character_id=character_id, json_data=json_data)
    
    def create_fleet_squad(self, fleet_id: int, character_id: str, wing_id: int) -> Dict[str, Any]:
        """
        Create new fleet squad (requires authentication and fleet commander role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet commander)
            wing_id: Wing ID to create squad in
            
        Returns:
            Created squad information
        """
        endpoint = f'/fleets/{fleet_id}/wings/{wing_id}/squads/'
        return self.client.post(endpoint, character_id=character_id, json_data={})
    
    def delete_fleet_squad(self, fleet_id: int, character_id: str, wing_id: int, squad_id: int) -> None:
        """
        Delete fleet squad (requires authentication and fleet commander role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet commander)
            wing_id: Wing ID
            squad_id: Squad ID to delete
        """
        endpoint = f'/fleets/{fleet_id}/wings/{wing_id}/squads/{squad_id}/'
        return self.client.delete(endpoint, character_id=character_id)
    
    def rename_fleet_squad(self, fleet_id: int, character_id: str, wing_id: int, 
                          squad_id: int, name: str) -> None:
        """
        Rename fleet squad (requires authentication and fleet commander role).
        
        Args:
            fleet_id: Fleet ID
            character_id: Character ID as string (must be fleet commander)
            wing_id: Wing ID
            squad_id: Squad ID to rename
            name: New squad name
        """
        endpoint = f'/fleets/{fleet_id}/wings/{wing_id}/squads/{squad_id}/'
        json_data = {'name': name}
        return self.client.put(endpoint, character_id=character_id, json_data=json_data)
