"""
Tests for ESI Client functionality
"""

from unittest.mock import Mock, patch, MagicMock
import json

import pytest
import requests
import responses

from eveonline_api_util.esi_client import (
    ESIClient, ESIException, ESIAuthenticationError, 
    ESIRateLimitError, ESIServerError
)
from eveonline_api_util.auth import EVEAuth


class TestESIClient:
    """Test ESIClient functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.mock_auth = Mock(spec=EVEAuth)
        self.client = ESIClient(auth=self.mock_auth)
    
    def test_init_without_auth(self):
        """Test ESIClient initialization without auth."""
        client = ESIClient()
        assert client.auth is None
        assert client.timeout == 30
        assert 'User-Agent' in client.session.headers
    
    def test_init_with_custom_params(self):
        """Test ESIClient initialization with custom parameters."""
        client = ESIClient(
            auth=self.mock_auth,
            user_agent='Custom-Agent/1.0',
            timeout=60,
            max_retries=5
        )
        
        assert client.auth == self.mock_auth
        assert client.timeout == 60
        assert client.session.headers['User-Agent'] == 'Custom-Agent/1.0'
    
    def test_build_url(self):
        """Test URL building."""
        # Test with leading slash
        url = self.client._build_url('/characters/12345/')
        assert url == 'https://esi.evetech.net/latest/characters/12345/'
        
        # Test without leading slash
        url = self.client._build_url('characters/12345/')
        assert url == 'https://esi.evetech.net/latest/characters/12345/'
        
        # Test with specific version
        url = self.client._build_url('/status/', version='v1')
        assert url == 'https://esi.evetech.net/v1/status/'
    
    def test_prepare_headers_no_auth(self):
        """Test header preparation without authentication."""
        headers = self.client._prepare_headers()
        
        expected = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        assert headers == expected
    
    def test_prepare_headers_with_auth(self):
        """Test header preparation with authentication."""
        self.mock_auth.get_valid_token.return_value = 'test_token'
        
        headers = self.client._prepare_headers(character_id='12345')
        
        expected = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test_token'
        }
        assert headers == expected
        self.mock_auth.get_valid_token.assert_called_once_with('12345')
    
    def test_prepare_headers_auth_failed(self):
        """Test header preparation when authentication fails."""
        self.mock_auth.get_valid_token.return_value = None
        
        with pytest.raises(ESIAuthenticationError):
            self.client._prepare_headers(character_id='12345')
    
    def test_prepare_headers_additional(self):
        """Test header preparation with additional headers."""
        additional = {'X-Custom-Header': 'test_value'}
        headers = self.client._prepare_headers(additional_headers=additional)
        
        assert headers['X-Custom-Header'] == 'test_value'
        assert headers['Accept'] == 'application/json'
    
    @responses.activate
    def test_handle_response_success_json(self):
        """Test successful JSON response handling."""
        test_data = {'test': 'data'}
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            json=test_data,
            status=200
        )
        
        response = requests.get('https://esi.evetech.net/latest/test/')
        result = self.client._handle_response(response)
        
        assert result == test_data
    
    @responses.activate
    def test_handle_response_success_no_content(self):
        """Test successful response with no content."""
        responses.add(
            responses.DELETE,
            'https://esi.evetech.net/latest/test/',
            status=204
        )
        
        response = requests.delete('https://esi.evetech.net/latest/test/')
        result = self.client._handle_response(response)
        
        assert result is None
    
    @responses.activate
    def test_handle_response_not_modified(self):
        """Test 304 Not Modified response."""
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            status=304
        )
        
        response = requests.get('https://esi.evetech.net/latest/test/')
        result = self.client._handle_response(response)
        
        assert result is None
    
    @responses.activate
    def test_handle_response_bad_request(self):
        """Test 400 Bad Request response."""
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            body='Bad request',
            status=400
        )
        
        response = requests.get('https://esi.evetech.net/latest/test/')
        
        with pytest.raises(ESIException, match='Bad request'):
            self.client._handle_response(response)
    
    @responses.activate
    def test_handle_response_unauthorized(self):
        """Test 401 Unauthorized response."""
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            status=401
        )
        
        response = requests.get('https://esi.evetech.net/latest/test/')
        
        with pytest.raises(ESIAuthenticationError):
            self.client._handle_response(response)
    
    @responses.activate
    def test_handle_response_forbidden(self):
        """Test 403 Forbidden response."""
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            body='Forbidden',
            status=403
        )
        
        response = requests.get('https://esi.evetech.net/latest/test/')
        
        with pytest.raises(ESIException, match='Forbidden'):
            self.client._handle_response(response)
    
    @responses.activate
    def test_handle_response_not_found(self):
        """Test 404 Not Found response."""
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            status=404
        )
        
        response = requests.get('https://esi.evetech.net/latest/test/')
        
        with pytest.raises(ESIException, match='Not found'):
            self.client._handle_response(response)
    
    @responses.activate
    def test_handle_response_error_limit(self):
        """Test 420 Error Limit response."""
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            status=420
        )
        
        response = requests.get('https://esi.evetech.net/latest/test/')
        
        with pytest.raises(ESIRateLimitError):
            self.client._handle_response(response)
    
    @responses.activate
    def test_handle_response_rate_limit(self):
        """Test 429 Rate Limit response."""
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            status=429
        )
        
        response = requests.get('https://esi.evetech.net/latest/test/')
        
        with pytest.raises(ESIRateLimitError):
            self.client._handle_response(response)
    
    @responses.activate
    def test_handle_response_server_error(self):
        """Test 500 Server Error response."""
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            body='Internal Server Error',
            status=500
        )
        
        response = requests.get('https://esi.evetech.net/latest/test/')
        
        with pytest.raises(ESIServerError):
            self.client._handle_response(response)
    
    @responses.activate
    def test_request_success(self):
        """Test successful request."""
        test_data = {'test': 'data'}
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            json=test_data,
            status=200
        )
        
        result = self.client.request('GET', '/test/')
        assert result == test_data
    
    @responses.activate
    def test_request_with_auth(self):
        """Test authenticated request."""
        self.mock_auth.get_valid_token.return_value = 'test_token'
        test_data = {'authenticated': 'data'}
        
        def request_callback(request):
            assert request.headers['Authorization'] == 'Bearer test_token'
            return (200, {}, json.dumps(test_data))
        
        responses.add_callback(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            callback=request_callback
        )
        
        result = self.client.request('GET', '/test/', character_id='12345')
        assert result == test_data
    
    @responses.activate
    def test_request_with_params(self):
        """Test request with parameters."""
        test_data = {'test': 'data'}
        
        def request_callback(request):
            assert 'datasource=tranquility' in request.url
            assert 'custom_param=value' in request.url
            return (200, {}, json.dumps(test_data))
        
        responses.add_callback(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            callback=request_callback
        )
        
        result = self.client.request('GET', '/test/', params={'custom_param': 'value'})
        assert result == test_data
    
    @responses.activate
    def test_request_post_with_json(self):
        """Test POST request with JSON data."""
        test_data = {'result': 'success'}
        post_data = {'input': 'data'}
        
        def request_callback(request):
            assert json.loads(request.body) == post_data
            return (200, {}, json.dumps(test_data))
        
        responses.add_callback(
            responses.POST,
            'https://esi.evetech.net/latest/test/',
            callback=request_callback
        )
        
        result = self.client.request('POST', '/test/', json_data=post_data)
        assert result == test_data
    
    def test_request_timeout(self):
        """Test request timeout handling."""
        with patch.object(self.client.session, 'request') as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout()
            
            with pytest.raises(ESIException, match='Request timeout'):
                self.client.request('GET', '/test/')
    
    def test_request_connection_error(self):
        """Test connection error handling."""
        with patch.object(self.client.session, 'request') as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError()
            
            with pytest.raises(ESIException, match='Connection error'):
                self.client.request('GET', '/test/')
    
    @responses.activate
    def test_get_method(self):
        """Test GET convenience method."""
        test_data = {'test': 'data'}
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/test/',
            json=test_data,
            status=200
        )
        
        result = self.client.get('/test/')
        assert result == test_data
    
    @responses.activate
    def test_post_method(self):
        """Test POST convenience method."""
        test_data = {'result': 'success'}
        responses.add(
            responses.POST,
            'https://esi.evetech.net/latest/test/',
            json=test_data,
            status=200
        )
        
        result = self.client.post('/test/', json_data={'input': 'data'})
        assert result == test_data
    
    @responses.activate
    def test_put_method(self):
        """Test PUT convenience method."""
        responses.add(
            responses.PUT,
            'https://esi.evetech.net/latest/test/',
            status=204
        )
        
        result = self.client.put('/test/', json_data={'update': 'data'})
        assert result is None
    
    @responses.activate
    def test_delete_method(self):
        """Test DELETE convenience method."""
        responses.add(
            responses.DELETE,
            'https://esi.evetech.net/latest/test/',
            status=204
        )
        
        result = self.client.delete('/test/')
        assert result is None
    
    @responses.activate
    def test_get_server_status(self):
        """Test server status endpoint."""
        status_data = {
            'players': 12345,
            'server_version': '1.0.0',
            'start_time': '2023-01-01T00:00:00Z'
        }
        responses.add(
            responses.GET,
            'https://esi.evetech.net/latest/status/',
            json=status_data,
            status=200
        )
        
        result = self.client.get_server_status()
        assert result == status_data
    
    @responses.activate
    def test_get_universe_types(self):
        """Test universe types endpoint."""
        type_data = [
            {'id': 34, 'name': 'Tritanium'},
            {'id': 35, 'name': 'Pyerite'}
        ]
        responses.add(
            responses.POST,
            'https://esi.evetech.net/latest/universe/names/',
            json=type_data,
            status=200
        )
        
        result = self.client.get_universe_types([34, 35])
        assert result == type_data
