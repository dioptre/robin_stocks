"""STATELESS orders functions - NO GLOBAL STATE"""

from typing import Dict, List, Any, Optional, Union
from .helper import _make_request, id_for_option, request_get, round_price
from .urls import (
    account_profile_url, crypto_account_url, crypto_cancel_url, 
    crypto_orders_url, order_crypto_url, option_cancel_url,
    cancel_url, orders_url, option_orders_url, instruments_url,
    option_instruments_url
)

# STATELESS REPLACEMENTS for all order functions - NO MORE BLOCKING!

# ========================
# ENHANCED HELPER FUNCTIONS - Using indexzero pattern
# ========================

def _get_account_url(access_token: str) -> Optional[str]:
    """Get the account URL for the authenticated user - ENHANCED VERSION"""
    first_account = request_get(access_token, account_profile_url(), data_type='indexzero')
    return first_account.get('url') if first_account else None

def _get_crypto_account_url(access_token: str) -> Optional[str]:
    """Get the crypto account URL for the authenticated user - ENHANCED VERSION"""
    first_crypto_account = request_get(access_token, crypto_account_url(), data_type='indexzero')
    if first_crypto_account:
        # Crypto accounts don't have 'url' field, construct it from 'id'
        account_id = first_crypto_account.get('id')
        if account_id:
            return f'https://nummus.robinhood.com/accounts/{account_id}/'
    return None


def _get_first_account(access_token: str) -> Optional[Dict[str, Any]]:
    """Get the full first account object for the authenticated user"""
    return request_get(access_token, account_profile_url(), data_type='indexzero')

def _get_first_crypto_account(access_token: str) -> Optional[Dict[str, Any]]:
    """Get the full first crypto account object for the authenticated user"""
    return request_get(access_token, crypto_account_url(), data_type='indexzero')

def _get_instrument_by_symbol(access_token: str, symbol: str) -> Optional[Dict[str, Any]]:
    """Get instrument data for a symbol using indexzero pattern"""
    return request_get(access_token, instruments_url(), data_type='indexzero', 
                      payload={'symbol': symbol.upper().strip()})

def cancel_all_crypto_orders(access_token: str) -> bool:
    """Cancel all crypto orders - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    orders = get_all_crypto_orders(access_token)
    
    for order in orders:
        if order.get('state') in ['queued', 'unconfirmed']:
            order_id = order.get('id')
            if order_id:
                _make_request('POST', crypto_cancel_url(order_id), headers=headers)
    
    return True

def cancel_all_option_orders(access_token: str) -> bool:
    """Cancel all option orders - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    orders = get_all_option_orders(access_token)
    
    for order in orders:
        if order.get('state') == 'queued':
            order_id = order.get('id')
            if order_id:
                _make_request('POST', option_cancel_url(order_id), headers=headers)
    
    return True

def cancel_all_stock_orders(access_token: str) -> bool:
    """Cancel all stock orders - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    orders = get_all_stock_orders(access_token)
    
    for order in orders:
        if order.get('state') == 'queued':
            order_id = order.get('id')
            if order_id:
                _make_request('POST', cancel_url(order_id), headers=headers)
    
    return True

def cancel_crypto_order(access_token: str, order_id: str) -> bool:
    """Cancel crypto order - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('POST', crypto_cancel_url(order_id), headers=headers)
    return response is not None

def cancel_option_order(access_token: str, order_id: str) -> bool:
    """Cancel option order - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('POST', option_cancel_url(order_id), headers=headers)
    return response is not None

def cancel_stock_order(access_token: str, order_id: str) -> bool:
    """Cancel stock order - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('POST', cancel_url(order_id), headers=headers)
    return response is not None

def find_stock_orders(access_token: str, **kwargs) -> List[Dict[str, Any]]:
    """Find stock orders with filters - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', orders_url(), headers=headers, params=kwargs)
    if response and 'results' in response:
        return response['results']
    return []

def get_all_crypto_orders(access_token: str) -> List[Dict[str, Any]]:
    """Get all crypto orders - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', crypto_orders_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_all_open_crypto_orders(access_token: str) -> List[Dict[str, Any]]:
    """Get all open crypto orders - STATELESS VERSION"""
    orders = get_all_crypto_orders(access_token)
    return [order for order in orders if order.get('state') in ['queued', 'unconfirmed']]

