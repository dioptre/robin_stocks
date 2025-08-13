"""STATELESS helper functions - NO GLOBAL STATE

This module contains useful utility functions that have been converted to stateless versions.

NO STATE. NO SESSIONS. NO FILES. NO PICKLES. NO BULLSHIT.
"""
import requests
from requests import Session
from typing import Dict, List, Any, Optional, Union
from .urls import instruments_url, option_chains_by_id_url, option_instruments_url


def _make_request(method: str, url: str, headers: Dict[str, str] = None, 
                  data: Dict = None, json: Dict = None, params: Dict = None, 
                  timeout: int = 16) -> Optional[Dict]:
    """Pure HTTP request function - no state"""
    try:
        session = Session()
        if headers:
            session.headers.update(headers)
        
        if method.upper() == 'GET':
            response = session.get(url, params=params, timeout=timeout)
        elif method.upper() == 'POST':
            if json:
                response = session.post(url, json=json, timeout=timeout)
            else:
                response = session.post(url, data=data, timeout=timeout)
        elif method.upper() == 'DELETE':
            response = session.delete(url, timeout=timeout)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# STATELESS UTILITY FUNCTIONS - These are safe and useful!

def id_for_stock(access_token: str, symbol: str) -> Optional[str]:
    """Takes a stock ticker and returns the instrument id - STATELESS VERSION
    
    :param access_token: The access token for authentication
    :type access_token: str
    :param symbol: The symbol to get the id for
    :type symbol: str
    :returns: A string that represents the stocks instrument id
    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError:
        return None

    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'symbol': symbol}
    response = _make_request('GET', instruments_url(), 
                           headers=headers, params=params)
    
    if response and 'results' in response and response['results']:
        return response['results'][0].get('id')
    return None

def id_for_chain(access_token: str, symbol: str) -> Optional[str]:
    """Takes a stock ticker and returns the chain id for options - STATELESS VERSION
    
    :param access_token: The access token for authentication
    :type access_token: str
    :param symbol: The symbol to get the chain id for
    :type symbol: str
    :returns: A string that represents the stocks options chain id
    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError:
        return None

    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'symbol': symbol}
    response = _make_request('GET', instruments_url(), 
                           headers=headers, params=params)
    
    if response and 'results' in response and response['results']:
        return response['results'][0].get('tradable_chain_id')
    return None

def id_for_group(access_token: str, symbol: str) -> Optional[str]:
    """Takes a stock ticker and returns the group id - STATELESS VERSION
    
    :param access_token: The access token for authentication
    :type access_token: str
    :param symbol: The symbol to get the group id for
    :type symbol: str
    :returns: A string that represents the stocks group id
    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError:
        return None

    chain_id = id_for_chain(access_token, symbol)
    if not chain_id:
        return None
    
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', option_chains_by_id_url(chain_id), 
                           headers=headers)
    
    if response and 'underlying_instruments' in response and response['underlying_instruments']:
        return response['underlying_instruments'][0].get('id')
    return None

def id_for_option(access_token: str, symbol: str, expiration_date: str, strike: float, option_type: str) -> Optional[str]:
    """Returns the id for a specific option - STATELESS VERSION
    
    :param access_token: The access token for authentication
    :type access_token: str
    :param symbol: The symbol to get the option id for
    :type symbol: str
    :param expiration_date: The expiration date as YYYY-MM-DD
    :type expiration_date: str
    :param strike: The strike price
    :type strike: float
    :param option_type: Either 'call' or 'put'
    :type option_type: str
    :returns: A string that represents the option id
    """
    symbol = symbol.upper()
    chain_id = id_for_chain(access_token, symbol)
    if not chain_id:
        return None
    
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'chain_id': chain_id,
        'expiration_dates': expiration_date,
        'strike_price': str(strike),
        'type': option_type.lower(),
        'state': 'active'
    }
    
    response = _make_request('GET', option_instruments_url(), 
                           headers=headers, params=params)
    
    if response and 'results' in response:
        # Filter for exact expiration date match
        matching_options = [item for item in response['results'] 
                          if item.get("expiration_date") == expiration_date]
        if matching_options:
            return matching_options[0]['id']
    
    return None

# PURE UTILITY FUNCTIONS - No API calls, no state, just pure logic

def round_price(price: Union[float, int]) -> float:
    """Takes a price and rounds it to appropriate decimal place for Robinhood - STATELESS VERSION
    
    :param price: The input price to round
    :type price: float or int
    :returns: The rounded price as a float
    """
    price = float(price)
    if price <= 1e-2:
        return round(price, 6)
    elif price < 1e0:
        return round(price, 4)
    else:
        return round(price, 2)

def filter_data(data: Union[Dict, List, None], info: Optional[str]) -> Any:
    """Takes data and extracts value for keyword that matches info - STATELESS VERSION
    
    :param data: The data to filter
    :type data: dict or list or None
    :param info: The keyword to filter from the data
    :type info: str or None
    :returns: A list or string with values that correspond to the info keyword
    """
    if data is None:
        return data
    elif data == [None]:
        return []
    elif isinstance(data, list):
        if len(data) == 0:
            return []
        compare_dict = data[0]
        none_type = []
    elif isinstance(data, dict):
        compare_dict = data
        none_type = None
    else:
        return data

    if info is not None:
        if info in compare_dict and isinstance(data, list):
            return [x.get(info) for x in data if info in x]
        elif info in compare_dict and isinstance(data, dict):
            return data[info]
        else:
            return none_type
    else:
        return data

def inputs_to_set(input_symbols: Union[str, List, tuple, set]) -> List[str]:
    """Takes input parameters and puts them in a clean list - STATELESS VERSION
    
    :param input_symbols: A list, dict, tuple, or string of stock tickers
    :type input_symbols: list or dict or tuple or str
    :returns: A list of strings that have been capitalized and stripped
    """
    symbols_list = []
    symbols_set = set()

    def add_symbol(symbol):
        if isinstance(symbol, str):
            symbol = symbol.upper().strip()
            if symbol not in symbols_set:
                symbols_set.add(symbol)
                symbols_list.append(symbol)

    if isinstance(input_symbols, str):
        add_symbol(input_symbols)
    elif isinstance(input_symbols, (list, tuple, set)):
        for item in input_symbols:
            add_symbol(item)

    return symbols_list

# STATELESS REQUEST FUNCTIONS - These are the safe replacements for the old stateful versions

def request_document(access_token: str, url: str, payload: Optional[Dict] = None):
    """Makes a GET request and returns the JSON response - STATELESS VERSION
    
    :param access_token: The access token for authentication
    :type access_token: str
    :param url: The url to send a get request to
    :type url: str
    :param payload: Optional parameters to pass to the url
    :type payload: Optional[dict]
    :returns: Returns the JSON response data
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    return _make_request('GET', url, headers=headers, params=payload)

