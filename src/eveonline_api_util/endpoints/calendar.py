"""
Calendar endpoint module for EVE Online ESI API

This module provides access to calendar-related endpoints including
character calendar events and responses.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class CalendarEndpoint:
    """
    Calendar endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character calendar events
    and managing event responses.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize calendar endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized CalendarEndpoint")
    
    def get_character_calendar(self, character_id: str, from_event: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get character's calendar events (requires authentication).
        
        Args:
            character_id: Character ID as string
            from_event: Event ID to start from for pagination
            
        Returns:
            List of character's calendar events
        """
        endpoint = f'/characters/{character_id}/calendar/'
        params = {}
        if from_event:
            params['from_event'] = from_event
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_calendar_event(self, character_id: str, event_id: int) -> Dict[str, Any]:
        """
        Get calendar event details (requires authentication).
        
        Args:
            character_id: Character ID as string
            event_id: Event ID
            
        Returns:
            Calendar event details
        """
        endpoint = f'/characters/{character_id}/calendar/{event_id}/'
        return self.client.get(endpoint, character_id=character_id)
    
    def put_character_calendar_event(self, character_id: str, event_id: int, response: str) -> None:
        """
        Respond to a calendar event (requires authentication).
        
        Args:
            character_id: Character ID as string
            event_id: Event ID
            response: Response ('accepted', 'declined', 'tentative')
        """
        endpoint = f'/characters/{character_id}/calendar/{event_id}/'
        response_data = {'response': response}
        self.client.put(endpoint, character_id=character_id, json_data=response_data)
    
    def get_character_calendar_event_attendees(self, character_id: str, event_id: int) -> List[Dict[str, Any]]:
        """
        Get calendar event attendees (requires authentication).
        
        Args:
            character_id: Character ID as string
            event_id: Event ID
            
        Returns:
            List of event attendees
        """
        endpoint = f'/characters/{character_id}/calendar/{event_id}/attendees/'
        return self.client.get(endpoint, character_id=character_id)
