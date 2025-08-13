"""Stocks functions - all stateless with access_token parameter"""

from typing import Dict, List, Any, Optional, Union
from .helper import _make_request
from .urls import (
    fundamentals_url, events_url, instruments_url, news_url,
    ratings_url, instrument_splits_url, instrument_by_id_url,
    quotes_url, quotes_by_id_url, historicals_url, popularity_url, splits_url
)

def find_instrument_data(access_token: str, symbol: str) -> Optional[Dict]:
    """Find instrument data by symbol"""
    instruments = get_instruments_by_symbols(access_token, [symbol])
    return instruments[0] if instruments else None

def get_earnings(access_token: str, symbol: str) -> List[Dict]:
    """Get earnings data"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = _make_request('GET', fundamentals_url(), params={'symbol': symbol}, 
                           headers=headers)
    
    if response:
        return [response]
    return []

def get_events(access_token: str, symbol: str) -> List[Dict[str, Any]]:
    """Get events for symbol"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', events_url(), params={'symbol': symbol}, headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_fundamentals(access_token: str, symbols: Union[str, List[str]]) -> List[Dict]:
    """Get fundamental data"""
    if isinstance(symbols, str):
        symbols = [symbols]
    
    headers = {'Authorization': f'Bearer {access_token}'}
    symbols_str = ','.join(symbols)
    
    response = _make_request('GET', fundamentals_url(), 
                           headers=headers, params={'symbols': symbols_str})
    
    if response and 'results' in response:
        return response['results']
    return []

def get_instrument_by_url(access_token: str, url: str) -> Optional[Dict]:
    """Get instrument by URL"""
    headers = {'Authorization': f'Bearer {access_token}'}
    return _make_request('GET', url, headers=headers)

def get_instruments_by_symbols(access_token: str, symbols: Union[str, List[str]]) -> List[Dict]:
    """Get instruments by symbols"""
    if isinstance(symbols, str):
        symbols = [symbols]
    
    headers = {'Authorization': f'Bearer {access_token}'}
    symbols_str = ','.join(symbols)
    
    response = _make_request('GET', instruments_url(), 
                           headers=headers, params={'symbols': symbols_str})
    
    if response and 'results' in response:
        return response['results']
    return []

def get_latest_price(access_token: str, symbols: Union[str, List[str]]) -> List[str]:
    """Get latest prices"""
    quotes = get_quotes(access_token, symbols)
    return [quote.get('last_trade_price', '0.00') for quote in quotes]

def get_name_by_symbol(access_token: str, symbol: str) -> Optional[str]:
    """Get company name by symbol"""
    instruments = get_instruments_by_symbols(access_token, [symbol])
    return instruments[0].get('simple_name') if instruments else None

def get_name_by_url(access_token: str, url: str) -> Optional[str]:
    """Get company name by instrument URL"""
    instrument = get_instrument_by_url(access_token, url)
    return instrument.get('simple_name') if instrument else None

def get_news(access_token: str, symbol: str) -> List[Dict]:
    """Get news for symbol"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = _make_request('GET', news_url(symbol), 
                           headers=headers)
    
    if response and 'results' in response:
        return response['results']
    return []

def get_pricebook_by_id(access_token: str, instrument_id: str) -> Optional[Dict]:
    """Get price book by instrument ID"""
    headers = {'Authorization': f'Bearer {access_token}'}
    return _make_request('GET', instrument_by_id_url(instrument_id), headers=headers)

def get_pricebook_by_symbol(access_token: str, symbol: str) -> Optional[Dict]:
    """Get price book by symbol"""
    instruments = get_instruments_by_symbols(access_token, [symbol])
    if instruments:
        instrument_id = instruments[0].get('id')
        return get_pricebook_by_id(access_token, instrument_id)
    return None

def get_quotes(access_token: str, symbols: Union[str, List[str]]) -> List[Dict]:
    """Get stock quotes"""
    if isinstance(symbols, str):
        symbols = [symbols]
    
    headers = {'Authorization': f'Bearer {access_token}'}
    symbols_str = ','.join(symbols)
    
    response = _make_request('GET', quotes_url(), 
                           headers=headers, params={'symbols': symbols_str})
    
    if response and 'results' in response:
        return response['results']
    return []

def get_ratings(access_token: str, symbol: str) -> Dict:
    """Get analyst ratings"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = _make_request('GET', ratings_url(symbol), 
                           headers=headers)
    
    return response or {}

def get_splits(access_token: str, symbol: str) -> List[Dict]:
    """Get stock splits (legacy method using instrument_id lookup)"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # First get instrument
    instrument_response = _make_request('GET', instruments_url(), 
                                      headers=headers, params={'symbol': symbol})
    
    if not instrument_response or not instrument_response.get('results'):
        return []
    
    instrument_id = instrument_response['results'][0]['id']
    
    response = _make_request('GET', instrument_splits_url(instrument_id), 
                           headers=headers)
    
    if response and 'results' in response:
        return response['results']
    return []

def get_stock_historicals(access_token: str, symbols: Union[str, List[str]], 
                         interval: str = 'day', span: str = 'year', bounds: str = 'regular') -> List[Dict]:
    """Get stock historical data"""
    if isinstance(symbols, str):
        symbols = [symbols]
    
    headers = {'Authorization': f'Bearer {access_token}'}
    symbols_str = ','.join(symbols)
    
    params = {
        'symbols': symbols_str,
        'interval': interval,
        'span': span,
        'bounds': bounds
    }
    
    response = _make_request('GET', historicals_url(), 
                           headers=headers, params=params)
    
    if response and 'results' in response:
        return response['results']
    return []

def get_stock_quote_by_id(access_token: str, instrument_id: str) -> Optional[Dict]:
    """Get stock quote by instrument ID"""
    headers = {'Authorization': f'Bearer {access_token}'}
    return _make_request('GET', quotes_by_id_url(instrument_id), headers=headers)

def get_stock_quote_by_symbol(access_token: str, symbol: str) -> Optional[Dict]:
    """Get stock quote by symbol"""
    quotes = get_quotes(access_token, [symbol])
    return quotes[0] if quotes else None

def get_symbol_by_url(access_token: str, url: str) -> Optional[str]:
    """Get symbol by instrument URL"""
    instrument = get_instrument_by_url(access_token, url)
    return instrument.get('symbol') if instrument else None

def get_popularity(access_token: str, symbol: str) -> Optional[Dict]:
    """Get stock popularity data"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = _make_request('GET', popularity_url(symbol), 
                           headers=headers)
    
    return response

def get_splits_by_symbol(access_token: str, symbol: str) -> List[Dict]:
    """Get stock splits data by symbol"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = _make_request('GET', splits_url(symbol), 
                           headers=headers)
    
    if response and 'results' in response:
        return response['results']
    return []