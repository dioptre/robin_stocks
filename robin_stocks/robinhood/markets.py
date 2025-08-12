"""STATELESS markets functions - NO GLOBAL STATE"""

from typing import Dict, List, Any, Optional
from .helper import _make_request

# STATELESS REPLACEMENTS for all market functions - NO MORE BLOCKING!

def get_top_movers_sp500(access_token: str, direction: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns a list of the top S&P500 movers up or down for the day - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    direction = direction.lower().strip()
    if direction not in ['up', 'down']:
        raise ValueError("direction must be 'up' or 'down'")
    
    params = {'direction': direction}
    response = _make_request('GET', 'https://robinhood.com/midlands/movers/sp500/', 
                           headers=headers, params=params)
    
    if response and 'results' in response:
        movers = response['results']
        if info:
            return [mover.get(info) for mover in movers if info in mover]
        return movers
    return []

def get_top_100(access_token: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns a list of the Top 100 stocks on Robinhood - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', 'https://robinhood.com/midlands/tags/tag/100-most-popular/', headers=headers)
    
    if response and 'results' in response:
        stocks = response['results']
        if info:
            return [stock.get(info) for stock in stocks if info in stock]
        return stocks
    return []

def get_top_movers(access_token: str, direction: str = 'up', info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get top movers - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    direction = direction.lower().strip()
    if direction not in ['up', 'down']:
        raise ValueError("direction must be 'up' or 'down'")
    
    params = {'direction': direction}
    response = _make_request('GET', 'https://robinhood.com/midlands/movers/sp500/', 
                           headers=headers, params=params)
    
    if response and 'results' in response:
        movers = response['results']
        if info:
            return [mover.get(info) for mover in movers if info in mover]
        return movers
    return []

def get_markets(access_token: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get market data - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', 'https://robinhood.com/markets/', headers=headers)
    
    if response and 'results' in response:
        markets = response['results']
        if info:
            return [market.get(info) for market in markets if info in market]
        return markets
    return []

def get_market_hours(access_token: str, market: str, date: str, info: Optional[str] = None) -> Optional[Dict]:
    """Get market hours - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', f'https://robinhood.com/markets/{market}/hours/{date}/', headers=headers)
    
    if info and response and info in response:
        return response[info]
    return response

def get_market_today_hours(access_token: str, market: str = 'XNAS', info: Optional[str] = None) -> Optional[Dict]:
    """Get market hours for today - STATELESS VERSION"""
    from datetime import date
    today = date.today().isoformat()
    return get_market_hours(access_token, market, today, info)

def get_market_next_open_hours(access_token: str, market: str = 'XNAS', info: Optional[str] = None) -> Optional[Dict]:
    """Get next market open hours - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', f'https://robinhood.com/markets/{market}/', headers=headers)
    
    if response and 'todays_hours' in response:
        next_open = response['todays_hours']
        if info and info in next_open:
            return next_open[info]
        return next_open
    return None

def get_market_next_open_hours_after_date(access_token: str, date_str: str, market: str = 'XNAS', info: Optional[str] = None) -> Optional[Dict]:
    """Get next market open hours after specific date - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'date': date_str}
    response = _make_request('GET', f'https://robinhood.com/markets/{market}/hours/', 
                           headers=headers, params=params)
    
    if response and 'results' in response and response['results']:
        next_open = response['results'][0]
        if info and info in next_open:
            return next_open[info]
        return next_open
    return None

def get_currency_pairs(access_token: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get currency pairs - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', 'https://nummus.robinhood.com/currency_pairs/', headers=headers)
    
    if response and 'results' in response:
        pairs = response['results']
        if info:
            return [pair.get(info) for pair in pairs if info in pair]
        return pairs
    return []

def get_all_stocks_from_market_tag(access_token: str, tag: str, info: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all stocks from market tag - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', f'https://robinhood.com/midlands/tags/tag/{tag}/', headers=headers)
    
    if response and 'results' in response:
        stocks = response['results']
        if info:
            return [stock.get(info) for stock in stocks if info in stock]
        return stocks
    return []
