"""
Universe endpoint module for EVE Online ESI API

This module provides access to universe-related endpoints including
systems, regions, stations, structures, and various game data.
"""

from typing import Dict, Any, Optional, List
import logging

from ..esi_client import ESIClient

logger = logging.getLogger(__name__)


class UniverseEndpoint:
    """
    Universe endpoint wrapper for EVE Online ESI API.
    
    Provides methods for accessing universe data including systems,
    regions, stations, structures, and various game items.
    """
    
    def __init__(self, client: ESIClient):
        """
        Initialize universe endpoint.
        
        Args:
            client: ESIClient instance
        """
        self.client = client
        logger.info("Initialized UniverseEndpoint")
    
    def get_universe_ancestries(self, accept_language: str = 'en') -> List[Dict[str, Any]]:
        """
        Get ancestries.
        
        Args:
            accept_language: Language to return names in
            
        Returns:
            List of ancestries
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get('/universe/ancestries/', headers=headers)
    
    def get_universe_bloodlines(self, accept_language: str = 'en') -> List[Dict[str, Any]]:
        """
        Get bloodlines.
        
        Args:
            accept_language: Language to return names in
            
        Returns:
            List of bloodlines
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get('/universe/bloodlines/', headers=headers)
    
    def get_universe_categories(self) -> List[int]:
        """
        Get item categories.
        
        Returns:
            List of category IDs
        """
        return self.client.get('/universe/categories/')
    
    def get_universe_category(self, category_id: int, accept_language: str = 'en') -> Dict[str, Any]:
        """
        Get information about an item category.
        
        Args:
            category_id: Category ID
            accept_language: Language to return names in
            
        Returns:
            Category information
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get(f'/universe/categories/{category_id}/', headers=headers)
    
    def get_universe_constellations(self) -> List[int]:
        """
        Get constellations.
        
        Returns:
            List of constellation IDs
        """
        return self.client.get('/universe/constellations/')
    
    def get_universe_constellation(self, constellation_id: int, accept_language: str = 'en') -> Dict[str, Any]:
        """
        Get information about a constellation.
        
        Args:
            constellation_id: Constellation ID
            accept_language: Language to return names in
            
        Returns:
            Constellation information
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get(f'/universe/constellations/{constellation_id}/', headers=headers)
    
    def get_universe_factions(self, accept_language: str = 'en') -> List[Dict[str, Any]]:
        """
        Get factions.
        
        Args:
            accept_language: Language to return names in
            
        Returns:
            List of factions
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get('/universe/factions/', headers=headers)
    
    def get_universe_graphics(self) -> List[int]:
        """
        Get graphics.
        
        Returns:
            List of graphic IDs
        """
        return self.client.get('/universe/graphics/')
    
    def get_universe_graphic(self, graphic_id: int) -> Dict[str, Any]:
        """
        Get information about a graphic.
        
        Args:
            graphic_id: Graphic ID
            
        Returns:
            Graphic information
        """
        return self.client.get(f'/universe/graphics/{graphic_id}/')
    
    def get_universe_groups(self, page: int = 1) -> List[int]:
        """
        Get item groups.
        
        Args:
            page: Page number for pagination
            
        Returns:
            List of group IDs
        """
        params = {'page': page}
        return self.client.get('/universe/groups/', params=params)
    
    def get_universe_group(self, group_id: int, accept_language: str = 'en') -> Dict[str, Any]:
        """
        Get information about an item group.
        
        Args:
            group_id: Group ID
            accept_language: Language to return names in
            
        Returns:
            Group information
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get(f'/universe/groups/{group_id}/', headers=headers)
    
    def get_universe_moons(self, moon_id: int) -> Dict[str, Any]:
        """
        Get information about a moon.
        
        Args:
            moon_id: Moon ID
            
        Returns:
            Moon information
        """
        return self.client.get(f'/universe/moons/{moon_id}/')
    
    def get_universe_planets(self, planet_id: int) -> Dict[str, Any]:
        """
        Get information about a planet.
        
        Args:
            planet_id: Planet ID
            
        Returns:
            Planet information
        """
        return self.client.get(f'/universe/planets/{planet_id}/')
    
    def get_universe_races(self, accept_language: str = 'en') -> List[Dict[str, Any]]:
        """
        Get races.
        
        Args:
            accept_language: Language to return names in
            
        Returns:
            List of races
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get('/universe/races/', headers=headers)
    
    def get_universe_regions(self) -> List[int]:
        """
        Get regions.
        
        Returns:
            List of region IDs
        """
        return self.client.get('/universe/regions/')
    
    def get_universe_region(self, region_id: int, accept_language: str = 'en') -> Dict[str, Any]:
        """
        Get information about a region.
        
        Args:
            region_id: Region ID
            accept_language: Language to return names in
            
        Returns:
            Region information
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get(f'/universe/regions/{region_id}/', headers=headers)
    
    def get_universe_stargates(self, stargate_id: int) -> Dict[str, Any]:
        """
        Get information about a stargate.
        
        Args:
            stargate_id: Stargate ID
            
        Returns:
            Stargate information
        """
        return self.client.get(f'/universe/stargates/{stargate_id}/')
    
    def get_universe_stars(self, star_id: int) -> Dict[str, Any]:
        """
        Get information about a star.
        
        Args:
            star_id: Star ID
            
        Returns:
            Star information
        """
        return self.client.get(f'/universe/stars/{star_id}/')
    
    def get_universe_stations(self, station_id: int) -> Dict[str, Any]:
        """
        Get information about a station.
        
        Args:
            station_id: Station ID
            
        Returns:
            Station information
        """
        return self.client.get(f'/universe/stations/{station_id}/')
    
    def get_universe_structures(self, structure_id: int, character_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about a structure.
        
        Args:
            structure_id: Structure ID
            character_id: Character ID as string (for authenticated requests)
            
        Returns:
            Structure information
        """
        endpoint = f'/universe/structures/{structure_id}/'
        if character_id:
            return self.client.get(endpoint, character_id=character_id)
        return self.client.get(endpoint)
    
    def get_universe_systems(self) -> List[int]:
        """
        Get systems.
        
        Returns:
            List of system IDs
        """
        return self.client.get('/universe/systems/')
    
    def get_universe_system(self, system_id: int, accept_language: str = 'en') -> Dict[str, Any]:
        """
        Get information about a system.
        
        Args:
            system_id: System ID
            accept_language: Language to return names in
            
        Returns:
            System information
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get(f'/universe/systems/{system_id}/', headers=headers)
    
    def get_universe_types(self, page: int = 1) -> List[int]:
        """
        Get types.
        
        Args:
            page: Page number for pagination
            
        Returns:
            List of type IDs
        """
        params = {'page': page}
        return self.client.get('/universe/types/', params=params)
    
    def get_universe_type(self, type_id: int, accept_language: str = 'en') -> Dict[str, Any]:
        """
        Get information about a type.
        
        Args:
            type_id: Type ID
            accept_language: Language to return names in
            
        Returns:
            Type information
        """
        headers = {'Accept-Language': accept_language}
        return self.client.get(f'/universe/types/{type_id}/', headers=headers)
    
    def post_universe_ids(self, names: List[str], accept_language: str = 'en') -> Dict[str, Any]:
        """
        Resolve names to IDs.
        
        Args:
            names: List of names to resolve
            accept_language: Language for results
            
        Returns:
            Dictionary with resolved IDs
        """
        headers = {'Accept-Language': accept_language}
        return self.client.post('/universe/ids/', json_data=names, headers=headers)
    
    def post_universe_names(self, ids: List[int], accept_language: str = 'en') -> List[Dict[str, Any]]:
        """
        Resolve IDs to names.
        
        Args:
            ids: List of IDs to resolve
            accept_language: Language for results
            
        Returns:
            List with resolved names
        """
        headers = {'Accept-Language': accept_language}
        return self.client.post('/universe/names/', json_data=ids, headers=headers)
