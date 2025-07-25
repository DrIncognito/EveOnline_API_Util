#!/usr/bin/env python3
"""
Comprehensive Examples for EveOnline API Util Library

This file demonstrates usage of all ESI API endpoints including:
- Basic endpoint usage with the endpoint manager
- Individual endpoint examples
- Integration examples for Flask and PyQt
- Asyncio patterns for concurrent requests
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def example_endpoint_manager_comprehensive():
    """Comprehensive example using the ESIEndpointManager with all endpoints."""
    from eveonline_api_util import ESIEndpointManager
    
    # Initialize endpoint manager
    manager = ESIEndpointManager(
        client_id=os.getenv('ESI_CLIENT_ID', 'your_client_id'),
        client_secret=os.getenv('ESI_CLIENT_SECRET', 'your_client_secret'),
        redirect_uri=os.getenv('REDIRECT_URI', 'your_redirect_uri')
    )
    
    print("=== EVE Online ESI API Comprehensive Example ===\n")
    
    # Show all available endpoints
    print("Available endpoints:")
    for endpoint, description in manager.get_available_endpoints().items():
        print(f"  {endpoint}: {description}")
    print()
    
    # Example 1: Universe data (no authentication required)
    print("1. Universe Data Examples:")
    try:
        # Get all regions
        regions = manager.universe.get_universe_regions()
        print(f"   - Total regions in EVE: {len(regions)}")
        
        # Get details for The Forge (Jita's region)
        forge_info = manager.universe.get_universe_region(10000002)
        print(f"   - The Forge has {len(forge_info.get('constellations', []))} constellations")
        
        # Get all systems
        systems = manager.universe.get_universe_systems()
        print(f"   - Total systems in EVE: {len(systems)}")
        
        # Get system details for Jita
        jita_info = manager.universe.get_universe_system(30000142)
        print(f"   - Jita system: {jita_info.get('name')} (Security: {jita_info.get('security_status', 0):.2f})")
        
    except Exception as e:
        print(f"   Error fetching universe data: {e}")
    print()
    
    # Example 2: Market data (no authentication required)
    print("2. Market Data Examples:")
    try:
        # Get market orders for Tritanium in The Forge
        tritanium_orders = manager.market.get_market_orders(10000002, type_id=34)
        buy_orders = [o for o in tritanium_orders if o['is_buy_order']]
        sell_orders = [o for o in tritanium_orders if not o['is_buy_order']]
        
        print(f"   - Tritanium orders in The Forge: {len(tritanium_orders)} total")
        print(f"     * Buy orders: {len(buy_orders)}")
        print(f"     * Sell orders: {len(sell_orders)}")
        
        if sell_orders:
            min_sell = min(sell_orders, key=lambda x: x['price'])
            print(f"     * Lowest sell price: {min_sell['price']:.2f} ISK")
        
        # Get market history
        market_history = manager.market.get_market_history(10000002, 34)
        if market_history:
            latest_day = market_history[-1]
            print(f"   - Latest trading day average: {latest_day['average']:.2f} ISK")
            print(f"     * Volume traded: {latest_day['volume']:,}")
        
    except Exception as e:
        print(f"   Error fetching market data: {e}")
    print()
    
    # Example 3: Wars data (no authentication required)
    print("3. Wars Data Examples:")
    try:
        wars = manager.wars.get_wars()
        print(f"   - Current wars in EVE: {len(wars)}")
        
        if wars:
            # Get details for the most recent war
            recent_war_id = max(wars)
            war_details = manager.wars.get_war(recent_war_id)
            print(f"   - Most recent war ID {recent_war_id}:")
            print(f"     * Started: {war_details.get('started')}")
            print(f"     * Aggressor: {war_details.get('aggressor', {}).get('corporation_id', 'Unknown')}")
            
    except Exception as e:
        print(f"   Error fetching wars data: {e}")
    print()
    
    # Example 4: Sovereignty data (no authentication required)
    print("4. Sovereignty Data Examples:")
    try:
        sov_campaigns = manager.sovereignty.get_sovereignty_campaigns()
        print(f"   - Active sovereignty campaigns: {len(sov_campaigns)}")
        
        sov_map = manager.sovereignty.get_sovereignty_map()
        print(f"   - Systems with sovereignty: {len(sov_map)}")
        
        sov_structures = manager.sovereignty.get_sovereignty_structures()
        print(f"   - Sovereignty structures: {len(sov_structures)}")
        
    except Exception as e:
        print(f"   Error fetching sovereignty data: {e}")
    print()
    
    # Example 5: Insurance data (no authentication required)
    print("5. Insurance Data Examples:")
    try:
        insurance_prices = manager.insurance.get_insurance_prices()
        print(f"   - Insurance available for {len(insurance_prices)} ship types")
        
        if insurance_prices:
            example_ship = insurance_prices[0]
            print(f"   - Example: Type ID {example_ship['type_id']}")
            for level in example_ship.get('levels', []):
                print(f"     * {level['name']}: {level['cost']:,} ISK (payout: {level['payout']:,} ISK)")
                break  # Just show first level
        
    except Exception as e:
        print(f"   Error fetching insurance data: {e}")
    print()
    
    # Example 6: Incursions data (no authentication required)
    print("6. Incursions Data Examples:")
    try:
        incursions = manager.incursions.get_incursions()
        print(f"   - Active incursions: {len(incursions)}")
        
        for incursion in incursions[:2]:  # Show first 2
            print(f"   - Incursion in {incursion.get('constellation_id')}")
            print(f"     * State: {incursion.get('state')}")
            print(f"     * Influence: {incursion.get('influence'):.2f}")
        
    except Exception as e:
        print(f"   Error fetching incursions data: {e}")
    print()

def example_individual_endpoints():
    """Examples of using individual endpoints directly."""
    from eveonline_api_util import ESIClient, EVEAuth, TokenManager
    from eveonline_api_util.endpoints import UniverseEndpoint, MarketEndpoint, WarsEndpoint
    
    print("=== Individual Endpoint Usage Examples ===\n")
    
    # Initialize authenticator and client
    token_manager = TokenManager()
    authenticator = EVEAuth(
        client_id=os.getenv('ESI_CLIENT_ID', 'your_client_id'),
        client_secret=os.getenv('ESI_CLIENT_SECRET', 'your_client_secret'),
        redirect_uri=os.getenv('REDIRECT_URI', 'your_redirect_uri'),
        scopes=[],
        token_manager=token_manager
    )
    
    client = ESIClient(authenticator)
    
    # Initialize specific endpoints
    universe = UniverseEndpoint(client)
    market = MarketEndpoint(client)
    wars = WarsEndpoint(client)
    
    print("1. Universe Endpoint Examples:")
    try:
        # Get and resolve some names
        names_to_resolve = ['Jita', 'Amarr', 'Dodixie', 'Rens', 'Hek']
        resolved_ids = universe.post_universe_ids(names_to_resolve)
        
        print(f"   Resolved trade hub names:")
        for category, items in resolved_ids.items():
            if items:
                print(f"   - {category}: {len(items)} items")
                for item in items[:2]:  # Show first 2
                    print(f"     * {item['name']} (ID: {item['id']})")
        
    except Exception as e:
        print(f"   Error with universe endpoint: {e}")
    print()
    
    print("2. Market Endpoint Examples:")
    try:
        # Get market groups
        market_groups = market.get_market_groups()
        print(f"   - Market groups available: {len(market_groups)}")
        
        # Get market prices
        market_prices = market.get_market_prices()
        if market_prices:
            print(f"   - Market prices for {len(market_prices)} items")
            # Find Tritanium price
            tritanium_price = next((p for p in market_prices if p['type_id'] == 34), None)
            if tritanium_price:
                print(f"     * Tritanium average price: {tritanium_price['average_price']:.2f} ISK")
        
    except Exception as e:
        print(f"   Error with market endpoint: {e}")
    print()

def example_authenticated_endpoints_usage():
    """Example showing how to use endpoints that require authentication."""
    print("=== Authenticated Endpoints Usage Example ===\n")
    
    print("Note: These examples show the API calls, but require actual authentication.")
    print("You would need to implement the OAuth2 flow first.\n")
    
    # Example authentication flow (commented as it requires user interaction)
    """
    from eveonline_api_util import ESIEndpointManager
    
    manager = ESIEndpointManager(
        client_id='your_client_id',
        client_secret='your_client_secret',
        redirect_uri='your_redirect_uri'
    )
    
    # Step 1: Get authorization URL
    scopes = [
        'esi-characters.read_characters.v1',
        'esi-wallet.read_character_wallet.v1',
        'esi-assets.read_assets.v1',
        'esi-mail.read_mail.v1'
    ]
    auth_url = manager.authenticate(scopes)
    print(f"Visit: {auth_url}")
    
    # Step 2: After user authorizes, handle callback
    # authorization_code = 'code_from_callback'
    # character_id = 'character_id_from_token'
    # tokens = manager.handle_callback(authorization_code, character_id)
    
    # Step 3: Use authenticated endpoints
    character_info = manager.character.get_character_info(character_id)
    wallet_balance = manager.wallet.get_character_wallet(character_id)
    assets = manager.assets.get_character_assets(character_id)
    mail = manager.mail.get_character_mail(character_id)
    """
    
    print("Example authenticated API calls:")
    print("1. Character info: manager.character.get_character_info(character_id)")
    print("2. Wallet balance: manager.wallet.get_character_wallet(character_id)")
    print("3. Assets: manager.assets.get_character_assets(character_id)")
    print("4. Mail: manager.mail.get_character_mail(character_id)")
    print("5. Skills: manager.skills.get_character_skills(character_id)")
    print("6. Location: manager.locations.get_character_location(character_id)")
    print("7. Fittings: manager.fittings.get_character_fittings(character_id)")
    print("8. Calendar: manager.calendar.get_character_calendar(character_id)")
    print("9. Bookmarks: manager.bookmarks.get_character_bookmarks(character_id)")
    print()

def example_cli_usage():
    """Example of using the CLI interface."""
    print("=== CLI Usage Examples ===\n")
    
    print("The library provides a CLI interface for quick data access:")
    print()
    print("1. Get character information:")
    print("   python -m eveonline_api_util character 123456789")
    print()
    print("2. Get wallet data:")
    print("   python -m eveonline_api_util wallet 123456789")
    print()
    print("3. Get fleet information:")
    print("   python -m eveonline_api_util fleet 123456789")
    print()
    print("4. Get market data:")
    print("   python -m eveonline_api_util market --region 10000002 --type-id 34")
    print()
    print("5. Get universe data:")
    print("   python -m eveonline_api_util universe --systems")
    print("   python -m eveonline_api_util universe --regions")
    print()
    print("6. Get wars data:")
    print("   python -m eveonline_api_util wars")
    print()

def example_flask_integration():
    """Example of integrating with Flask web application."""
    print("=== Flask Integration Example ===\n")
    
    print("Flask integration example (requires flask: pip install flask):")
    print()
    
    example_code = '''
from flask import Flask, request, session, redirect, url_for, jsonify
from eveonline_api_util import ESIEndpointManager

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize endpoint manager
esi_manager = ESIEndpointManager(
    client_id='your_client_id',
    client_secret='your_client_secret', 
    redirect_uri='http://localhost:5000/callback'
)

@app.route('/')
def index():
    return """
    <h1>EVE Online ESI API Demo</h1>
    <a href="/login">Login with EVE</a><br>
    <a href="/market">Market Data</a><br>
    <a href="/universe">Universe Data</a>
    """

@app.route('/login')
def login():
    scopes = ['esi-characters.read_characters.v1']
    auth_url = esi_manager.authenticate(scopes)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    # Handle authentication...
    return "Authentication handled"

@app.route('/market')
def market_data():
    try:
        orders = esi_manager.market.get_market_orders(10000002, type_id=34)
        return jsonify({
            "total_orders": len(orders),
            "buy_orders": len([o for o in orders if o['is_buy_order']]),
            "sell_orders": len([o for o in orders if not o['is_buy_order']])
        })
    except Exception as e:
        return f"Error: {e}"

@app.route('/universe')
def universe_data():
    try:
        regions = esi_manager.universe.get_universe_regions()
        systems = esi_manager.universe.get_universe_systems()
        return jsonify({
            "regions": len(regions),
            "systems": len(systems)
        })
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
'''
    
    print(example_code)
    print()

async def example_async_patterns():
    """Example of async patterns for concurrent API requests."""
    print("=== Async Patterns Example ===\n")
    
    from eveonline_api_util import ESIEndpointManager
    
    manager = ESIEndpointManager(
        client_id=os.getenv('ESI_CLIENT_ID', 'your_client_id'),
        client_secret=os.getenv('ESI_CLIENT_SECRET', 'your_client_secret'),
        redirect_uri=os.getenv('REDIRECT_URI', 'your_redirect_uri')
    )
    
    async def fetch_region_info(region_id):
        """Fetch information for a specific region."""
        try:
            # Note: Current implementation is sync, but shows the pattern
            region_info = manager.universe.get_universe_region(region_id)
            return {
                'region_id': region_id,
                'name': region_info.get('name', 'Unknown'),
                'constellations': len(region_info.get('constellations', []))
            }
        except Exception as e:
            return {'region_id': region_id, 'error': str(e)}
    
    async def fetch_market_data(region_id, type_id):
        """Fetch market data for a specific item in a region."""
        try:
            orders = manager.market.get_market_orders(region_id, type_id=type_id)
            return {
                'region_id': region_id,
                'type_id': type_id,
                'total_orders': len(orders),
                'buy_orders': len([o for o in orders if o['is_buy_order']]),
                'sell_orders': len([o for o in orders if not o['is_buy_order']])
            }
        except Exception as e:
            return {'region_id': region_id, 'type_id': type_id, 'error': str(e)}
    
    # Fetch data for multiple regions concurrently
    print("Fetching data for major trade regions...")
    major_regions = [10000002, 10000043, 10000032, 10000030, 10000042]  # Forge, Domain, Sinq Laison, Heimatar, Metropolis
    
    # Concurrent region info requests
    region_tasks = [fetch_region_info(region_id) for region_id in major_regions]
    region_results = await asyncio.gather(*region_tasks)
    
    print("Region Information:")
    for result in region_results:
        if 'error' in result:
            print(f"  Region {result['region_id']}: Error - {result['error']}")
        else:
            print(f"  {result['name']} ({result['region_id']}): {result['constellations']} constellations")
    
    # Concurrent market data requests for Tritanium
    print("\nFetching Tritanium market data for all regions...")
    market_tasks = [fetch_market_data(region_id, 34) for region_id in major_regions]
    market_results = await asyncio.gather(*market_tasks)
    
    print("Tritanium Market Data:")
    for result in market_results:
        if 'error' in result:
            print(f"  Region {result['region_id']}: Error - {result['error']}")
        else:
            print(f"  Region {result['region_id']}: {result['total_orders']} orders ({result['buy_orders']} buy, {result['sell_orders']} sell)")

def main():
    """Run all examples."""
    print("EVE Online API Util - Comprehensive Examples\n")
    print("=" * 60)
    
    # Run synchronous examples
    example_endpoint_manager_comprehensive()
    example_individual_endpoints()
    example_authenticated_endpoints_usage()
    example_cli_usage()
    example_flask_integration()
    
    # Run async example
    print("Running async patterns example...")
    asyncio.run(example_async_patterns())
    
    print("\n" + "=" * 60)
    print("Examples completed! Check the source code for implementation details.")

if __name__ == '__main__':
    main()