def get_all_open_option_orders(access_token: str) -> List[Dict[str, Any]]:
    """Get all open option orders - STATELESS VERSION"""
    orders = get_all_option_orders(access_token)
    return [order for order in orders if order.get('state') == 'queued']

def get_all_open_stock_orders(access_token: str) -> List[Dict[str, Any]]:
    """Get all open stock orders - STATELESS VERSION"""
    orders = get_all_stock_orders(access_token)
    return [order for order in orders if order.get('state') == 'queued']

def get_all_option_orders(access_token: str) -> List[Dict[str, Any]]:
    """Get all option orders - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', option_orders_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_all_stock_orders(access_token: str) -> List[Dict[str, Any]]:
    """Get all stock orders - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', orders_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_crypto_order_info(access_token: str, order_id: str) -> Optional[Dict]:
    """Get crypto order info - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    return _make_request('GET', crypto_orders_url(order_id), headers=headers)

def get_option_order_info(access_token: str, order_id: str) -> Optional[Dict]:
    """Get option order info - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    return _make_request('GET', option_orders_url(order_id), headers=headers)

def get_stock_order_info(access_token: str, order_id: str) -> Optional[Dict]:
    """Get stock order info - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    return _make_request('GET', orders_url(order_id), headers=headers)

def order(access_token: str, symbol: str, quantity: Union[int, float], side: str, 
          order_type: str = 'market', price: Optional[float] = None, stop_price: Optional[float] = None,
          time_in_force: str = 'gtc', market_hours: str = 'regular_hours', extended_hours: bool = False, **kwargs) -> Optional[Dict]:
    """Generic order function - STATELESS VERSION - Fixed to match original robin_stocks exactly"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(f"Symbol error: {message}")
        return None
    
    # Determine order type like original
    if price and stop_price:
        order_type = "stop_limit"
    elif price:
        order_type = "limit"
    elif stop_price:
        order_type = "stop_loss"
    else:
        order_type = "market"
    
    # Get account URL
    account_url = _get_account_url(access_token)
    if not account_url:
        return None
    
    # Get instrument
    instrument_response = _make_request('GET', instruments_url(), 
                                      headers=headers, params={'symbol': symbol})
    
    if not instrument_response or not instrument_response.get('results'):
        return None
    
    instrument_url = instrument_response['results'][0]['url']
    
    # Generate unique reference ID like original
    import uuid
    ref_id = str(uuid.uuid4())
    
    # Round quantity if it's a string (like original)
    if isinstance(quantity, str):
        quantity = round_price(quantity)
    
    # Fix extended_hours and market_hours consistency (like original)
    if extended_hours:
        market_hours = 'extended_hours'
        extended_hours = True
    else:
        market_hours = 'regular_hours'
        extended_hours = False
    
    # Build payload EXACTLY like original robin-stocks
    payload = {
        'account': account_url,
        'instrument': instrument_url,
        'symbol': symbol,
        'price': price,  # None for market orders - will be removed below
        'quantity': quantity,
        'ref_id': ref_id,
        'type': order_type,
        'stop_price': stop_price,  # None unless stop order - will be removed below
        'time_in_force': time_in_force,
        'trigger': 'immediate',
        'side': side,
        'extended_hours': extended_hours,
        'market_hours': market_hours,
        'order_form_version': 4
    }
    
    # Remove all keys that have 'None' as value (CRITICAL - like original)
    payload = {key: value for key, value in payload.items() if value is not None}
    
    # Debug output
    print(f"ROBINHOOD PAYLOAD DEBUG: Full order payload for {symbol}: {payload}")
    
    return _make_request('POST', orders_url(), headers=headers, json=payload)

