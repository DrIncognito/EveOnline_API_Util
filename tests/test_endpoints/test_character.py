"""
Tests for Character endpoint functionality
"""

from unittest.mock import Mock
import pytest

from eveonline_api_util.endpoints.character import CharacterEndpoint
from eveonline_api_util.esi_client import ESIClient


class TestCharacterEndpoint:
    """Test CharacterEndpoint functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.mock_client = Mock(spec=ESIClient)
        self.endpoint = CharacterEndpoint(self.mock_client)
    
    def test_init(self):
        """Test CharacterEndpoint initialization."""
        assert self.endpoint.client == self.mock_client
    
    def test_get_character_public_info(self):
        """Test getting character public information."""
        expected_data = {
            'name': 'Test Character',
            'corporation_id': 12345,
            'birthday': '2023-01-01T00:00:00Z'
        }
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_public_info(98765)
        
        self.mock_client.get.assert_called_once_with('/characters/98765/')
        assert result == expected_data
    
    def test_get_character_portrait(self):
        """Test getting character portrait URLs."""
        expected_data = {
            'px64x64': 'https://image.eveonline.com/Character/98765_64.jpg',
            'px128x128': 'https://image.eveonline.com/Character/98765_128.jpg',
            'px256x256': 'https://image.eveonline.com/Character/98765_256.jpg',
            'px512x512': 'https://image.eveonline.com/Character/98765_512.jpg'
        }
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_portrait(98765)
        
        self.mock_client.get.assert_called_once_with('/characters/98765/portrait/')
        assert result == expected_data
    
    def test_get_character_corporation_history(self):
        """Test getting character corporation history."""
        expected_data = [
            {
                'corporation_id': 12345,
                'is_deleted': False,
                'record_id': 1,
                'start_date': '2023-01-01T00:00:00Z'
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_corporation_history(98765)
        
        self.mock_client.get.assert_called_once_with('/characters/98765/corporationhistory/')
        assert result == expected_data
    
    def test_get_character_attributes(self):
        """Test getting character attributes (authenticated)."""
        expected_data = {
            'charisma': 20,
            'intelligence': 24,
            'memory': 21,
            'perception': 23,
            'willpower': 22
        }
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_attributes('98765')
        
        self.mock_client.get.assert_called_once_with('/characters/98765/attributes/', character_id='98765')
        assert result == expected_data
    
    def test_get_character_implants(self):
        """Test getting character implants."""
        expected_data = [9899, 9941, 9942, 9943, 9944]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_implants('98765')
        
        self.mock_client.get.assert_called_once_with('/characters/98765/implants/', character_id='98765')
        assert result == expected_data
    
    def test_get_character_skills(self):
        """Test getting character skills."""
        expected_data = {
            'skills': [
                {
                    'active_skill_level': 5,
                    'skill_id': 3300,
                    'skillpoints_in_skill': 256000,
                    'trained_skill_level': 5
                }
            ],
            'total_sp': 500000,
            'unallocated_sp': 0
        }
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_skills('98765')
        
        self.mock_client.get.assert_called_once_with('/characters/98765/skills/', character_id='98765')
        assert result == expected_data
    
    def test_get_character_skillqueue(self):
        """Test getting character skill queue."""
        expected_data = [
            {
                'finish_date': '2023-12-01T00:00:00Z',
                'finished_level': 4,
                'level_end_sp': 45255,
                'level_start_sp': 8000,
                'queue_position': 0,
                'skill_id': 1978,
                'start_date': '2023-11-15T00:00:00Z',
                'training_start_sp': 40000
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_skillqueue('98765')
        
        self.mock_client.get.assert_called_once_with('/characters/98765/skillqueue/', character_id='98765')
        assert result == expected_data
    
    def test_get_character_location(self):
        """Test getting character location."""
        expected_data = {
            'solar_system_id': 30000142,
            'station_id': 60003760
        }
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_location('98765')
        
        self.mock_client.get.assert_called_once_with('/characters/98765/location/', character_id='98765')
        assert result == expected_data
    
    def test_get_character_ship(self):
        """Test getting character current ship."""
        expected_data = {
            'ship_item_id': 1000000016991,
            'ship_name': 'Test Ship',
            'ship_type_id': 670
        }
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_ship('98765')
        
        self.mock_client.get.assert_called_once_with('/characters/98765/ship/', character_id='98765')
        assert result == expected_data
    
    def test_get_character_online(self):
        """Test getting character online status."""
        expected_data = {
            'last_login': '2023-11-20T10:30:00Z',
            'last_logout': '2023-11-20T08:15:00Z',
            'logins': 500,
            'online': True
        }
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_online('98765')
        
        self.mock_client.get.assert_called_once_with('/characters/98765/online/', character_id='98765')
        assert result == expected_data
    
    def test_get_character_assets(self):
        """Test getting character assets."""
        expected_data = [
            {
                'is_singleton': True,
                'item_id': 1000000016991,
                'location_flag': 'Hangar',
                'location_id': 60003760,
                'location_type': 'station',
                'quantity': 1,
                'type_id': 670
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_assets('98765', page=2)
        
        self.mock_client.get.assert_called_once_with(
            '/characters/98765/assets/', 
            character_id='98765', 
            params={'page': 2}
        )
        assert result == expected_data
    
    def test_get_character_blueprints(self):
        """Test getting character blueprints."""
        expected_data = [
            {
                'item_id': 1000000016990,
                'location_flag': 'Hangar',
                'location_id': 60003760,
                'material_efficiency': 10,
                'quantity': -1,
                'runs': 300,
                'time_efficiency': 20,
                'type_id': 691
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_blueprints('98765')
        
        self.mock_client.get.assert_called_once_with(
            '/characters/98765/blueprints/', 
            character_id='98765', 
            params={'page': 1}
        )
        assert result == expected_data
    
    def test_get_character_bookmarks(self):
        """Test getting character bookmarks."""
        expected_data = [
            {
                'bookmark_id': 4,
                'created': '2012-07-09T22:38:31Z',
                'creator_id': 2112625428,
                'folder_id': 5,
                'item': {
                    'item_id': 50006722,
                    'type_id': 29633
                },
                'label': 'Random bookmark',
                'location_id': 30003430,
                'notes': 'This is a random bookmark'
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_bookmarks('98765')
        
        self.mock_client.get.assert_called_once_with(
            '/characters/98765/bookmarks/', 
            character_id='98765', 
            params={'page': 1}
        )
        assert result == expected_data
    
    def test_get_character_contacts(self):
        """Test getting character contacts."""
        expected_data = [
            {
                'contact_id': 2112625428,
                'contact_type': 'character',
                'is_blocked': False,
                'is_watched': True,
                'standing': 9.9
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_contacts('98765')
        
        self.mock_client.get.assert_called_once_with(
            '/characters/98765/contacts/', 
            character_id='98765', 
            params={'page': 1}
        )
        assert result == expected_data
    
    def test_add_character_contacts(self):
        """Test adding character contacts."""
        contact_ids = [2112625428, 2112625429]
        standing = 5.0
        label_ids = [1, 2]
        
        self.endpoint.add_character_contacts(
            '98765', contact_ids, standing, label_ids=label_ids, watched=True
        )
        
        expected_json = {
            'contact_ids': contact_ids,
            'standing': standing,
            'watched': True,
            'label_ids': label_ids
        }
        
        self.mock_client.post.assert_called_once_with(
            '/characters/98765/contacts/', 
            character_id='98765', 
            json_data=expected_json
        )
    
    def test_add_character_contacts_minimal(self):
        """Test adding character contacts with minimal parameters."""
        contact_ids = [2112625428]
        standing = -5.0
        
        self.endpoint.add_character_contacts('98765', contact_ids, standing)
        
        expected_json = {
            'contact_ids': contact_ids,
            'standing': standing,
            'watched': False
        }
        
        self.mock_client.post.assert_called_once_with(
            '/characters/98765/contacts/', 
            character_id='98765', 
            json_data=expected_json
        )
    
    def test_delete_character_contacts(self):
        """Test deleting character contacts."""
        contact_ids = [2112625428, 2112625429]
        
        self.endpoint.delete_character_contacts('98765', contact_ids)
        
        self.mock_client.delete.assert_called_once_with(
            '/characters/98765/contacts/', 
            character_id='98765', 
            json_data=contact_ids
        )
