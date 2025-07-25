"""
Market endpoint module for EVE Online ESI API

This module provides access to market-related endpoints including
market orders, prices, history, and structure markets.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class MarketEndpoint:
    """
    Market endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing market data including orders,
    prices, history, and structure markets.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize market endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized MarketEndpoint")
    
    def get_character_orders(self, character_id: str) -> List[Dict[str, Any]]:
        """
        Get character's market orders (requires authentication).
        
        Args:
            character_id: Character ID as string
            
        Returns:
            List of character's market orders
        """
        endpoint = f'/characters/{character_id}/orders/'
        return self.client.get(endpoint, character_id=character_id)
    
    def get_character_orders_history(self, character_id: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get character's market order history (requires authentication).
        
        Args:
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of character's historical market orders
        """
        endpoint = f'/characters/{character_id}/orders/history/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_orders(self, corporation_id: int, character_id: str,
                             page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation's market orders (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation's market orders
        """
        endpoint = f'/corporations/{corporation_id}/orders/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_corporation_orders_history(self, corporation_id: int, character_id: str,
                                     page: int = 1) -> List[Dict[str, Any]]:
        """
        Get corporation's market order history (requires authentication and roles).
        
        Args:
            corporation_id: Corporation ID
            character_id: Character ID as string (must have corp roles)
            page: Page number for pagination
            
        Returns:
            List of corporation's historical market orders
        """
        endpoint = f'/corporations/{corporation_id}/orders/history/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
    
    def get_market_groups(self) -> List[int]:
        """
        Get market group IDs.
        
        Returns:
            List of market group IDs
        """
        return self.client.get('/markets/groups/')
    
    def get_market_group_info(self, market_group_id: int, language: str = 'en') -> Dict[str, Any]:
        """
        Get information about a market group.
        
        Args:
            market_group_id: Market group ID
            language: Language for localized strings
            
        Returns:
            Market group information
        """
        params = {'language': language}
        return self.client.get(f'/markets/groups/{market_group_id}/', params=params)
    
    def get_market_prices(self) -> List[Dict[str, Any]]:
        """
        Get current market prices.
        
        Returns:
            List of current market prices
        """
        return self.client.get('/markets/prices/')
    
    def get_market_types(self, region_id: int, page: int = 1) -> List[int]:
        """
        Get types available in a region's market.
        
        Args:
            region_id: Region ID
            page: Page number for pagination
            
        Returns:
            List of type IDs available in the market
        """
        params = {'page': page}
        return self.client.get(f'/markets/{region_id}/types/', params=params)
    
    def get_market_orders(self, region_id: int, order_type: str = 'all',
                         page: int = 1, type_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get market orders for a region.
        
        Args:
            region_id: Region ID
            order_type: Order type ('all', 'buy', 'sell')
            page: Page number for pagination
            type_id: Type ID to filter by (optional)
            
        Returns:
            List of market orders
        """
        params = {'order_type': order_type, 'page': page}
        if type_id:
            params['type_id'] = type_id
        return self.client.get(f'/markets/{region_id}/orders/', params=params)
    
    def get_market_history(self, region_id: int, type_id: int) -> List[Dict[str, Any]]:
        """
        Get market history for a type in a region.
        
        Args:
            region_id: Region ID
            type_id: Type ID
            
        Returns:
            List of historical market data
        """
        return self.client.get(f'/markets/{region_id}/history/', params={'type_id': type_id})
    
    def get_structure_orders(self, structure_id: int, character_id: str,
                           page: int = 1) -> List[Dict[str, Any]]:
        """
        Get market orders for a structure (requires authentication and docking access).
        
        Args:
            structure_id: Structure ID
            character_id: Character ID as string
            page: Page number for pagination
            
        Returns:
            List of structure market orders
        """
        endpoint = f'/markets/structures/{structure_id}/'
        params = {'page': page}
        return self.client.get(endpoint, character_id=character_id, params=params)