# Market order functions
def order_buy_market(access_token: str, symbol: str, quantity: Union[int, float], 
                     time_in_force: str = 'gfd', extended_hours: bool = False) -> Optional[Dict]:
    """Buy market order - STATELESS VERSION (supports fractional shares)"""
    return order(access_token, symbol, quantity, 'buy', 'market', 
                time_in_force=time_in_force, extended_hours=extended_hours)

def order_sell_market(access_token: str, symbol: str, quantity: Union[int, float], 
                      time_in_force: str = 'gfd', extended_hours: bool = False) -> Optional[Dict]:
    """Sell market order - STATELESS VERSION"""
    return order(access_token, symbol, quantity, 'sell', 'market', 
                time_in_force=time_in_force, extended_hours=extended_hours)

# Limit order functions
def order_buy_limit(access_token: str, symbol: str, quantity: int, price: float) -> Optional[Dict]:
    """Buy limit order - STATELESS VERSION"""
    return order(access_token, symbol, quantity, 'buy', 'limit', price)

def order_sell_limit(access_token: str, symbol: str, quantity: int, price: float) -> Optional[Dict]:
    """Sell limit order - STATELESS VERSION"""
    return order(access_token, symbol, quantity, 'sell', 'limit', price)

# Stop-loss order functions
def order_buy_stop_loss(access_token: str, symbol: str, quantity: int, stop_price: float) -> Optional[Dict]:
    """Buy stop-loss order - STATELESS VERSION"""
    return order(access_token, symbol, quantity, 'buy', 'market', trigger='stop', stop_price=str(stop_price))

def order_sell_stop_loss(access_token: str, symbol: str, quantity: int, stop_price: float) -> Optional[Dict]:
    """Sell stop-loss order - STATELESS VERSION"""
    return order(access_token, symbol, quantity, 'sell', 'market', trigger='stop', stop_price=str(stop_price))

# Stop-limit order functions  
def order_buy_stop_limit(access_token: str, symbol: str, quantity: int, price: float, stop_price: float) -> Optional[Dict]:
    """Buy stop-limit order - STATELESS VERSION"""
    return order(access_token, symbol, quantity, 'buy', 'limit', price, trigger='stop', stop_price=str(stop_price))

def order_sell_stop_limit(access_token: str, symbol: str, quantity: int, price: float, stop_price: float) -> Optional[Dict]:
    """Sell stop-limit order - STATELESS VERSION"""
    return order(access_token, symbol, quantity, 'sell', 'limit', price, trigger='stop', stop_price=str(stop_price))

# Trailing stop functions
def order_buy_trailing_stop(access_token: str, symbol: str, quantity: int, trailing_pct: float) -> Optional[Dict]:
    """Buy trailing stop order - STATELESS VERSION"""
    return order(access_token, symbol, quantity, 'buy', 'market', trigger='stop', trailing_pct=str(trailing_pct))

def order_sell_trailing_stop(access_token: str, symbol: str, quantity: int, trailing_pct: float) -> Optional[Dict]:
    """Sell trailing stop order - STATELESS VERSION"""
    return order(access_token, symbol, quantity, 'sell', 'market', trigger='stop', trailing_pct=str(trailing_pct))

