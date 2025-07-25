"""
Mail endpoint module for EVE Online ESI API

This module provides access to mail-related endpoints including
character mail, mailing lists, and mail management.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class MailEndpoint:
    """
    Mail endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing character mail, mailing lists,
    and mail management functionality.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize mail endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized MailEndpoint")
    
    def get_character_mail(self, character_id: str, labels: Optional[List[int]] = None,
                          last_mail_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get character's mail (requires authentication).
        
        Args:
            character_id: Character ID as string
            labels: List of label IDs to filter by
            last_mail_id: ID of last mail for pagination
            
        Returns:
            List of character's mail
        """
        endpoint = f'/characters/{character_id}/mail/'
        params = {}
        if labels:
            params['labels'] = ','.join(map(str, labels))
        if last_mail_id:
            params['last_mail_id'] = last_mail_id
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_character_mail_labels(self, character_id: str) -> Dict[str, Any]:
        """
        Get character's mail labels and unread counts (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Mail labels and unread counts
        """
        endpoint = f'/characters/{character_id}/mail/labels/'
        return self.client.get(endpoint, character_id=character_id)
    
    def post_character_mail_labels(self, character_id: str, label_data: Dict[str, Any]) -> int:
        """
        Create a mail label (requires authentication).
        
        Args:
            character_id: Character ID as string
            label_data: Label data including name and color
            
        Returns:
            ID of created label
        """
        endpoint = f'/characters/{character_id}/mail/labels/'
        return self.client.post(endpoint, character_id=character_id, json_data=label_data)
    
    def delete_character_mail_label(self, character_id: str, label_id: int) -> None:
        """
        Delete a mail label (requires authentication).
        
        Args:
            character_id: Character ID as string
            label_id: Label ID to delete
        """
        endpoint = f'/characters/{character_id}/mail/labels/{label_id}/'
        self.client.delete(endpoint, character_id=character_id)
    
    def get_character_mail_lists(self, character_id: str) -> List[Dict[str, Any]]:
        """
        Get character's mailing lists (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            List of character's mailing lists
        """
        endpoint = f'/characters/{character_id}/mail/lists/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_mail_detail(self, character_id: str, mail_id: int) -> Dict[str, Any]:
        """
        Get mail details (requires authentication).
        
        Args:
            character_id: Character ID as string
            mail_id: Mail ID
            
        Returns:
            Mail details
        """
        endpoint = f'/characters/{character_id}/mail/{mail_id}/'
        return self.client.get(endpoint, character_id=character_id)
    
    def delete_character_mail(self, character_id: str, mail_id: int) -> None:
        """
        Delete a mail (requires authentication).
        
        Args:
            character_id: Character ID as string
            mail_id: Mail ID to delete
        """
        endpoint = f'/characters/{character_id}/mail/{mail_id}/'
        self.client.delete(endpoint, character_id=character_id)
    
    def put_character_mail(self, character_id: str, mail_id: int, mail_data: Dict[str, Any]) -> None:
        """
        Update mail metadata (requires authentication).
        
        Args:
            character_id: Character ID as string
            mail_id: Mail ID to update
            mail_data: Mail metadata to update
        """
        endpoint = f'/characters/{character_id}/mail/{mail_id}/'
        self.client.put(endpoint, character_id=character_id, json_data=mail_data)
    
    def post_character_mail(self, character_id: str, mail_data: Dict[str, Any]) -> int:
        """
        Send a new mail (requires authentication).
        
        Args:
            character_id: Character ID as string
            mail_data: Mail data including recipients, subject, and body
            
        Returns:
            ID of sent mail
        """
        endpoint = f'/characters/{character_id}/mail/'
        return self.client.post(endpoint, character_id=character_id, json_data=mail_data)
