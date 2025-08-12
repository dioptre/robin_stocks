"""STATELESS options functions - NO GLOBAL STATE"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from .helper import _make_request

# STATELESS REPLACEMENTS for all options functions - NO MORE BLOCKING!

def get_aggregate_positions(access_token: str, info: Optional[str] = None, account_number: Optional[str] = None) -> List[Dict[str, Any]]:
    """Collapses all option orders for a stock into a single dictionary - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    if account_number:
        url = f'https://robinhood.com/options/aggregate_positions/?account_number={account_number}'
    else:
        url = 'https://robinhood.com/options/aggregate_positions/'
    
    response = _make_request('GET', url, headers=headers)
    
    if response and 'results' in response:
        positions = response['results']
        if info:
            return [pos.get(info) for pos in positions if info in pos]
        return positions
    return []

def get_aggregate_open_positions(access_token: str, info: Optional[str] = None, account_number: Optional[str] = None) -> List[Dict[str, Any]]:
    """Collapses all open option positions for a stock into a single dictionary - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    if account_number:
        url = f'https://robinhood.com/options/aggregate_positions/?account_number={account_number}'
    else:
        url = 'https://robinhood.com/options/aggregate_positions/'
    
    params = {'nonzero': 'true'}
    response = _make_request('GET', url, headers=headers, params=params)
    
    if response and 'results' in response:
        positions = response['results']
        if info:
            return [pos.get(info) for pos in positions if info in pos]
        return positions
    return []

def get_all_option_positions(access_token: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns all option positions - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', 'https://robinhood.com/options/positions/', headers=headers)
    
    if response and 'results' in response:
        positions = response['results']
        if info:
            return [pos.get(info) for pos in positions if info in pos]
        return positions
    return []

def get_open_option_positions(access_token: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns open option positions - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'nonzero': 'true'}
    response = _make_request('GET', 'https://robinhood.com/options/positions/', headers=headers, params=params)
    
    if response and 'results' in response:
        positions = response['results']
        if info:
            return [pos.get(info) for pos in positions if info in pos]
        return positions
    return []

def get_chains(access_token: str, symbol: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get options chains for symbol - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # First get the instrument
    instrument_response = _make_request('GET', 'https://robinhood.com/instruments/', 
                                      headers=headers, params={'symbol': symbol})
    
    if not instrument_response or not instrument_response.get('results'):
        return []
    
    instrument_id = instrument_response['results'][0]['id']
    response = _make_request('GET', f'https://robinhood.com/options/chains/?equity_instrument_ids={instrument_id}', 
                           headers=headers)
    
    if response and 'results' in response:
        chains = response['results']
        if info:
            return [chain.get(info) for chain in chains if info in chain]
        return chains
    return []

def get_market_options(access_token: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get market options data - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', 'https://robinhood.com/options/instruments/', headers=headers)
    
    if response and 'results' in response:
        options = response['results']
        if info:
            return [opt.get(info) for opt in options if info in opt]
        return options
    return []

def get_option_historicals(access_token: str, option_id: str, interval: str = '5minute', 
                          span: str = 'day', info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get option historical data - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    params = {
        'interval': interval,
        'span': span
    }
    
    response = _make_request('GET', f'https://robinhood.com/options/instruments/{option_id}/historicals/', 
                           headers=headers, params=params)
    
    if response and 'data_points' in response:
        data = response['data_points']
        if info:
            return [point.get(info) for point in data if info in point]
        return data
    return []

def get_option_instrument_data(access_token: str, symbol: str, expiration_date: str, strike: float, 
                              option_type: str, info: Optional[str] = None) -> Optional[Dict]:
    """Get option instrument data - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get chains first
    chains = get_chains(access_token, symbol)
    if not chains:
        return None
    
    chain_id = chains[0].get('id')
    if not chain_id:
        return None
    
    params = {
        'chain_id': chain_id,
        'expiration_dates': expiration_date,
        'strike_price': str(strike),
        'type': option_type
    }
    
    response = _make_request('GET', 'https://robinhood.com/options/instruments/', 
                           headers=headers, params=params)
    
    if response and 'results' in response and response['results']:
        option_data = response['results'][0]
        if info and info in option_data:
            return option_data[info]
        return option_data
    return None

def get_option_instrument_data_by_id(access_token: str, option_id: str, info: Optional[str] = None) -> Optional[Dict]:
    """Get option instrument data by ID - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', f'https://robinhood.com/options/instruments/{option_id}/', headers=headers)
    
    if info and response and info in response:
        return response[info]
    return response

def get_option_market_data(access_token: str, option_ids: Union[str, List[str]], info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get option market data - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    if isinstance(option_ids, str):
        option_ids = [option_ids]
    
    ids_str = ','.join(option_ids)
    response = _make_request('GET', f'https://robinhood.com/marketdata/options/?instruments={ids_str}', 
                           headers=headers)
    
    if response and 'results' in response:
        market_data = response['results']
        if info:
            return [data.get(info) for data in market_data if info in data]
        return market_data
    return []

def get_option_market_data_by_id(access_token: str, option_id: str, info: Optional[str] = None) -> Optional[Dict]:
    """Get option market data by ID - STATELESS VERSION"""
    market_data = get_option_market_data(access_token, [option_id], info)
    return market_data[0] if market_data else None

def find_tradable_options(access_token: str, symbol: str, expiration_date: Optional[str] = None, 
                         strike: Optional[float] = None, option_type: Optional[str] = None, 
                         info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Find tradable options with filters - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    chains = get_chains(access_token, symbol)
    if not chains:
        return []
    
    chain_id = chains[0].get('id')
    if not chain_id:
        return []
    
    params = {'chain_id': chain_id, 'tradeable': 'true'}
    
    if expiration_date:
        params['expiration_dates'] = expiration_date
    if strike:
        params['strike_price'] = str(strike)
    if option_type:
        params['type'] = option_type
    
    response = _make_request('GET', 'https://robinhood.com/options/instruments/', 
                           headers=headers, params=params)
    
    if response and 'results' in response:
        options = response['results']
        if info:
            return [opt.get(info) for opt in options if info in opt]
        return options
    return []

def find_options_by_expiration(access_token: str, symbol: str, expiration_date: str, 
                              option_type: Optional[str] = None, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Find options by expiration date - STATELESS VERSION"""
    return find_tradable_options(access_token, symbol, expiration_date=expiration_date, 
                                option_type=option_type, info=info)

def find_options_by_strike(access_token: str, symbol: str, strike: float, 
                          option_type: Optional[str] = None, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Find options by strike price - STATELESS VERSION"""
    return find_tradable_options(access_token, symbol, strike=strike, 
                                option_type=option_type, info=info)

def find_options_by_expiration_and_strike(access_token: str, symbol: str, expiration_date: str, strike: float,
                                         option_type: Optional[str] = None, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Find options by expiration and strike - STATELESS VERSION"""
    return find_tradable_options(access_token, symbol, expiration_date=expiration_date, 
                                strike=strike, option_type=option_type, info=info)

def find_options_by_specific_profitability(access_token: str, symbol: str, profit_threshold: float = 0.1,
                                          info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Find options by profitability - STATELESS VERSION"""
    # This is a more complex calculation that would need current prices
    # For now, return all tradable options
    return find_tradable_options(access_token, symbol, info=info)
