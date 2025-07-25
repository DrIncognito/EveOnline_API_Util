"""
Tests for Wallet endpoint functionality
"""

from unittest.mock import Mock
import pytest

from eveonline_api_util.endpoints.wallet import WalletEndpoint
from eveonline_api_util.esi_client import ESIClient


class TestWalletEndpoint:
    """Test WalletEndpoint functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.mock_client = Mock(spec=ESIClient)
        self.endpoint = WalletEndpoint(self.mock_client)
    
    def test_init(self):
        """Test WalletEndpoint initialization."""
        assert self.endpoint.client == self.mock_client
    
    def test_get_character_wallet_balance(self):
        """Test getting character wallet balance."""
        expected_balance = 1234567.89
        self.mock_client.get.return_value = expected_balance
        
        result = self.endpoint.get_character_wallet_balance('98765')
        
        self.mock_client.get.assert_called_once_with('/characters/98765/wallet/', character_id='98765')
        assert result == expected_balance
    
    def test_get_character_wallet_journal(self):
        """Test getting character wallet journal."""
        expected_data = [
            {
                'amount': 1000000.0,
                'balance': 500000000.0,
                'context_id': 4,
                'context_id_type': 'structure_id',
                'date': '2018-02-23T14:31:32Z',
                'description': 'Market escrow',
                'first_party_id': 2112625428,
                'id': 89,
                'reason': '',
                'ref_type': 'market_escrow',
                'second_party_id': 1000132
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_wallet_journal('98765', page=2)
        
        self.mock_client.get.assert_called_once_with(
            '/characters/98765/wallet/journal/', 
            character_id='98765', 
            params={'page': 2}
        )
        assert result == expected_data
    
    def test_get_character_wallet_journal_default_page(self):
        """Test getting character wallet journal with default page."""
        expected_data = []
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_wallet_journal('98765')
        
        self.mock_client.get.assert_called_once_with(
            '/characters/98765/wallet/journal/', 
            character_id='98765', 
            params={'page': 1}
        )
        assert result == expected_data
    
    def test_get_character_wallet_transactions(self):
        """Test getting character wallet transactions."""
        expected_data = [
            {
                'client_id': 54321,
                'date': '2016-10-24T09:00:00Z',
                'is_buy': True,
                'is_personal': True,
                'journal_ref_id': 67890,
                'location_id': 60014719,
                'quantity': 1,
                'transaction_id': 1234567890,
                'type_id': 587,
                'unit_price': 1.0
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_wallet_transactions('98765', from_id=123456)
        
        self.mock_client.get.assert_called_once_with(
            '/characters/98765/wallet/transactions/', 
            character_id='98765', 
            params={'from_id': 123456}
        )
        assert result == expected_data
    
    def test_get_character_wallet_transactions_no_from_id(self):
        """Test getting character wallet transactions without from_id."""
        expected_data = []
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_character_wallet_transactions('98765')
        
        self.mock_client.get.assert_called_once_with(
            '/characters/98765/wallet/transactions/', 
            character_id='98765', 
            params={}
        )
        assert result == expected_data
    
    def test_get_corporation_wallets(self):
        """Test getting corporation wallet information."""
        expected_data = [
            {
                'balance': 123456.78,
                'division': 1
            },
            {
                'balance': 999999.99,
                'division': 2
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_corporation_wallets(12345, '98765')
        
        self.mock_client.get.assert_called_once_with('/corporations/12345/wallets/', character_id='98765')
        assert result == expected_data
    
    def test_get_corporation_wallet_journal(self):
        """Test getting corporation wallet journal."""
        expected_data = [
            {
                'amount': 10000.0,
                'balance': 500000.0,
                'context_id': 4,
                'context_id_type': 'contract_id',
                'date': '2018-02-23T14:31:32Z',
                'description': 'Contract reward',
                'first_party_id': 2112625428,
                'id': 123,
                'reason': '',
                'ref_type': 'contract_reward',
                'second_party_id': 1000132
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_corporation_wallet_journal(12345, 1, '98765', page=3)
        
        self.mock_client.get.assert_called_once_with(
            '/corporations/12345/wallets/1/journal/', 
            character_id='98765', 
            params={'page': 3}
        )
        assert result == expected_data
    
    def test_get_corporation_wallet_journal_default_page(self):
        """Test getting corporation wallet journal with default page."""    
        expected_data = []
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_corporation_wallet_journal(12345, 2, '98765')
        
        self.mock_client.get.assert_called_once_with(
            '/corporations/12345/wallets/2/journal/', 
            character_id='98765', 
            params={'page': 1}
        )
        assert result == expected_data
    
    def test_get_corporation_wallet_transactions(self):
        """Test getting corporation wallet transactions."""
        expected_data = [
            {
                'client_id': 54321,
                'date': '2016-10-24T09:00:00Z',
                'is_buy': False,
                'journal_ref_id': 67890,
                'location_id': 60014719,
                'quantity': 10,
                'transaction_id': 1234567891,
                'type_id': 587,
                'unit_price': 50.0
            }
        ]
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_corporation_wallet_transactions(12345, 1, '98765', from_id=999999)
        
        self.mock_client.get.assert_called_once_with(
            '/corporations/12345/wallets/1/transactions/', 
            character_id='98765', 
            params={'from_id': 999999}
        )
        assert result == expected_data
    
    def test_get_corporation_wallet_transactions_no_from_id(self):
        """Test getting corporation wallet transactions without from_id."""
        expected_data = []
        self.mock_client.get.return_value = expected_data
        
        result = self.endpoint.get_corporation_wallet_transactions(12345, 3, '98765')
        
        self.mock_client.get.assert_called_once_with(
            '/corporations/12345/wallets/3/transactions/', 
            character_id='98765', 
            params={}
        )
        assert result == expected_data