# Fractional order functions
def order_buy_fractional_by_price(access_token: str, symbol: str, amount_in_dollars: float, 
                                  account_number: Optional[str] = None, time_in_force: str = 'gfd',
                                  extended_hours: bool = False, market_hours: str = 'regular_hours') -> Optional[Dict]:
    """Submits a market order to be executed immediately for fractional shares by specifying the amount in dollars.
    
    :param access_token: The access token for authentication
    :param symbol: The stock ticker of the stock to purchase
    :param amount_in_dollars: The amount in dollars of the fractional shares you want to buy
    :param account_number: the robinhood account number (optional)
    :param time_in_force: Changes how long the order will be in effect for. 'gfd' = good for the day
    :param extended_hours: Premium users only. Allows trading during extended hours
    :param market_hours: Market hours setting ('regular_hours' or 'extended_hours')
    :returns: Dictionary containing order information
    """
    if amount_in_dollars < 1:
        print(f"ERROR: Fractional share price should meet minimum 1.00, got {amount_in_dollars}")
        return None

    # Get the current ask price to calculate fractional shares (matching GitHub implementation)
    from .stocks import get_quotes
    quotes = get_quotes(access_token, [symbol])
    
    if not quotes or not quotes[0]:
        print(f"ERROR: Could not get quote for {symbol}")
        return None
    
    quote = quotes[0]
    ask_price = float(quote.get('ask_price', 0.0))
    
    if ask_price == 0.0:
        print(f"ERROR: Invalid ask price for {symbol}")
        return None
    
    # Calculate fractional shares (matching GitHub logic)
    fractional_shares = round_price(amount_in_dollars / ask_price)
    
    print(f"ROBINHOOD DEBUG: {symbol} ask_price=${ask_price}, amount=${amount_in_dollars}, fractional_shares={fractional_shares}")
    
    # Use the generic order function like the GitHub version
    return order(access_token, symbol, fractional_shares, 'buy', 'market', 
                time_in_force=time_in_force, market_hours=market_hours)

def order_sell_fractional_by_price(access_token: str, symbol: str, amount: float) -> Optional[Dict]:
    """Sell fractional shares by dollar amount - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get account URL
    account_url = _get_account_url(access_token)
    if not account_url:
        return None
    
    instrument_response = _make_request('GET', instruments_url(), 
                                      headers=headers, params={'symbol': symbol})
    
    if not instrument_response or not instrument_response.get('results'):
        return None
    
    instrument_url = instrument_response['results'][0]['url']
    
    payload = {
        'account': account_url,
        'instrument': instrument_url,
        'symbol': symbol,
        'side': 'sell',
        'dollar_based_amount': str(amount),
        'type': 'market',
        'time_in_force': 'gfd'
    }
    
    return _make_request('POST', orders_url(), headers=headers, json=payload)

def order_buy_fractional_by_quantity(access_token: str, symbol: str, quantity: float) -> Optional[Dict]:
    """Buy fractional shares by quantity - STATELESS VERSION (matching original robin-stocks)"""
    # Use the standard order function like the original implementation
    return order(access_token, symbol, quantity, 'buy', 'market', 
                time_in_force='gfd', market_hours='regular_hours')

def order_sell_fractional_by_quantity(access_token: str, symbol: str, quantity: float) -> Optional[Dict]:
    """Sell fractional shares by quantity - STATELESS VERSION"""
    # Use 'gfd' (good for day) like original GitHub implementation
    return order(access_token, symbol, quantity, 'sell', 'market', time_in_force='gfd')

# Crypto order functions  
def order_buy_crypto_by_price(access_token: str, symbol: str, amount_in_dollars: float) -> Optional[Dict]:
    """Buy crypto by dollar amount - STATELESS VERSION (matching GitHub logic)"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get crypto account ID (not URL)
    first_crypto_account = request_get(access_token, crypto_account_url(), data_type='indexzero')
    if not first_crypto_account:
        return None
    
    account_id = first_crypto_account.get('id')
    if not account_id:
        return None
    
    # Get crypto quote for price calculation (like GitHub)
    from .crypto import get_crypto_quote_from_id
    
    # Symbol should be the currency pair ID
    crypto_price = get_crypto_quote_from_id(access_token, symbol, info='ask_price')
    if not crypto_price:
        return None
    
    crypto_price_float = round(float(crypto_price), 2)  # Round to nearest cent
    
    # Calculate quantity from dollar amount (like GitHub)
    from .helper import round_price
    quantity = round_price(amount_in_dollars / crypto_price_float)
    
    # Generate unique reference ID (like GitHub)
    import uuid
    ref_id = str(uuid.uuid4())
    
    # Build payload matching GitHub format exactly
    payload = {
        'account_id': account_id,
        'currency_pair_id': symbol,  # Should be the pair ID
        'price': str(crypto_price_float),
        'quantity': str(quantity),
        'ref_id': ref_id,
        'side': 'buy',
        'time_in_force': 'gtc',
        'type': 'market'
    }
    
    result = _make_request('POST', order_crypto_url(), headers=headers, json=payload)
    
    return result

