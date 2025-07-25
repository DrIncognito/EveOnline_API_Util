# EVE Online API Utility Library

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/eveonline-api-util.svg)](https://badge.fury.io/py/eveonline-api-util)

A comprehensive Python library for EVE Online ESI API integration with OAuth2 authentication, token management, and modular endpoint access. Designed to be usable in various Python applications including Flask web apps, PyQt desktop applications, and command-line tools.

## Features

- **OAuth2 Authentication**: Complete OAuth2 flow implementation using `requests_oauthlib`
- **Token Management**: Automatic token refresh, secure storage, and lifecycle management
- **Modular Design**: Organized endpoint access with dedicated modules for different API areas
- **Generic ESI Client**: Flexible client wrapper with automatic error handling and rate limiting
- **CLI Interface**: Command-line interface for quick API access and token management
- **Framework Agnostic**: Usable in Flask, PyQt, Django, or any Python application
- **Comprehensive Testing**: Full test coverage with mocked ESI responses
- **Type Hints**: Complete type annotations for better IDE support and code quality
- **Configurable**: Environment-based configuration with `.env` file support

## Installation

### From PyPI (when published)
```bash
pip install eveonline-api-util
```

### From Source
```bash
git clone https://github.com/DrIncognito/EveOnline_API_Util.git
cd EveOnline_API_Util
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/DrIncognito/EveOnline_API_Util.git
cd EveOnline_API_Util
pip install -e ".[dev]"
```

## Quick Start

### 1. EVE Application Setup

First, create an EVE Online application at [https://developers.eveonline.com/applications](https://developers.eveonline.com/applications):

1. Click "Create New Application"
2. Fill in application details
3. Set callback URL (e.g., `http://localhost:8000/callback`)
4. Select required scopes
5. Note your `Client ID` and `Client Secret`

### 2. Configuration

Copy `.env.example` to `.env` and configure your application:

```bash
cp .env.example .env
```

Edit `.env`:
```env
EVE_CLIENT_ID=your_client_id_here
EVE_CLIENT_SECRET=your_client_secret_here
EVE_REDIRECT_URI=http://localhost:8000/callback
EVE_SCOPES=esi-wallet.read_character_wallet.v1,esi-characters.read_corporation_history.v1
EVE_TOKEN_FILE=tokens.json
```

### 3. Basic Usage

#### Authentication
```python
from eveonline_api_util import EVEAuth, TokenManager, ESIClient

# Initialize authentication
token_manager = TokenManager('tokens.json')
auth = EVEAuth(
    client_id='your_client_id',
    client_secret='your_client_secret',
    redirect_uri='http://localhost:8000/callback',
    scopes=['esi-wallet.read_character_wallet.v1'],
    token_manager=token_manager
)

# Get authorization URL
auth_url, state = auth.get_authorization_url()
print(f"Visit: {auth_url}")

# After user authorizes, handle callback
callback_url = input("Enter callback URL: ")
token = auth.handle_callback(callback_url, state)
print(f"Authenticated: {token['CharacterName']}")
```

#### Using the ESI Client
```python
from eveonline_api_util import ESIClient
from eveonline_api_util.endpoints import CharacterEndpoint, WalletEndpoint

# Initialize client
client = ESIClient(auth)

# Use endpoint modules
character_api = CharacterEndpoint(client)
wallet_api = WalletEndpoint(client)

# Get character information
character_id = '12345'
char_info = character_api.get_character_public_info(int(character_id))
print(f"Character: {char_info['name']}")

# Get wallet balance (requires authentication)
balance = wallet_api.get_character_wallet_balance(character_id)
print(f"Wallet Balance: {balance:,.2f} ISK")
```

### 4. Using in Different Frameworks

#### Flask Web Application
```python
from flask import Flask, session, redirect, url_for, request
from eveonline_api_util import EVEAuth, TokenManager, ESIClient

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Initialize EVE auth
auth = EVEAuth(client_id, client_secret, redirect_uri, scopes)

@app.route('/login')
def login():
    auth_url, state = auth.get_authorization_url()
    session['oauth_state'] = state
    return redirect(auth_url)

@app.route('/callback')
def callback():
    token = auth.handle_callback(request.url, session.get('oauth_state'))
    session['character_id'] = str(token['CharacterID'])
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    character_id = session.get('character_id')
    if not character_id:
        return redirect(url_for('login'))
    
    client = ESIClient(auth)
    wallet_api = WalletEndpoint(client)
    balance = wallet_api.get_character_wallet_balance(character_id)
    
    return f"Your wallet balance: {balance:,.2f} ISK"
```

#### PyQt Desktop Application
```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from eveonline_api_util import EVEAuth, ESIClient
from eveonline_api_util.endpoints import CharacterEndpoint

class EVEAuthThread(QThread):
    auth_complete = pyqtSignal(dict)
    
    def __init__(self, auth, callback_url, state):
        super().__init__()
        self.auth = auth
        self.callback_url = callback_url
        self.state = state
    
    def run(self):
        try:
            token = self.auth.handle_callback(self.callback_url, self.state)
            self.auth_complete.emit(token)
        except Exception as e:
            self.auth_complete.emit({'error': str(e)})

class EVEApp(QWidget):
    def __init__(self):
        super().__init__()
        self.auth = EVEAuth(client_id, client_secret, redirect_uri, scopes)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.login_btn = QPushButton('Login to EVE Online')
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)
        
        self.status_label = QLabel('Not logged in')
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def login(self):
        auth_url, state = self.auth.get_authorization_url()
        # Open auth_url in browser, get callback_url from user
        # For demo purposes, assume we have the callback_url
        callback_url = "http://localhost:8000/callback?code=..."
        
        self.auth_thread = EVEAuthThread(self.auth, callback_url, state)
        self.auth_thread.auth_complete.connect(self.on_auth_complete)
        self.auth_thread.start()
    
    def on_auth_complete(self, token):
        if 'error' in token:
            self.status_label.setText(f"Error: {token['error']}")
        else:
            self.status_label.setText(f"Logged in as: {token['CharacterName']}")

app = QApplication(sys.argv)
window = EVEApp()
window.show()
sys.exit(app.exec_())
```

## CLI Usage

The library includes a command-line interface:

```bash
# Authenticate with EVE Online
eve-api-util auth

# List stored authentication tokens
eve-api-util list-tokens

# Get character information
eve-api-util character-info 12345 --public

# Get wallet balance
eve-api-util wallet-balance 12345

# Get server status
eve-api-util server-status

# Revoke stored token
eve-api-util revoke-token 12345
```

## API Reference

### Core Classes

#### `EVEAuth`
Handles OAuth2 authentication flow.

```python
auth = EVEAuth(
    client_id='your_client_id',
    client_secret='your_client_secret',
    redirect_uri='http://localhost:8000/callback',
    scopes=['esi-wallet.read_character_wallet.v1'],
    token_manager=token_manager
)

# Get authorization URL
auth_url, state = auth.get_authorization_url()

# Handle callback
token = auth.handle_callback(callback_url, state)

# Get valid access token (with automatic refresh)
access_token = auth.get_valid_token(character_id)
```

#### `TokenManager`
Manages token storage and retrieval.

```python
token_manager = TokenManager('tokens.json')

# Store token
token_manager.store_token(character_id, token_data)

# Retrieve token
token = token_manager.get_token(character_id)

# Check if token is expired
is_expired = token_manager.is_token_expired(token)

# List all stored character IDs
character_ids = token_manager.list_characters()
```

#### `ESIClient`
Generic client for ESI API requests.

```python
client = ESIClient(auth=auth, timeout=30)

# Make requests
data = client.get('/characters/12345/')
client.post('/characters/12345/contacts/', json_data={...})

# Convenience methods
server_status = client.get_server_status()
```

### Endpoint Modules

#### `CharacterEndpoint`
Access character-related endpoints.

```python
char_api = CharacterEndpoint(client)

# Public information
public_info = char_api.get_character_public_info(character_id)
portrait = char_api.get_character_portrait(character_id)
corp_history = char_api.get_character_corporation_history(character_id)

# Authenticated information
attributes = char_api.get_character_attributes(character_id)
skills = char_api.get_character_skills(character_id)
location = char_api.get_character_location(character_id)
assets = char_api.get_character_assets(character_id)
```

#### `WalletEndpoint`
Access wallet-related endpoints.

```python
wallet_api = WalletEndpoint(client)

# Character wallet
balance = wallet_api.get_character_wallet_balance(character_id)
journal = wallet_api.get_character_wallet_journal(character_id)
transactions = wallet_api.get_character_wallet_transactions(character_id)

# Corporation wallet (requires roles)
corp_wallets = wallet_api.get_corporation_wallets(corp_id, character_id)
```

#### `FleetEndpoint`
Access fleet-related endpoints.

```python
fleet_api = FleetEndpoint(client)

# Fleet information
fleet_info = fleet_api.get_character_fleet_info(character_id)
members = fleet_api.get_fleet_members(fleet_id, character_id)

# Fleet management
fleet_api.invite_to_fleet(fleet_id, character_id, invitee_id)
fleet_api.update_fleet_info(fleet_id, character_id, motd="New MOTD")
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EVE_CLIENT_ID` | EVE application client ID | Required |
| `EVE_CLIENT_SECRET` | EVE application client secret | Required |
| `EVE_REDIRECT_URI` | OAuth2 redirect URI | `http://localhost:8000/callback` |
| `EVE_SCOPES` | Comma-separated list of ESI scopes | Empty |
| `EVE_TOKEN_FILE` | Path to token storage file | `tokens.json` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Common ESI Scopes

- `esi-characters.read_corporation_history.v1` - Corporation history
- `esi-wallet.read_character_wallet.v1` - Wallet balance and journal
- `esi-skills.read_skills.v1` - Character skills
- `esi-location.read_location.v1` - Character location
- `esi-assets.read_assets.v1` - Character assets
- `esi-fleets.read_fleet.v1` - Fleet information
- `esi-fleets.write_fleet.v1` - Fleet management

Full scope list: [ESI Reference](https://esi.evetech.net/ui/)

## Error Handling

The library provides specific exception types:

```python
from eveonline_api_util.esi_client import (
    ESIException, ESIAuthenticationError, 
    ESIRateLimitError, ESIServerError
)

try:
    data = client.get('/characters/12345/')
except ESIAuthenticationError:
    print("Authentication failed - token may be expired")
except ESIRateLimitError:
    print("Rate limit exceeded - wait before retrying")
except ESIServerError:
    print("ESI server error - try again later")
except ESIException as e:
    print(f"API error: {e}")
```

## Testing

Run the test suite:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/eveonline_api_util --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [EVE Online ESI API](https://esi.evetech.net/ui/) - The API this library wraps
- [CCP Games](https://www.ccpgames.com/) - For creating EVE Online
- [requests-oauthlib](https://github.com/requests/requests-oauthlib) - OAuth2 implementation

## Support

- **Issues**: [GitHub Issues](https://github.com/DrIncognito/EveOnline_API_Util/issues)
- **Documentation**: This README and inline docstrings
- **EVE Online Third-Party Development**: [EVE Developers](https://developers.eveonline.com/)

## Changelog

### Version 1.0.0
- Initial release
- OAuth2 authentication with automatic token refresh
- Modular endpoint access (Character, Wallet, Fleet)
- Generic ESI client with error handling
- CLI interface
- Comprehensive test coverage
- Framework-agnostic design for Flask, PyQt, etc.