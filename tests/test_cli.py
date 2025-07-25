"""
Tests for CLI functionality
"""

import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys

import pytest

from eveonline_api_util.cli import (
    setup_logging, load_config, cmd_auth, cmd_list_tokens,
    cmd_revoke_token, cmd_character_info, cmd_wallet_balance,
    cmd_server_status, main
)


class TestCLI:
    """Test CLI functionality."""
    
    def test_setup_logging(self):
        """Test logging setup."""
        setup_logging('DEBUG')
        # Just verify it doesn't raise an exception
        assert True
    
    @patch.dict(os.environ, {
        'EVE_CLIENT_ID': 'test_client_id',
        'EVE_CLIENT_SECRET': 'test_client_secret',
        'EVE_REDIRECT_URI': 'http://localhost:8000/callback',
        'EVE_SCOPES': 'scope1,scope2',
        'EVE_TOKEN_FILE': 'test_tokens.json'
    })
    @patch('eveonline_api_util.cli.load_dotenv')
    def test_load_config_success(self, mock_load_dotenv):
        """Test successful config loading."""
        config = load_config()
        
        assert config['client_id'] == 'test_client_id'
        assert config['client_secret'] == 'test_client_secret'
        assert config['redirect_uri'] == 'http://localhost:8000/callback'
        assert config['scopes'] == ['scope1', 'scope2']
        assert config['token_file'] == 'test_tokens.json'
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('eveonline_api_util.cli.load_dotenv')
    def test_load_config_missing_credentials(self, mock_load_dotenv):
        """Test config loading with missing credentials."""
        with pytest.raises(SystemExit):
            load_config()
    
    @patch('eveonline_api_util.cli.load_config')
    @patch('eveonline_api_util.cli.EVEAuth')
    @patch('eveonline_api_util.cli.TokenManager')
    @patch('builtins.input', return_value='http://localhost:8000/callback?code=test&state=test')
    @patch('builtins.print')
    def test_cmd_auth_success(self, mock_print, mock_input, mock_token_manager, mock_eve_auth, mock_load_config):
        """Test successful authentication command."""
        # Setup mocks
        mock_config = {
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'redirect_uri': 'http://localhost:8000/callback',
            'scopes': ['scope1'],
            'token_file': 'tokens.json'
        }
        mock_load_config.return_value = mock_config
        
        mock_auth_instance = Mock()
        mock_auth_instance.get_authorization_url.return_value = ('http://auth_url', 'state123')
        mock_auth_instance.handle_callback.return_value = {
            'CharacterName': 'Test Character',
            'CharacterID': 12345
        }
        mock_eve_auth.return_value = mock_auth_instance
        
        # Run command
        args = Mock()
        cmd_auth(args)
        
        # Verify auth flow
        mock_auth_instance.get_authorization_url.assert_called_once()
        mock_auth_instance.handle_callback.assert_called_once()
        
        # Check print calls for success message
        print_calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        success_messages = [msg for msg in print_calls if 'Successfully authenticated' in msg]
        assert len(success_messages) > 0
    
    @patch('eveonline_api_util.cli.load_config')
    @patch('eveonline_api_util.cli.TokenManager')
    @patch('builtins.print')
    def test_cmd_list_tokens_empty(self, mock_print, mock_token_manager, mock_load_config):
        """Test listing tokens when none exist."""
        mock_load_config.return_value = {'token_file': 'tokens.json'}
        
        mock_manager_instance = Mock()
        mock_manager_instance.list_characters.return_value = []
        mock_token_manager.return_value = mock_manager_instance
        
        args = Mock()
        cmd_list_tokens(args)
        
        mock_print.assert_called_with("No stored tokens found.")
    
    @patch('eveonline_api_util.cli.load_config')
    @patch('eveonline_api_util.cli.TokenManager')
    @patch('builtins.print')
    def test_cmd_list_tokens_with_data(self, mock_print, mock_token_manager, mock_load_config):
        """Test listing tokens with stored data."""
        mock_load_config.return_value = {'token_file': 'tokens.json'}
        
        mock_manager_instance = Mock()
        mock_manager_instance.list_characters.return_value = ['12345', '67890']
        mock_manager_instance.get_token.side_effect = [
            {'CharacterName': 'Character 1', 'expires_at': 9999999999},
            {'CharacterName': 'Character 2', 'expires_at': 1000000000}
        ]
        mock_manager_instance.is_token_expired.side_effect = [False, True]
        mock_token_manager.return_value = mock_manager_instance
        
        args = Mock()
        cmd_list_tokens(args)
        
        # Check that character info was printed
        print_calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
        character_lines = [msg for msg in print_calls if 'Character' in msg and 'ID:' in msg]
        assert len(character_lines) == 2
    
    @patch('eveonline_api_util.cli.load_config')
    @patch('eveonline_api_util.cli.EVEAuth')
    @patch('eveonline_api_util.cli.TokenManager')
    @patch('builtins.print')
    def test_cmd_revoke_token_success(self, mock_print, mock_token_manager, mock_eve_auth, mock_load_config):
        """Test successful token revocation."""
        mock_load_config.return_value = {
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'redirect_uri': 'http://localhost:8000/callback',
            'token_file': 'tokens.json'
        }
        
        mock_auth_instance = Mock()
        mock_auth_instance.revoke_token.return_value = True
        mock_eve_auth.return_value = mock_auth_instance
        
        args = Mock()
        args.character_id = '12345'
        cmd_revoke_token(args)
        
        mock_auth_instance.revoke_token.assert_called_once_with('12345')
        mock_print.assert_called_with("Successfully revoked token for character 12345")
    
    @patch('eveonline_api_util.cli.load_config')
    @patch('eveonline_api_util.cli.ESIClient')
    @patch('eveonline_api_util.cli.CharacterEndpoint')
    @patch('eveonline_api_util.cli.EVEAuth')
    @patch('eveonline_api_util.cli.TokenManager')
    @patch('builtins.print')
    def test_cmd_character_info_public(self, mock_print, mock_token_manager, mock_eve_auth, 
                                      mock_char_endpoint, mock_esi_client, mock_load_config):
        """Test getting public character information."""
        mock_load_config.return_value = {
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'redirect_uri': 'http://localhost:8000/callback',
            'token_file': 'tokens.json'
        }
        
        mock_endpoint_instance = Mock()
        mock_endpoint_instance.get_character_public_info.return_value = {
            'name': 'Test Character',
            'corporation_id': 12345
        }
        mock_char_endpoint.return_value = mock_endpoint_instance
        
        args = Mock()
        args.character_id = '12345'
        args.public = True
        
        cmd_character_info(args)
        
        mock_endpoint_instance.get_character_public_info.assert_called_once_with(12345)
    
    @patch('eveonline_api_util.cli.load_config')
    @patch('eveonline_api_util.cli.ESIClient')
    @patch('eveonline_api_util.cli.WalletEndpoint')
    @patch('eveonline_api_util.cli.EVEAuth')
    @patch('eveonline_api_util.cli.TokenManager')
    @patch('builtins.print')
    def test_cmd_wallet_balance(self, mock_print, mock_token_manager, mock_eve_auth,
                               mock_wallet_endpoint, mock_esi_client, mock_load_config):
        """Test getting wallet balance."""
        mock_load_config.return_value = {
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'redirect_uri': 'http://localhost:8000/callback',
            'token_file': 'tokens.json'
        }
        
        mock_endpoint_instance = Mock()
        mock_endpoint_instance.get_character_wallet_balance.return_value = 1234567.89
        mock_wallet_endpoint.return_value = mock_endpoint_instance
        
        args = Mock()
        args.character_id = '12345'
        
        cmd_wallet_balance(args)
        
        mock_endpoint_instance.get_character_wallet_balance.assert_called_once_with('12345')
        mock_print.assert_called_with("Wallet balance: 1,234,567.89 ISK")
    
    @patch('eveonline_api_util.cli.ESIClient')
    @patch('builtins.print')
    def test_cmd_server_status(self, mock_print, mock_esi_client):
        """Test getting server status."""
        mock_client_instance = Mock()
        mock_client_instance.get_server_status.return_value = {
            'players': 12345,
            'server_version': '1.0.0'
        }
        mock_esi_client.return_value = mock_client_instance
        
        args = Mock()
        cmd_server_status(args)
        
        mock_client_instance.get_server_status.assert_called_once()
    
    @patch('sys.argv', ['eve-api-util', 'server-status'])
    @patch('eveonline_api_util.cli.cmd_server_status')
    def test_main_server_status(self, mock_cmd):
        """Test main function with server-status command."""
        main()
        mock_cmd.assert_called_once()
    
    @patch('sys.argv', ['eve-api-util', '--help'])
    def test_main_help(self):
        """Test main function with help."""
        with pytest.raises(SystemExit):
            main()
    
    @patch('sys.argv', ['eve-api-util'])
    @patch('builtins.print')
    def test_main_no_command(self, mock_print):
        """Test main function with no command."""
        # This should print help and not raise an exception
        main()