def order_sell_crypto_by_price(access_token: str, symbol: str, amount: float) -> Optional[Dict]:
    """Sell crypto by dollar amount - STATELESS VERSION (matching GitHub format)"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get crypto account ID (not URL)
    first_crypto_account = request_get(access_token, crypto_account_url(), data_type='indexzero')
    if not first_crypto_account:
        return None
    
    account_id = first_crypto_account.get('id')
    if not account_id:
        return None
    
    # Get current crypto price for quantity calculation (like GitHub)
    from .crypto import get_crypto_quote_from_id
    
    # Get bid price for sell orders (like GitHub)
    crypto_price = get_crypto_quote_from_id(access_token, symbol, info='bid_price')
    if not crypto_price:
        return None
    
    crypto_price_float = round(float(crypto_price), 2)  # Round to nearest cent
    
    # Calculate quantity from dollar amount (like GitHub)
    from .helper import round_price
    quantity = round_price(amount / crypto_price_float)
    
    # Generate unique reference ID (like GitHub)
    import uuid
    ref_id = str(uuid.uuid4())
    
    # Build payload matching GitHub format exactly
    payload = {
        'account_id': account_id,
        'currency_pair_id': symbol,  # Should be the pair ID
        'price': str(crypto_price_float),
        'quantity': str(quantity),
        'ref_id': ref_id,
        'side': 'sell',
        'time_in_force': 'gtc',
        'type': 'market'
    }
    
    return _make_request('POST', order_crypto_url(), headers=headers, json=payload)

def order_buy_crypto_by_quantity(access_token: str, symbol: str, quantity: float) -> Optional[Dict]:
    """Buy crypto by quantity - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get crypto account URL
    account_url = _get_crypto_account_url(access_token)
    if not account_url:
        return None
    
    payload = {
        'account': account_url,
        'currency_pair_id': symbol,
        'quantity': str(quantity),
        'side': 'buy',
        'time_in_force': 'gtc',
        'type': 'market'
    }
    
    return _make_request('POST', order_crypto_url(), headers=headers, json=payload)

def order_sell_crypto_by_quantity(access_token: str, symbol: str, quantity: float) -> Optional[Dict]:
    """Sell crypto by quantity - STATELESS VERSION (matching GitHub format)"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get crypto account ID (not URL)
    first_crypto_account = request_get(access_token, crypto_account_url(), data_type='indexzero')
    if not first_crypto_account:
        return None
    
    account_id = first_crypto_account.get('id')
    if not account_id:
        return None
    
    # Get current crypto price (like GitHub)
    from .crypto import get_crypto_quote_from_id
    
    # Get bid price for sell orders (like GitHub)
    crypto_price = get_crypto_quote_from_id(access_token, symbol, info='bid_price')
    if not crypto_price:
        return None
    
    crypto_price_float = round(float(crypto_price), 2)  # Round to nearest cent
    
    # Generate unique reference ID (like GitHub)
    import uuid
    ref_id = str(uuid.uuid4())
    
    # Build payload matching GitHub format exactly
    payload = {
        'account_id': account_id,
        'currency_pair_id': symbol,  # Should be the pair ID
        'price': str(crypto_price_float),
        'quantity': str(quantity),
        'ref_id': ref_id,
        'side': 'sell',
        'time_in_force': 'gtc',
        'type': 'market'
    }
    
    return _make_request('POST', order_crypto_url(), headers=headers, json=payload)

def order_crypto(access_token: str, symbol: str, side: str, quantity: Optional[float] = None, 
                price: Optional[float] = None, order_type: str = 'market') -> Optional[Dict]:
    """Generic crypto order - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get crypto account URL
    account_url = _get_crypto_account_url(access_token)
    if not account_url:
        return None
    
    payload = {
        'account': account_url,
        'currency_pair_id': symbol,
        'side': side,
        'time_in_force': 'gtc',
        'type': order_type
    }
    
    if quantity:
        payload['quantity'] = str(quantity)
    if price:
        payload['price'] = str(price)
    
    return _make_request('POST', order_crypto_url(), headers=headers, json=payload)

