"""STATELESS export functions - NO GLOBAL STATE"""

from typing import Dict, List, Any, Optional
from .helper import _make_request

# STATELESS REPLACEMENTS for all export functions - NO MORE BLOCKING!

def export_completed_stock_orders(access_token: str) -> List[Dict[str, Any]]:
    """Exports all completed stock orders - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    all_orders = []
    url = 'https://robinhood.com/orders/'
    
    while url:
        response = _make_request('GET', url, headers=headers)
        if not response:
            break
            
        if 'results' in response:
            # Filter for completed orders only
            completed_orders = [order for order in response['results'] 
                              if order.get('state') in ['filled', 'confirmed']]
            all_orders.extend(completed_orders)
            
        url = response.get('next')
    
    return all_orders

def export_completed_option_orders(access_token: str) -> List[Dict[str, Any]]:
    """Exports all completed option orders - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    all_orders = []
    url = 'https://robinhood.com/options/orders/'
    
    while url:
        response = _make_request('GET', url, headers=headers)
        if not response:
            break
            
        if 'results' in response:
            # Filter for completed orders only
            completed_orders = [order for order in response['results'] 
                              if order.get('state') in ['filled', 'confirmed']]
            all_orders.extend(completed_orders)
            
        url = response.get('next')
    
    return all_orders

def export_completed_crypto_orders(access_token: str) -> List[Dict[str, Any]]:
    """Exports all completed crypto orders - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    
    all_orders = []
    url = 'https://nummus.robinhood.com/orders/'
    
    while url:
        response = _make_request('GET', url, headers=headers)
        if not response:
            break
            
        if 'results' in response:
            # Filter for completed orders only
            completed_orders = [order for order in response['results'] 
                              if order.get('state') in ['filled', 'confirmed']]
            all_orders.extend(completed_orders)
            
        url = response.get('next')
    
    return all_orders