"""
Endpoint manager for EVE Online ESI API

This module provides a convenient way to access all ESI endpoints
through a single interface.
"""

from typing import Optional
import logging

from .auth import EVEAuth, TokenManager
from .esi_client import ESIClient
from .endpoints import (
    CharacterEndpoint,
    WalletEndpoint,
    FleetEndpoint,
    AllianceEndpoint,
    CorporationEndpoint,
    ContractsEndpoint,
    MarketEndpoint,
    IndustryEndpoint,
    AssetsEndpoint,
    UniverseEndpoint,
    KillmailsEndpoint,
    LocationsEndpoint,
    MailEndpoint,
    SkillsEndpoint,
    WarsEndpoint,
    SovereigntyEndpoint,
    IncursionsEndpoint,
    InsuranceEndpoint,
    FittingsEndpoint,
    DogmaEndpoint,
    CalendarEndpoint,
    BookmarksEndpoint
)

logger = logging.getLogger(__name__)


class ESIEndpointManager:
    """
    Endpoint manager for easy access to all ESI endpoints.
    
    This class provides a convenient interface to all available
    ESI endpoints through a single object.
    """
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str,
                 user_agent: Optional[str] = None, token_file: Optional[str] = None):
        """
        Initialize the endpoint manager.
        
        Args:
            client_id: EVE Online application client ID
            client_secret: EVE Online application client secret
            redirect_uri: OAuth2 redirect URI
            user_agent: Custom user agent string
            token_file: Optional file path for token storage
        """
        self.token_manager = TokenManager(token_file)
        self.authenticator = EVEAuth(client_id, client_secret, redirect_uri, [], self.token_manager)
        self.client = ESIClient(self.authenticator, user_agent)
        
        # Initialize all endpoints
        self.character = CharacterEndpoint(self.client)
        self.wallet = WalletEndpoint(self.client)
        self.fleet = FleetEndpoint(self.client)
        self.alliance = AllianceEndpoint(self.client)
        self.corporation = CorporationEndpoint(self.client)
        self.contracts = ContractsEndpoint(self.client)
        self.market = MarketEndpoint(self.client)
        self.industry = IndustryEndpoint(self.client)
        self.assets = AssetsEndpoint(self.client)
        self.universe = UniverseEndpoint(self.client)
        self.killmails = KillmailsEndpoint(self.client)
        self.locations = LocationsEndpoint(self.client)
        self.mail = MailEndpoint(self.client)
        self.skills = SkillsEndpoint(self.client)
        self.wars = WarsEndpoint(self.client)
        self.sovereignty = SovereigntyEndpoint(self.client)
        self.incursions = IncursionsEndpoint(self.client)
        self.insurance = InsuranceEndpoint(self.client)
        self.fittings = FittingsEndpoint(self.client)
        self.dogma = DogmaEndpoint(self.client)
        self.calendar = CalendarEndpoint(self.client)
        self.bookmarks = BookmarksEndpoint(self.client)
        
        logger.info("Initialized ESIEndpointManager with all endpoints")
    
    def authenticate(self, scopes: list) -> str:
        """
        Get authentication URL for OAuth2 flow.
        
        Args:
            scopes: List of ESI scopes to request
            
        Returns:
            Authorization URL for user to visit
        """
        self.authenticator.scopes = scopes
        auth_url, _ = self.authenticator.get_authorization_url()
        return auth_url
    
    def handle_callback(self, callback_url: str, state: str) -> dict:
        """
        Handle OAuth2 callback and store tokens.
        
        Args:
            callback_url: Full callback URL from OAuth2 flow
            state: OAuth2 state parameter
            
        Returns:
            Token information dictionary
        """
        return self.authenticator.handle_callback(callback_url, state)
    
    def get_available_endpoints(self) -> dict:
        """
        Get information about all available endpoints.
        
        Returns:
            Dictionary with endpoint names and descriptions
        """
        return {
            'character': 'Character information and data',
            'wallet': 'Wallet transactions and balances',
            'fleet': 'Fleet management and information',
            'alliance': 'Alliance information and data',
            'corporation': 'Corporation information and data',
            'contracts': 'Contract management and data',
            'market': 'Market data and orders',
            'industry': 'Industry jobs and facilities',
            'assets': 'Asset management and locations',
            'universe': 'Universe data and information',
            'killmails': 'Killmail data and information',
            'locations': 'Character location and status',
            'mail': 'In-game mail management',
            'skills': 'Character skills and training',
            'wars': 'War information and data',
            'sovereignty': 'Sovereignty campaigns and structures',
            'incursions': 'Active incursion information',
            'insurance': 'Ship insurance prices',
            'fittings': 'Ship fitting management',
            'dogma': 'Dogma attributes and effects',
            'calendar': 'Calendar events and management',
            'bookmarks': 'Bookmark management'
        }