def order_buy_crypto_limit(access_token: str, symbol: str, quantity: float, price: float) -> Optional[Dict]:
    """Buy crypto limit order - STATELESS VERSION"""
    return order_crypto(access_token, symbol, 'buy', quantity=quantity, price=price, order_type='limit')

def order_sell_crypto_limit(access_token: str, symbol: str, quantity: float, price: float) -> Optional[Dict]:
    """Sell crypto limit order - STATELESS VERSION"""
    return order_crypto(access_token, symbol, 'sell', quantity=quantity, price=price, order_type='limit')

def order_buy_crypto_limit_by_price(access_token: str, symbol: str, amount: float, price: float) -> Optional[Dict]:
    """Buy crypto limit by dollar amount - STATELESS VERSION"""
    return order_crypto(access_token, symbol, 'buy', price=amount, order_type='limit')

def order_sell_crypto_limit_by_price(access_token: str, symbol: str, amount: float, price: float) -> Optional[Dict]:
    """Sell crypto limit by dollar amount - STATELESS VERSION"""
    return order_crypto(access_token, symbol, 'sell', price=amount, order_type='limit')

# ============================================================================
# OPTION ORDER FUNCTIONS - STATELESS IMPLEMENTATIONS
# ============================================================================

def order_buy_option_limit(access_token: str, symbol: str, expiration_date: str, strike: float, 
                          option_type: str, quantity: int, price: float) -> Optional[Dict]:
    """Buy option limit order - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get account URL
    account_url = _get_account_url(access_token)
    if not account_url:
        return None
    
    # Get option instrument ID
    option_id = id_for_option(access_token, symbol, expiration_date, strike, option_type)
    if not option_id:
        return None
    
    payload = {
        'account': account_url,
        'direction': 'debit',
        'time_in_force': 'gfd',
        'legs': [
            {
                'side': 'buy',
                'option': option_instruments_url(option_id),
                'position_effect': 'open',
                'ratio_quantity': 1
            }
        ],
        'type': 'limit',
        'trigger': 'immediate',
        'quantity': str(quantity),
        'price': str(price)
    }
    
    return _make_request('POST', option_orders_url(), headers=headers, json=payload)

def order_sell_option_limit(access_token: str, symbol: str, expiration_date: str, strike: float, 
                           option_type: str, quantity: int, price: float) -> Optional[Dict]:
    """Sell option limit order - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get account URL
    account_url = _get_account_url(access_token)
    if not account_url:
        return None
    
    # Get option instrument ID
    option_id = id_for_option(access_token, symbol, expiration_date, strike, option_type)
    if not option_id:
        return None
    
    payload = {
        'account': account_url,
        'direction': 'credit',
        'time_in_force': 'gfd',
        'legs': [
            {
                'side': 'sell',
                'option': option_instruments_url(option_id),
                'position_effect': 'close',
                'ratio_quantity': 1
            }
        ],
        'type': 'limit',
        'trigger': 'immediate',
        'quantity': str(quantity),
        'price': str(price)
    }
    
    return _make_request('POST', option_orders_url(), headers=headers, json=payload)

