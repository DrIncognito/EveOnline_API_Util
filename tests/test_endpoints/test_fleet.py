"""
Tests for Fleet endpoint functionality
"""

from unittest.mock import Mock
import pytest

from eveonline_api_util.endpoints.fleet import FleetEndpoint
from eveonline_api_util.esi_client import ESIClient


class TestFleetEndpoint:
    """Test FleetEndpoint functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.mock_client = Mock(spec=ESIClient)
        self.endpoint = FleetEndpoint(self.mock_client)
    
    def test_init(self):
        """Test FleetEndpoint initialization."""
        assert self.endpoint.client == self.mock_client
    
    def test_get_character_fleet_info(self):
        """Test getting character's current fleet information."""
        expected_data = {
            'fleet_id': 1234567890,
            'role': 'squad_member',
            'squad_id': 3,
            'wing_id': 2
        }
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_fleet_info('98765')
        
        self.mock_client.get.assert_called_once_with('/characters/98765/fleet/', character_id='98765')
        assert result == expected_data
    
    def test_get_fleet_info(self):
        """Test getting fleet information."""
        expected_data = {
            'is_free_move': False,
            'is_registered': False,
            'is_voice_enabled': False,
            'motd': 'This is the fleet MOTD'
        }
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_fleet_info(1234567890, '98765')
        
        self.mock_client.get.assert_called_once_with('/fleets/1234567890/', character_id='98765')
        assert result == expected_data
    
    def test_update_fleet_info_all_params(self):
        """Test updating fleet information with all parameters."""
        self.endpoint.update_fleet_info(1234567890, '98765', is_free_move=True, motd='New MOTD')
        
        expected_json = {
            'is_free_move': True,
            'motd': 'New MOTD'
        }
        
        self.mock_client.put.assert_called_once_with(
            '/fleets/1234567890/', 
            character_id='98765', 
            json_data=expected_json
        )
    
    def test_update_fleet_info_partial(self):
        """Test updating fleet information with partial parameters."""
        self.endpoint.update_fleet_info(1234567890, '98765', is_free_move=False)
        
        expected_json = {
            'is_free_move': False
        }
        
        self.mock_client.put.assert_called_once_with(
            '/fleets/1234567890/', 
            character_id='98765', 
            json_data=expected_json
        )
    
    def test_update_fleet_info_empty(self):
        """Test updating fleet information with no parameters."""
        self.endpoint.update_fleet_info(1234567890, '98765')
        
        self.mock_client.put.assert_called_once_with(
            '/fleets/1234567890/', 
            character_id='98765', 
            json_data={}
        )
    
    def test_get_fleet_members(self):
        """Test getting fleet members."""
        expected_data = [
            {
                'character_id': 98765,
                'join_time': '2016-04-29T12:34:56Z',
                'role': 'squad_member',
                'role_name': 'Squad Member',
                'ship_type_id': 33328,
                'solar_system_id': 30003729,
                'squad_id': 3,
                'station_id': 61000180,
                'takes_fleet_warp': True,
                'wing_id': 2
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_fleet_members(1234567890, '98765')
        
        self.mock_client.get.assert_called_once_with('/fleets/1234567890/members/', character_id='98765')
        assert result == expected_data
    
    def test_invite_to_fleet_minimal(self):
        """Test inviting character to fleet with minimal parameters."""
        self.endpoint.invite_to_fleet(1234567890, '98765', 99999)
        
        expected_json = {
            'character_id': 99999,
            'role': 'squad_member'
        }
        
        self.mock_client.post.assert_called_once_with(
            '/fleets/1234567890/members/', 
            character_id='98765', 
            json_data=expected_json
        )
    
    def test_invite_to_fleet_full_params(self):
        """Test inviting character to fleet with all parameters."""
        self.endpoint.invite_to_fleet(
            1234567890, '98765', 99999, 
            role='squad_commander', 
            squad_id=3, 
            wing_id=2
        )
        
        expected_json = {
            'character_id': 99999,
            'role': 'squad_commander',
            'squad_id': 3,
            'wing_id': 2
        }
        
        self.mock_client.post.assert_called_once_with(
            '/fleets/1234567890/members/', 
            character_id='98765', 
            json_data=expected_json
        )
    
    def test_kick_from_fleet(self):
        """Test kicking member from fleet."""
        self.endpoint.kick_from_fleet(1234567890, '98765', 99999)
        
        self.mock_client.delete.assert_called_once_with(
            '/fleets/1234567890/members/99999/', 
            character_id='98765'
        )
    
    def test_move_fleet_member_minimal(self):
        """Test moving fleet member with minimal parameters."""
        self.endpoint.move_fleet_member(1234567890, '98765', 99999, 'wing_commander')
        
        expected_json = {
            'role': 'wing_commander'
        }
        
        self.mock_client.put.assert_called_once_with(
            '/fleets/1234567890/members/99999/', 
            character_id='98765', 
            json_data=expected_json
        )
    
    def test_move_fleet_member_full_params(self):
        """Test moving fleet member with all parameters."""
        self.endpoint.move_fleet_member(
            1234567890, '98765', 99999, 
            'squad_commander', 
            squad_id=5, 
            wing_id=3
        )
        
        expected_json = {
            'role': 'squad_commander',
            'squad_id': 5,
            'wing_id': 3
        }
        
        self.mock_client.put.assert_called_once_with(
            '/fleets/1234567890/members/99999/', 
            character_id='98765', 
            json_data=expected_json
        )
    
    def test_get_fleet_wings(self):
        """Test getting fleet wings."""
        expected_data = [
            {
                'id': 2,
                'name': 'Wing 1',
                'squads': [
                    {
                        'id': 3,
                        'name': 'Squad 1'
                    }
                ]
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_fleet_wings(1234567890, '98765')
        
        self.mock_client.get.assert_called_once_with('/fleets/1234567890/wings/', character_id='98765')
        assert result == expected_data
    
    def test_create_fleet_wing(self):
        """Test creating new fleet wing."""
        expected_data = {
            'wing_id': 4
        }
        self.mock_client.post.return_value = expected_data
        
        result = self.endpoint.create_fleet_wing(1234567890, '98765')
        
        self.mock_client.post.assert_called_once_with(
            '/fleets/1234567890/wings/', 
            character_id='98765', 
            json_data={}
        )
        assert result == expected_data
    
    def test_delete_fleet_wing(self):
        """Test deleting fleet wing."""
        self.endpoint.delete_fleet_wing(1234567890, '98765', 4)
        
        self.mock_client.delete.assert_called_once_with(
            '/fleets/1234567890/wings/4/', 
            character_id='98765'
        )
    
    def test_rename_fleet_wing(self):
        """Test renaming fleet wing."""
        self.endpoint.rename_fleet_wing(1234567890, '98765', 4, 'New Wing Name')
        
        expected_json = {
            'name': 'New Wing Name'
        }
        
        self.mock_client.put.assert_called_once_with(
            '/fleets/1234567890/wings/4/', 
            character_id='98765', 
            json_data=expected_json
        )
    
    def test_create_fleet_squad(self):
        """Test creating new fleet squad."""
        expected_data = {
            'squad_id': 6
        }
        self.mock_client.post.return_value = expected_data
        
        result = self.endpoint.create_fleet_squad(1234567890, '98765', 4)
        
        self.mock_client.post.assert_called_once_with(
            '/fleets/1234567890/wings/4/squads/', 
            character_id='98765', 
            json_data={}
        )
        assert result == expected_data
    
    def test_delete_fleet_squad(self):
        """Test deleting fleet squad."""
        self.endpoint.delete_fleet_squad(1234567890, '98765', 4, 6)
        
        self.mock_client.delete.assert_called_once_with(
            '/fleets/1234567890/wings/4/squads/6/', 
            character_id='98765'
        )
    
    def test_rename_fleet_squad(self):
        """Test renaming fleet squad."""
        self.endpoint.rename_fleet_squad(1234567890, '98765', 4, 6, 'New Squad Name')
        
        expected_json = {
            'name': 'New Squad Name'
        }
        
        self.mock_client.put.assert_called_once_with(
            '/fleets/1234567890/wings/4/squads/6/', 
            character_id='98765', 
            json_data=expected_json
        )
