"""
Tests for authentication and token management functionality
"""

import json
import os
import tempfile
import time
from unittest.mock import Mock, patch, MagicMock

import pytest
import requests

from eveonline_api_util.auth import TokenManager, EVEAuth


class TestTokenManager:
    """Test TokenManager functionality."""
    
    def test_init_without_file(self):
        """Test TokenManager initialization without file."""
        manager = TokenManager()
        assert manager.token_file is None
        assert manager._tokens == {}
    
    def test_init_with_nonexistent_file(self):
        """Test TokenManager initialization with nonexistent file."""
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            tmp_path = tmp.name
        
        manager = TokenManager(tmp_path)
        assert manager.token_file == tmp_path
        assert manager._tokens == {}
    
    def test_init_with_existing_file(self):
        """Test TokenManager initialization with existing token file."""
        test_tokens = {
            '12345': {
                'access_token': 'test_token',
                'refresh_token': 'test_refresh',
                'CharacterName': 'Test Character'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            json.dump(test_tokens, tmp)
            tmp_path = tmp.name
        
        try:
            manager = TokenManager(tmp_path)
            assert manager._tokens == test_tokens
        finally:
            os.unlink(tmp_path)
    
    def test_store_token(self):
        """Test storing a token."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name
        
        try:
            manager = TokenManager(tmp_path)
            token = {
                'access_token': 'test_token',
                'refresh_token': 'test_refresh',
                'CharacterName': 'Test Character'
            }
            
            manager.store_token('12345', token)
            
            # Check token was stored in memory
            stored_token = manager.get_token('12345')
            assert stored_token['access_token'] == 'test_token'
            assert 'stored_at' in stored_token
            
            # Check token was saved to file
            with open(tmp_path, 'r') as f:
                file_tokens = json.load(f)
            assert '12345' in file_tokens
            assert file_tokens['12345']['access_token'] == 'test_token'
            
        finally:
            os.unlink(tmp_path)
    
    def test_get_token(self):
        """Test retrieving a token."""
        manager = TokenManager()
        token = {'access_token': 'test_token'}
        manager._tokens['12345'] = token
        
        retrieved = manager.get_token('12345')
        assert retrieved == token
        
        # Test non-existent token
        assert manager.get_token('99999') is None
    
    def test_remove_token(self):
        """Test removing a token."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name
        
        try:
            manager = TokenManager(tmp_path)
            manager._tokens['12345'] = {'access_token': 'test_token'}
            
            # Remove existing token
            assert manager.remove_token('12345') is True
            assert manager.get_token('12345') is None
            
            # Try to remove non-existent token
            assert manager.remove_token('99999') is False
            
        finally:
            os.unlink(tmp_path)
    
    def test_is_token_expired(self):
        """Test token expiration checking."""
        manager = TokenManager()
        
        # Token without expires_at
        token_no_expiry = {'access_token': 'test'}
        assert manager.is_token_expired(token_no_expiry) is True
        
        # Expired token
        expired_token = {'expires_at': time.time() - 100}
        assert manager.is_token_expired(expired_token) is True
        
        # Valid token
        valid_token = {'expires_at': time.time() + 1000}
        assert manager.is_token_expired(valid_token) is False
        
        # Token expiring soon (within buffer)
        soon_token = {'expires_at': time.time() + 200}
        assert manager.is_token_expired(soon_token, buffer_seconds=300) is True
    
    def test_list_characters(self):
        """Test listing characters with tokens."""
        manager = TokenManager()
        manager._tokens = {
            '12345': {'CharacterName': 'Character 1'},
            '67890': {'CharacterName': 'Character 2'}
        }
        
        characters = manager.list_characters()
        assert set(characters) == {'12345', '67890'}


class TestEVEAuth:
    """Test EVEAuth functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.client_id = 'test_client_id'
        self.client_secret = 'test_client_secret'
        self.redirect_uri = 'http://localhost:8000/callback'
        self.scopes = ['esi-wallet.read_character_wallet.v1']
        
        self.token_manager = TokenManager()
        self.auth = EVEAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scopes=self.scopes,
            token_manager=self.token_manager
        )
    
    def test_init(self):
        """Test EVEAuth initialization."""
        assert self.auth.client_id == self.client_id
        assert self.auth.client_secret == self.client_secret
        assert self.auth.redirect_uri == self.redirect_uri
        assert self.auth.scopes == self.scopes
        assert self.auth.token_manager == self.token_manager
    
    @patch('eveonline_api_util.auth.OAuth2Session')
    def test_get_authorization_url(self, mock_oauth_session):
        """Test authorization URL generation."""
        mock_session = Mock()
        mock_session.authorization_url.return_value = ('http://auth_url', 'state123')
        mock_oauth_session.return_value = mock_session
        
        auth_url, state = self.auth.get_authorization_url('test_state')
        
        assert auth_url == 'http://auth_url'
        assert state == 'state123'
        
        mock_oauth_session.assert_called_once_with(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=self.scopes,
            state='test_state'
        )
    
    @patch('eveonline_api_util.auth.requests.get')
    @patch('eveonline_api_util.auth.OAuth2Session')
    def test_handle_callback(self, mock_oauth_session, mock_requests_get):
        """Test handling OAuth2 callback."""
        # Mock OAuth2Session
        mock_session = Mock()
        mock_token = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'expires_at': time.time() + 3600
        }
        mock_session.fetch_token.return_value = mock_token
        mock_oauth_session.return_value = mock_session
        
        # Mock verify response
        mock_verify_response = Mock()
        mock_verify_response.json.return_value = {
            'CharacterID': 12345,
            'CharacterName': 'Test Character',
            'CharacterOwnerHash': 'test_hash'
        }
        mock_verify_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_verify_response
        
        callback_url = 'http://localhost:8000/callback?code=test_code&state=test_state'
        result = self.auth.handle_callback(callback_url, 'test_state')
        
        # Verify token was fetched
        mock_session.fetch_token.assert_called_once_with(
            self.auth.TOKEN_URL,
            authorization_response=callback_url,
            client_secret=self.client_secret
        )
        
        # Verify token was verified
        mock_requests_get.assert_called_once_with(
            self.auth.VERIFY_URL,
            headers={'Authorization': 'Bearer test_access_token'}
        )
        
        # Verify result contains character info
        assert result['CharacterID'] == 12345
        assert result['CharacterName'] == 'Test Character'
        assert result['access_token'] == 'test_access_token'
    
    @patch('eveonline_api_util.auth.requests.get')
    def test_verify_token(self, mock_requests_get):
        """Test token verification."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'CharacterID': 12345,
            'CharacterName': 'Test Character'
        }
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response
        
        result = self.auth._verify_token('test_token')
        
        mock_requests_get.assert_called_once_with(
            self.auth.VERIFY_URL,
            headers={'Authorization': 'Bearer test_token'}
        )
        assert result['CharacterID'] == 12345
    
    @patch('eveonline_api_util.auth.OAuth2Session')
    def test_refresh_token_success(self, mock_oauth_session):
        """Test successful token refresh."""
        # Setup existing token
        old_token = {
            'access_token': 'old_token',
            'refresh_token': 'refresh_token',
            'CharacterID': 12345,
            'CharacterName': 'Test Character'
        }
        self.token_manager.store_token('12345', old_token)
        
        # Mock OAuth2Session
        mock_session = Mock()
        new_token = {
            'access_token': 'new_token',
            'refresh_token': 'new_refresh_token',
            'expires_at': time.time() + 3600
        }
        mock_session.refresh_token.return_value = new_token
        mock_oauth_session.return_value = mock_session
        
        result = self.auth.refresh_token('12345')
        
        # Verify refresh was called
        mock_session.refresh_token.assert_called_once_with(
            self.auth.TOKEN_URL,
            refresh_token='refresh_token',
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        
        # Verify result preserves character info
        assert result['access_token'] == 'new_token'
        assert result['CharacterID'] == 12345
        assert result['CharacterName'] == 'Test Character'
    
    def test_refresh_token_no_token(self):
        """Test refresh with no stored token."""
        result = self.auth.refresh_token('99999')
        assert result is None
    
    def test_get_valid_token_valid(self):
        """Test getting valid token when token is not expired."""
        token = {
            'access_token': 'valid_token',
            'expires_at': time.time() + 1000
        }
        self.token_manager.store_token('12345', token)
        
        result = self.auth.get_valid_token('12345')
        assert result == 'valid_token'
    
    @patch.object(EVEAuth, 'refresh_token')
    def test_get_valid_token_expired(self, mock_refresh):
        """Test getting valid token when token is expired."""
        # Store expired token
        expired_token = {
            'access_token': 'expired_token',
            'expires_at': time.time() - 100
        }
        self.token_manager.store_token('12345', expired_token)
        
        # Mock successful refresh
        refreshed_token = {
            'access_token': 'refreshed_token',
            'expires_at': time.time() + 1000
        }
        mock_refresh.return_value = refreshed_token
        
        result = self.auth.get_valid_token('12345')
        
        mock_refresh.assert_called_once_with('12345')
        assert result == 'refreshed_token'
    
    def test_get_valid_token_no_token(self):
        """Test getting valid token when no token exists."""
        result = self.auth.get_valid_token('99999')
        assert result is None
    
    def test_revoke_token(self):
        """Test token revocation."""
        token = {'access_token': 'test_token'}
        self.token_manager.store_token('12345', token)
        
        result = self.auth.revoke_token('12345')
        assert result is True
        assert self.token_manager.get_token('12345') is None
        
        # Test revoking non-existent token
        result = self.auth.revoke_token('99999')
        assert result is False