def order_buy_option_stop_limit(access_token: str, symbol: str, expiration_date: str, strike: float, 
                               option_type: str, quantity: int, price: float, stop_price: float) -> Optional[Dict]:
    """Buy option stop limit order - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get account URL
    account_url = _get_account_url(access_token)
    if not account_url:
        return None
    
    # Get option instrument ID
    option_id = id_for_option(access_token, symbol, expiration_date, strike, option_type)
    if not option_id:
        return None
    
    payload = {
        'account': account_url,
        'direction': 'debit',
        'time_in_force': 'gfd',
        'legs': [
            {
                'side': 'buy',
                'option': option_instruments_url(option_id),
                'position_effect': 'open',
                'ratio_quantity': 1
            }
        ],
        'type': 'limit',
        'trigger': 'stop',
        'quantity': str(quantity),
        'price': str(price),
        'stop_price': str(stop_price)
    }
    
    return _make_request('POST', option_orders_url(), headers=headers, json=payload)

def order_sell_option_stop_limit(access_token: str, symbol: str, expiration_date: str, strike: float, 
                                option_type: str, quantity: int, price: float, stop_price: float) -> Optional[Dict]:
    """Sell option stop limit order - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get account URL
    account_url = _get_account_url(access_token)
    if not account_url:
        return None
    
    # Get option instrument ID
    option_id = id_for_option(access_token, symbol, expiration_date, strike, option_type)
    if not option_id:
        return None
    
    payload = {
        'account': account_url,
        'direction': 'credit',
        'time_in_force': 'gfd',
        'legs': [
            {
                'side': 'sell',
                'option': option_instruments_url(option_id),
                'position_effect': 'close',
                'ratio_quantity': 1
            }
        ],
        'type': 'limit',
        'trigger': 'stop',
        'quantity': str(quantity),
        'price': str(price),
        'stop_price': str(stop_price)
    }
    
    return _make_request('POST', option_orders_url(), headers=headers, json=payload)

def order_option_spread(access_token: str, symbol: str, expiration_date: str, 
                       buy_strike: float, sell_strike: float, option_type: str, 
                       quantity: int, price: float, direction: str = 'debit') -> Optional[Dict]:
    """Generic option spread order - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get account URL
    account_url = _get_account_url(access_token)
    if not account_url:
        return None
    
    # Get option instrument IDs
    buy_option_id = id_for_option(access_token, symbol, expiration_date, buy_strike, option_type)
    sell_option_id = id_for_option(access_token, symbol, expiration_date, sell_strike, option_type)
    
    if not buy_option_id or not sell_option_id:
        return None
    
    payload = {
        'account': account_url,
        'direction': direction,
        'time_in_force': 'gfd',
        'legs': [
            {
                'side': 'buy',
                'option': option_instruments_url(buy_option_id),
                'position_effect': 'open',
                'ratio_quantity': 1
            },
            {
                'side': 'sell', 
                'option': option_instruments_url(sell_option_id),
                'position_effect': 'open',
                'ratio_quantity': 1
            }
        ],
        'type': 'limit',
        'trigger': 'immediate',
        'quantity': str(quantity),
        'price': str(price)
    }
    
    return _make_request('POST', option_orders_url(), headers=headers, json=payload)

def order_option_credit_spread(access_token: str, symbol: str, expiration_date: str, 
                              short_strike: float, long_strike: float, option_type: str, 
                              quantity: int, price: float) -> Optional[Dict]:
    """Option credit spread order - STATELESS VERSION"""
    # For credit spreads: sell higher strike (short), buy lower strike (long)
    if option_type.lower() == 'put':
        # Put credit spread: sell higher strike, buy lower strike
        return order_option_spread(access_token, symbol, expiration_date, 
                                 long_strike, short_strike, option_type, 
                                 quantity, price, direction='credit')
    else:
        # Call credit spread: sell lower strike, buy higher strike  
        return order_option_spread(access_token, symbol, expiration_date, 
                                 short_strike, long_strike, option_type, 
                                 quantity, price, direction='credit')

def order_option_debit_spread(access_token: str, symbol: str, expiration_date: str, 
                             long_strike: float, short_strike: float, option_type: str, 
                             quantity: int, price: float) -> Optional[Dict]:
    """Option debit spread order - STATELESS VERSION"""
    # For debit spreads: buy higher strike (long), sell lower strike (short)  
    if option_type.lower() == 'call':
        # Call debit spread: buy lower strike, sell higher strike
        return order_option_spread(access_token, symbol, expiration_date, 
                                 long_strike, short_strike, option_type, 
                                 quantity, price, direction='debit')
    else:
        # Put debit spread: buy higher strike, sell lower strike
        return order_option_spread(access_token, symbol, expiration_date, 
                                 long_strike, short_strike, option_type, 
                                 quantity, price, direction='debit')
