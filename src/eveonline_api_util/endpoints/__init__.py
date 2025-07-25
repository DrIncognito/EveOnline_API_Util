"""
Endpoints package for EVE Online ESI API

This package contains modules for different ESI API endpoints.
"""

from .character import CharacterEndpoint
from .wallet import WalletEndpoint
from .fleet import FleetEndpoint
from .alliance import AllianceEndpoint
from .corporation import CorporationEndpoint
from .contracts import ContractsEndpoint
from .market import MarketEndpoint
from .industry import IndustryEndpoint
from .assets import AssetsEndpoint
from .universe import UniverseEndpoint
from .killmails import KillmailsEndpoint
from .locations import LocationsEndpoint
from .mail import MailEndpoint
from .skills import SkillsEndpoint
from .wars import WarsEndpoint
from .sovereignty import SovereigntyEndpoint
from .incursions import IncursionsEndpoint
from .insurance import InsuranceEndpoint
from .fittings import FittingsEndpoint
from .dogma import DogmaEndpoint
from .calendar import CalendarEndpoint
from .bookmarks import BookmarksEndpoint

__all__ = [
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
