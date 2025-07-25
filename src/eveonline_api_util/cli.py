"""
Command Line Interface for EVE Online API Utility

This module provides a CLI for interacting with the EVE Online ESI API,
including authentication, token management, and endpoint access.
"""

import argparse
import json
import os
import sys
import logging
from typing import Optional

from dotenv import load_dotenv

from .auth import EVEAuth, TokenManager
from .esi_client import ESIClient, ESIException
from .endpoints.character import CharacterEndpoint
from .endpoints.wallet import WalletEndpoint
from .endpoints.fleet import FleetEndpoint


def setup_logging(level: str = 'INFO') -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def load_config() -> dict:
    """Load configuration from environment variables."""
    load_dotenv()
    
    config = {
        'client_id': os.getenv('EVE_CLIENT_ID'),
        'client_secret': os.getenv('EVE_CLIENT_SECRET'),
        'redirect_uri': os.getenv('EVE_REDIRECT_URI', 'http://localhost:8000/callback'),
        'scopes': os.getenv('EVE_SCOPES', '').split(',') if os.getenv('EVE_SCOPES') else [],
        'token_file': os.getenv('EVE_TOKEN_FILE', 'tokens.json')
    }
    
    if not config['client_id'] or not config['client_secret']:
        print("Error: EVE_CLIENT_ID and EVE_CLIENT_SECRET must be set in environment variables or .env file")
        sys.exit(1)
    
    return config


def cmd_auth(args) -> None:
    """Handle authentication command."""
    config = load_config()
    token_manager = TokenManager(config['token_file'])
    auth = EVEAuth(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        redirect_uri=config['redirect_uri'],
        scopes=config['scopes'],
        token_manager=token_manager
    )
    
    # Generate authorization URL
    auth_url, state = auth.get_authorization_url()
    print(f"Please visit this URL to authorize the application:")
    print(f"{auth_url}")
    print()
    
    # Get callback URL from user
    callback_url = input("Enter the full callback URL after authorization: ").strip()
    
    try:
        token = auth.handle_callback(callback_url, state)
        character_name = token.get('CharacterName', 'Unknown')
        character_id = token.get('CharacterID', 'Unknown')
        
        print(f"Successfully authenticated character: {character_name} (ID: {character_id})")
        print(f"Token stored in: {config['token_file']}")
        
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)


def cmd_list_tokens(args) -> None:
    """List stored authentication tokens."""
    config = load_config()
    token_manager = TokenManager(config['token_file'])
    
    characters = token_manager.list_characters()
    if not characters:
        print("No stored tokens found.")
        return
    
    print("Stored character tokens:")
    for char_id in characters:
        token = token_manager.get_token(char_id)
        char_name = token.get('CharacterName', 'Unknown')
        expired = token_manager.is_token_expired(token)
        status = "EXPIRED" if expired else "VALID"
        print(f"  - {char_name} (ID: {char_id}) - {status}")


def cmd_revoke_token(args) -> None:
    """Revoke authentication token for a character."""
    config = load_config()
    token_manager = TokenManager(config['token_file'])
    auth = EVEAuth(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        redirect_uri=config['redirect_uri'],
        token_manager=token_manager
    )
    
    character_id = args.character_id
    if auth.revoke_token(character_id):
        print(f"Successfully revoked token for character {character_id}")
    else:
        print(f"No token found for character {character_id}")


def cmd_character_info(args) -> None:
    """Get character information."""
    config = load_config()
    token_manager = TokenManager(config['token_file'])
    auth = EVEAuth(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        redirect_uri=config['redirect_uri'],
        token_manager=token_manager
    )
    
    client = ESIClient(auth)
    character_endpoint = CharacterEndpoint(client)
    
    try:
        if args.public:
            # Get public information (no auth needed)
            info = character_endpoint.get_character_public_info(int(args.character_id))
        else:
            # Get authenticated information
            info = character_endpoint.get_character_attributes(args.character_id)
            
        print(json.dumps(info, indent=2))
        
    except ESIException as e:
        print(f"API Error: {e}")
        sys.exit(1)


def cmd_wallet_balance(args) -> None:
    """Get character wallet balance."""
    config = load_config()
    token_manager = TokenManager(config['token_file'])
    auth = EVEAuth(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        redirect_uri=config['redirect_uri'],
        token_manager=token_manager
    )
    
    client = ESIClient(auth)
    wallet_endpoint = WalletEndpoint(client)
    
    try:
        balance = wallet_endpoint.get_character_wallet_balance(args.character_id)
        print(f"Wallet balance: {balance:,.2f} ISK")
        
    except ESIException as e:
        print(f"API Error: {e}")
        sys.exit(1)


def cmd_server_status(args) -> None:
    """Get EVE Online server status."""
    client = ESIClient()
    
    try:
        status = client.get_server_status()
        print(json.dumps(status, indent=2))
        
    except ESIException as e:
        print(f"API Error: {e}")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='EVE Online API Utility CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Authentication commands
    auth_parser = subparsers.add_parser('auth', help='Authenticate with EVE Online')
    
    list_tokens_parser = subparsers.add_parser('list-tokens', help='List stored authentication tokens')
    
    revoke_parser = subparsers.add_parser('revoke-token', help='Revoke authentication token')
    revoke_parser.add_argument('character_id', help='Character ID to revoke token for')
    
    # Character commands
    char_info_parser = subparsers.add_parser('character-info', help='Get character information')
    char_info_parser.add_argument('character_id', help='Character ID')
    char_info_parser.add_argument('--public', action='store_true', help='Get public info only (no auth)')
    
    # Wallet commands
    wallet_parser = subparsers.add_parser('wallet-balance', help='Get character wallet balance')
    wallet_parser.add_argument('character_id', help='Character ID')
    
    # Server commands
    server_parser = subparsers.add_parser('server-status', help='Get EVE Online server status')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Route to command handlers
    if args.command == 'auth':
        cmd_auth(args)
    elif args.command == 'list-tokens':
        cmd_list_tokens(args)
    elif args.command == 'revoke-token':
        cmd_revoke_token(args)
    elif args.command == 'character-info':
        cmd_character_info(args)
    elif args.command == 'wallet-balance':
        cmd_wallet_balance(args)
    elif args.command == 'server-status':
        cmd_server_status(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