def request_get(access_token: str, url: str, data_type: str = 'regular', payload: Optional[Dict] = None, jsonify_data: bool = True):
    """Makes a GET request with various data filtering options - STATELESS VERSION
    
    :param access_token: The access token for authentication
    :type access_token: str
    :param url: The url to send a get request to
    :type url: str
    :param data_type: How to filter data ('regular', 'results', 'pagination', 'indexzero')
    :type data_type: str
    :param payload: Optional parameters to pass to the url
    :type payload: Optional[dict]
    :param jsonify_data: Whether to return JSON data (always True in stateless version)
    :type jsonify_data: bool
    :returns: Filtered data based on data_type parameter
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', url, headers=headers, params=payload)
    
    if not response:
        return [None] if data_type in ['results', 'pagination'] else None
    
    # Filter data based on data_type
    if data_type == 'results':
        return response.get('results', [None])
    elif data_type == 'pagination':
        # Handle pagination by following 'next' links
        all_results = response.get('results', [])
        next_url = response.get('next')
        
        while next_url:
            next_response = _make_request('GET', next_url, headers=headers)
            if next_response and 'results' in next_response:
                all_results.extend(next_response['results'])
                next_url = next_response.get('next')
            else:
                break
        
        return all_results
    elif data_type == 'indexzero':
        results = response.get('results', [])
        return results[0] if results else None
    else:  # data_type == 'regular'
        return response

def request_post(access_token: str, url: str, payload: Optional[Dict] = None, timeout: int = 16, 
                json_data: bool = False, jsonify_data: bool = True):
    """Makes a POST request - STATELESS VERSION
    
    :param access_token: The access token for authentication
    :type access_token: str
    :param url: The url to send a post request to
    :type url: str
    :param payload: Dictionary of parameters to send
    :type payload: Optional[dict]
    :param timeout: Request timeout in seconds
    :type timeout: int
    :param json_data: Whether to send payload as JSON
    :type json_data: bool
    :param jsonify_data: Whether to return JSON data (always True in stateless version)
    :type jsonify_data: bool
    :returns: Response data
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    
    if json_data:
        headers['Content-Type'] = 'application/json'
        return _make_request('POST', url, headers=headers, json=payload, timeout=timeout)
    else:
        return _make_request('POST', url, headers=headers, data=payload, timeout=timeout)

def request_delete(access_token: str, url: str):
    """Makes a DELETE request - STATELESS VERSION
    
    :param access_token: The access token for authentication
    :type access_token: str
    :param url: The url to send a delete request to
    :type url: str
    :returns: Response data
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    return _make_request('DELETE', url, headers=headers)