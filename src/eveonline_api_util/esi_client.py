"""
Generic ESI Client for EVE Online API Integration

This module provides a generic client wrapper for making authenticated
requests to the EVE Online ESI API with automatic error handling,
rate limiting, and response parsing.
"""

import time
import logging
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import EVEAuth

logger = logging.getLogger(__name__)


class ESIException(Exception):
    """Base exception for ESI API errors."""
    pass


class ESIAuthenticationError(ESIException):
    """Raised when authentication fails."""
    pass


class ESIRateLimitError(ESIException):
    """Raised when rate limit is exceeded."""
    pass


class ESIServerError(ESIException):
    """Raised when ESI server returns an error."""
    pass


class ESIClient:
    """
    Generic client for EVE Online ESI API.
    
    Provides methods for making authenticated requests with automatic
    token refresh, error handling, rate limiting, and response parsing.
    """
    
    BASE_URL = 'https://esi.evetech.net'
    DEFAULT_DATASOURCE = 'tranquility'
    DEFAULT_USER_AGENT = 'EVE-Online-API-Util/1.0.0'
    
    def __init__(self, auth: Optional[EVEAuth] = None, user_agent: Optional[str] = None,
                 timeout: int = 30, max_retries: int = 3):
        """
        Initialize ESI Client.
        
        Args:
            auth: EVEAuth instance for authentication
            user_agent: Custom user agent string
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.auth = auth
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set user agent
        user_agent = user_agent or self.DEFAULT_USER_AGENT
        self.session.headers.update({'User-Agent': user_agent})
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        logger.info("Initialized ESI Client")
    
    def _build_url(self, endpoint: str, version: str = 'latest') -> str:
        """
        Build full URL for ESI endpoint.
        
        Args:
            endpoint: API endpoint path
            version: API version (default: 'latest')
            
        Returns:
            Full URL string
        """
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
            
        return urljoin(self.BASE_URL, f'/{version}{endpoint}')
    
    def _prepare_headers(self, character_id: Optional[str] = None, 
                        additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Prepare request headers including authentication.
        
        Args:
            character_id: Character ID for authenticated requests
            additional_headers: Additional headers to include
            
        Returns:
            Dictionary of headers
        """
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        if character_id and self.auth:
            access_token = self.auth.get_valid_token(character_id)
            if access_token:
                headers['Authorization'] = f'Bearer {access_token}'
            else:
                raise ESIAuthenticationError(f"No valid token for character {character_id}")
        
        if additional_headers:
            headers.update(additional_headers)
            
        return headers
    
    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle API response and parse JSON.
        
        Args:
            response: Requests response object
            
        Returns:
            Parsed JSON data
            
        Raises:
            ESIException: For various API errors
        """
        # Log rate limit headers
        if 'X-ESI-Error-Limit-Remain' in response.headers:
            remaining = response.headers.get('X-ESI-Error-Limit-Remain')
            reset_time = response.headers.get('X-ESI-Error-Limit-Reset')
            logger.debug(f"ESI Error limit remaining: {remaining}, resets at: {reset_time}")
        
        # Handle different status codes
        if response.status_code == 200:
            try:
                return response.json() if response.content else None
            except ValueError:
                return response.text
                
        elif response.status_code == 204:
            return None
            
        elif response.status_code == 304:
            logger.debug("Data not modified (304)")
            return None
            
        elif response.status_code == 400:
            error_msg = f"Bad request: {response.text}"
            logger.error(error_msg)
            raise ESIException(error_msg)
            
        elif response.status_code == 401:
            error_msg = "Authentication failed"
            logger.error(error_msg)
            raise ESIAuthenticationError(error_msg)
            
        elif response.status_code == 403:
            error_msg = f"Forbidden: {response.text}"
            logger.error(error_msg)
            raise ESIException(error_msg)
            
        elif response.status_code == 404:
            error_msg = f"Not found: {response.url}"
            logger.warning(error_msg)
            raise ESIException(error_msg)
            
        elif response.status_code == 420:
            error_msg = "Error limit exceeded"
            logger.error(error_msg)
            raise ESIRateLimitError(error_msg)
            
        elif response.status_code == 429:
            error_msg = "Rate limit exceeded"
            logger.error(error_msg)
            raise ESIRateLimitError(error_msg)
            
        elif response.status_code >= 500:
            error_msg = f"Server error ({response.status_code}): {response.text}"
            logger.error(error_msg)
            raise ESIServerError(error_msg)
            
        else:
            error_msg = f"Unexpected status code {response.status_code}: {response.text}"
            logger.error(error_msg)
            raise ESIException(error_msg)
    
    def request(self, method: str, endpoint: str, character_id: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None, version: str = 'latest') -> Any:
        """
        Make an authenticated request to the ESI API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            character_id: Character ID for authenticated requests
            params: Query parameters
            json_data: JSON data for POST/PUT requests
            headers: Additional headers
            version: API version
            
        Returns:
            Parsed response data
            
        Raises:
            ESIException: For various API errors
        """
        url = self._build_url(endpoint, version)
        request_headers = self._prepare_headers(character_id, headers)
        
        # Add default parameters
        if params is None:
            params = {}
        params.setdefault('datasource', self.DEFAULT_DATASOURCE)
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=request_headers,
                params=params,
                json=json_data,
                timeout=self.timeout
            )
            
            return self._handle_response(response)
            
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout for {url}"
            logger.error(error_msg)
            raise ESIException(error_msg)
            
        except requests.exceptions.ConnectionError:
            error_msg = f"Connection error for {url}"
            logger.error(error_msg)
            raise ESIException(error_msg)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed for {url}: {e}"
            logger.error(error_msg)
            raise ESIException(error_msg)
    
    def get(self, endpoint: str, character_id: Optional[str] = None, 
            params: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a GET request."""
        return self.request('GET', endpoint, character_id, params, **kwargs)
    
    def post(self, endpoint: str, character_id: Optional[str] = None,
             json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a POST request."""
        return self.request('POST', endpoint, character_id, json_data=json_data, **kwargs)
    
    def put(self, endpoint: str, character_id: Optional[str] = None,
            json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Any:
        """Make a PUT request."""
        return self.request('PUT', endpoint, character_id, json_data=json_data, **kwargs)
    
    def delete(self, endpoint: str, character_id: Optional[str] = None, **kwargs) -> Any:
        """Make a DELETE request."""
        return self.request('DELETE', endpoint, character_id, **kwargs)
    
    def get_server_status(self) -> Dict[str, Any]:
        """
        Get EVE Online server status.
        
        Returns:
            Server status information
        """
        return self.get('/status/')
    
    def get_universe_types(self, type_ids: list) -> Dict[str, Any]:
        """
        Get information about universe types.
        
        Args:
            type_ids: List of type IDs
            
        Returns:
            Type information
        """
        return self.post('/universe/names/', json_data=type_ids)
