"""
OAuth2 Authentication and Token Management for EVE Online ESI API

This module provides authentication functionality including OAuth2 flow,
token refresh, and secure token storage for EVE Online ESI API access.
"""

import json
import os
import time
from typing import Dict, Optional, Any
from urllib.parse import parse_qs, urlparse
import logging

from requests_oauthlib import OAuth2Session
import requests

logger = logging.getLogger(__name__)


class TokenManager:
    """
    Manages OAuth2 tokens including storage, retrieval, and refresh operations.
    
    Supports both file-based and in-memory token storage with automatic
    token refresh when tokens expire.
    """
    
    def __init__(self, token_file: Optional[str] = None):
        """
        Initialize TokenManager.
        
        Args:
            token_file: Path to file for token storage. If None, uses in-memory storage.
        """
        self.token_file = token_file
        self._tokens: Dict[str, Any] = {}
        
        if token_file and os.path.exists(token_file):
            self._load_tokens()
    
    def _load_tokens(self) -> None:
        """Load tokens from file storage."""
        try:
            with open(self.token_file, 'r') as f:
                self._tokens = json.load(f)
            logger.info(f"Loaded tokens from {self.token_file}")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load tokens: {e}")
            self._tokens = {}
    
    def _save_tokens(self) -> None:
        """Save tokens to file storage."""
        if not self.token_file:
            return
            
        try:
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, 'w') as f:
                json.dump(self._tokens, f, indent=2)
            logger.info(f"Saved tokens to {self.token_file}")
        except IOError as e:
            logger.error(f"Failed to save tokens: {e}")
    
    def store_token(self, character_id: str, token: Dict[str, Any]) -> None:
        """
        Store a token for a character.
        
        Args:
            character_id: Character ID as string
            token: Token dictionary containing access_token, refresh_token, etc.
        """
        token['stored_at'] = time.time()
        self._tokens[character_id] = token
        self._save_tokens()
        logger.info(f"Stored token for character {character_id}")
    
    def get_token(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve token for a character.
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Token dictionary or None if not found
        """
        return self._tokens.get(character_id)
    
    def remove_token(self, character_id: str) -> bool:
        """
        Remove token for a character.
        
        Args:
            character_id: Character ID as string
            
        Returns:
            True if token was removed, False if not found
        """
        if character_id in self._tokens:
            del self._tokens[character_id]
            self._save_tokens()
            logger.info(f"Removed token for character {character_id}")
            return True
        return False
    
    def is_token_expired(self, token: Dict[str, Any], buffer_seconds: int = 300) -> bool:
        """
        Check if a token is expired or will expire soon.
        
        Args:
            token: Token dictionary
            buffer_seconds: Consider token expired if it expires within this buffer
            
        Returns:
            True if token is expired or will expire soon
        """
        if 'expires_at' not in token:
            return True
            
        return time.time() + buffer_seconds >= token['expires_at']
    
    def list_characters(self) -> list:
        """
        List all character IDs with stored tokens.
        
        Returns:
            List of character IDs
        """
        return list(self._tokens.keys())


class EVEAuth:
    """
    Handles OAuth2 authentication flow for EVE Online ESI API.
    
    Provides methods for generating authorization URLs, handling callbacks,
    and refreshing tokens automatically.
    """
    
    # EVE Online ESI OAuth2 endpoints
    AUTHORIZATION_BASE_URL = 'https://login.eveonline.com/v2/oauth/authorize'
    TOKEN_URL = 'https://login.eveonline.com/v2/oauth/token'
    VERIFY_URL = 'https://esi.evetech.net/verify/'
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, 
                 scopes: Optional[list] = None, token_manager: Optional[TokenManager] = None):
        """
        Initialize EVE Online OAuth2 authentication.
        
        Args:
            client_id: EVE application client ID
            client_secret: EVE application client secret
            redirect_uri: OAuth2 redirect URI
            scopes: List of ESI scopes to request
            token_manager: TokenManager instance for token storage
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes or []
        self.token_manager = token_manager or TokenManager()
        
        logger.info(f"Initialized EVEAuth for client {client_id}")
    
    def get_authorization_url(self, state: Optional[str] = None) -> tuple:
        """
        Generate authorization URL for OAuth2 flow.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            Tuple of (authorization_url, state)
        """
        oauth = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=self.scopes,
            state=state
        )
        
        authorization_url, state = oauth.authorization_url(
            self.AUTHORIZATION_BASE_URL
        )
        
        logger.info("Generated authorization URL")
        return authorization_url, state
    
    def handle_callback(self, authorization_response: str, state: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle OAuth2 callback and exchange code for tokens.
        
        Args:
            authorization_response: Full callback URL with code
            state: State parameter for verification
            
        Returns:
            Token dictionary with character information
        """
        oauth = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            state=state
        )
        
        token = oauth.fetch_token(
            self.TOKEN_URL,
            authorization_response=authorization_response,
            client_secret=self.client_secret
        )
        
        # Verify token and get character info
        character_info = self._verify_token(token['access_token'])
        token.update(character_info)
        
        # Store token
        character_id = str(character_info['CharacterID'])
        self.token_manager.store_token(character_id, token)
        
        logger.info(f"Successfully authenticated character {character_id}")
        return token
    
    def _verify_token(self, access_token: str) -> Dict[str, Any]:
        """
        Verify access token and get character information.
        
        Args:
            access_token: OAuth2 access token
            
        Returns:
            Dictionary with character information
        """
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.VERIFY_URL, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def refresh_token(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        Refresh access token for a character.
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Updated token dictionary or None if refresh failed
        """
        token = self.token_manager.get_token(character_id)
        if not token or 'refresh_token' not in token:
            logger.error(f"No refresh token found for character {character_id}")
            return None
        
        oauth = OAuth2Session(client_id=self.client_id)
        
        try:
            updated_token = oauth.refresh_token(
                self.TOKEN_URL,
                refresh_token=token['refresh_token'],
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            # Preserve character info
            updated_token.update({
                'CharacterID': token.get('CharacterID'),
                'CharacterName': token.get('CharacterName'),
                'CharacterOwnerHash': token.get('CharacterOwnerHash')
            })
            
            self.token_manager.store_token(character_id, updated_token)
            logger.info(f"Refreshed token for character {character_id}")
            return updated_token
            
        except Exception as e:
            logger.error(f"Failed to refresh token for character {character_id}: {e}")
            return None
    
    def get_valid_token(self, character_id: str) -> Optional[str]:
        """
        Get a valid access token for a character, refreshing if necessary.
        
        Args:
            character_id: Character ID as string
            
        Returns:
            Valid access token or None if unavailable
        """
        token = self.token_manager.get_token(character_id)
        if not token:
            logger.error(f"No token found for character {character_id}")
            return None
        
        if self.token_manager.is_token_expired(token):
            logger.info(f"Token expired for character {character_id}, refreshing...")
            token = self.refresh_token(character_id)
            if not token:
                return None
        
        return token['access_token']
    
    def revoke_token(self, character_id: str) -> bool:
        """
        Revoke and remove token for a character.
        
        Args:
            character_id: Character ID as string
            
        Returns:
            True if successfully revoked
        """
        # EVE Online doesn't provide a revoke endpoint, so we just remove locally
        return self.token_manager.remove_token(character_id)
