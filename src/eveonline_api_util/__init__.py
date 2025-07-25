"""
EveOnline API Util

A comprehensive Python library for EVE Online ESI API integration.
"""

from .auth import EVEAuth, TokenManager
from .esi_client import ESIClient
from .endpoint_manager import ESIEndpointManager
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

__version__ = "1.0.0"

__all__ = [
    'EVEAuth',
    'TokenManager',
    'ESIClient',
    'ESIEndpointManager',
    'CharacterEndpoint',
    'WalletEndpoint',
    'FleetEndpoint',
    'AllianceEndpoint',
    'CorporationEndpoint',
    'ContractsEndpoint',
    'MarketEndpoint',
    'IndustryEndpoint',
    'AssetsEndpoint',
    'UniverseEndpoint',
    'KillmailsEndpoint',
    'LocationsEndpoint',
    'MailEndpoint',
    'SkillsEndpoint',
    'WarsEndpoint',
    'SovereigntyEndpoint',
    'IncursionsEndpoint',
    'InsuranceEndpoint',
    'FittingsEndpoint',
    'DogmaEndpoint',
    'CalendarEndpoint',
    'BookmarksEndpoint'
]

from .auth import EVEAuth, TokenManager
from .esi_client import ESIClient
from .endpoints.character import CharacterEndpoint
from .endpoints.wallet import WalletEndpoint
from .endpoints.fleet import FleetEndpoint

__version__ = "1.0.0"
__author__ = "EVE Online API Util Contributors"
__email__ = "your-email@example.com"
__description__ = "A comprehensive Python library for EVE Online ESI API integration"

__all__ = [
    "EVEAuth",
    "TokenManager", 
    "ESIClient",
    "CharacterEndpoint",
    "WalletEndpoint",
    "FleetEndpoint",
]
