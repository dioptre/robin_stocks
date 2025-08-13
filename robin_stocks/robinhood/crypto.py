"""STATELESS crypto functions - NO GLOBAL STATE"""

from typing import Dict, List, Any, Optional, Union
from .helper import _make_request, request_get
from .urls import (
    crypto_account_url, crypto_holdings_url, crypto_quote_url,
    crypto_currency_pairs_url, crypto_historical_url, crypto_currency_url
)

# STATELESS REPLACEMENTS for all crypto functions - NO MORE BLOCKING!

def load_crypto_profile(access_token: str, info: Optional[str] = None) -> Optional[Dict]:
    """Gets the information associated with the crypto account - STATELESS VERSION"""
    # Use indexzero pattern for cleaner first result access
    response = request_get(access_token, crypto_account_url(), data_type='indexzero')
    
    if info and response and info in response:
        return response[info]
    return response

def get_crypto_positions(access_token: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns crypto positions for the account - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', crypto_holdings_url(), headers=headers)
    
    if response and 'results' in response:
        positions = response['results']
        if info:
            return [pos.get(info) for pos in positions if info in pos]
        return positions
    return []

def get_crypto_quote(access_token: str, symbol: str, info: Optional[str] = None) -> Optional[Dict]:
    """Get crypto quote by symbol - STATELESS VERSION"""
    # First, get the currency pair ID for this symbol
    pairs = get_crypto_currency_pairs(access_token)
    pair_id = None
    
    for pair in pairs:
        if pair.get('asset_currency', {}).get('code') == symbol.upper():
            pair_id = pair.get('id')
            break
    
    if not pair_id:
        return None
        
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', crypto_quote_url(pair_id), headers=headers)
    
    if info and response and info in response:
        return response[info]
    return response

def get_crypto_quote_from_id(access_token: str, crypto_id: str, info: Optional[str] = None) -> Optional[Dict]:
    """Get crypto quote by ID - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', crypto_quote_url(crypto_id), headers=headers)
    
    if info and response and info in response:
        return response[info]
    return response

def get_crypto_currency_pairs(access_token: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get crypto currency pairs - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', crypto_currency_pairs_url(), headers=headers)
    
    if response and 'results' in response:
        pairs = response['results']
        if info:
            return [pair.get(info) for pair in pairs if info in pair]
        return pairs
    return []

def get_crypto_historicals(access_token: str, symbol: str, interval: str = '5minute', 
                          span: str = 'day', bounds: str = '24_7', info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get crypto historical data - STATELESS VERSION"""
    # First, get the currency pair ID for this symbol
    pairs = get_crypto_currency_pairs(access_token)
    pair_id = None
    
    for pair in pairs:
        if pair.get('asset_currency', {}).get('code') == symbol.upper():
            pair_id = pair.get('id')
            break
    
    if not pair_id:
        return []
        
    headers = {'Authorization': f'Bearer {access_token}'}
    
    params = {
        'interval': interval,
        'span': span,
        'bounds': bounds
    }
    
    response = _make_request('GET', crypto_historical_url(pair_id), 
                           headers=headers, params=params)
    
    if response and 'data_points' in response:
        data = response['data_points']
        if info:
            return [point.get(info) for point in data if info in point]
        return data
    return []

def get_crypto_info(access_token: str, symbol: str, info: Optional[str] = None) -> Optional[Dict]:
    """Get crypto currency info - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', crypto_currency_url(symbol), headers=headers)
    
    if info and response and info in response:
        return response[info]
    return response
