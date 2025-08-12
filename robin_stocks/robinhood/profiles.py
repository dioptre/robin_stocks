"""STATELESS profiles functions - NO GLOBAL STATE"""

from typing import Dict, List, Any, Optional
from .helper import _make_request

# STATELESS REPLACEMENTS for all profile functions - NO MORE BLOCKING!

def load_account_profile(access_token: str, account_number: Optional[str] = None, info: Optional[str] = None) -> Optional[Dict]:
    """Gets the information associated with the accounts profile - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    if account_number:
        url = f'https://robinhood.com/accounts/{account_number}/'
        response = _make_request('GET', url, headers=headers)
    else:
        response = _make_request('GET', 'https://robinhood.com/accounts/', headers=headers)
        if response and 'results' in response and response['results']:
            response = response['results'][0]
    
    if info and response and info in response:
        return response[info]
    return response

def load_basic_profile(access_token: str, info: Optional[str] = None) -> Optional[Dict]:
    """Gets the information associated with the personal profile - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', 'https://robinhood.com/user/basic_info/', headers=headers)
    
    if info and response and info in response:
        return response[info]
    return response

def load_investment_profile(access_token: str, info: Optional[str] = None) -> Optional[Dict]:
    """Gets the information associated with the investment profile - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', 'https://robinhood.com/user/investment_profile/', headers=headers)
    
    if info and response and info in response:
        return response[info]
    return response

def load_portfolio_profile(access_token: str, account_number: Optional[str] = None, info: Optional[str] = None) -> Optional[Dict]:
    """Gets the information associated with the portfolios profile - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    if account_number:
        url = f'https://robinhood.com/accounts/{account_number}/portfolio/'
        response = _make_request('GET', url, headers=headers)
    else:
        response = _make_request('GET', 'https://robinhood.com/positions/', headers=headers)
        if response and 'results' in response and response['results']:
            response = response['results'][0]
    
    if info and response and info in response:
        return response[info]
    return response

def load_security_profile(access_token: str, info: Optional[str] = None) -> Optional[Dict]:
    """Gets the information associated with the security profile - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', 'https://robinhood.com/user/additional_info/', headers=headers)
    
    if info and response and info in response:
        return response[info]
    return response

def load_user_profile(access_token: str, info: Optional[str] = None) -> Optional[Dict]:
    """Gets the information associated with the user profile - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', 'https://robinhood.com/user/', headers=headers)
    
    if info and response and info in response:
        return response[info]
    return response
