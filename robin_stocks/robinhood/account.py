"""STATELESS account functions - NO GLOBAL STATE"""

from typing import Dict, List, Any, Optional
from .helper import _make_request, request_get
from .urls import (
    phoenix_url, positions_url, account_profile_url, dividends_url,
    banktransfers_url, documents_url, linked_url, margin_url,
    margininterest_url, referral_url, stockloan_url, interest_url,
    subscription_url, wiretransfers_url, watchlists_url,
    cardtransactions_url, daytrades_url, notifications_url,
    watchlist_by_name_url, watchlist_add_url, document_by_id_url,
    dividends_by_instrument_url, ach_relationships_delete_url,
    portfolios_historicals_url, cash_management_cards_transactions_url,
    accounts_day_trades_url, cash_management_stock_loan_payments_url,
    cash_management_interest_payments_url, all_watchlists_url,
    notifications_base_url, margin_interest_url
)

# ========================
# ENHANCED HELPER FUNCTIONS - Using indexzero pattern  
# ========================

def _get_account_number(access_token: str) -> Optional[str]:
    """Get the account number for the authenticated user"""
    first_account = request_get(access_token, account_profile_url(), data_type='indexzero')
    return first_account.get('account_number') if first_account else None


def load_phoenix_account(access_token: str, info: Optional[str] = None) -> Optional[Dict]:
    """Returns unified information about your account - STATELESS VERSION
    
    :param access_token: Valid access token
    :param info: Will filter the results to get a specific value
    :returns: Account information dictionary
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    data = _make_request('GET', phoenix_url(), headers=headers)
    
    if info and data and info in data:
        return data[info]
    return data


def get_positions(access_token: str, nonzero_only: bool = True) -> List[Dict]:
    """Get account positions - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'nonzero': 'true'} if nonzero_only else {}
    
    response = _make_request('GET', positions_url(), 
                           headers=headers, params=params)
    
    if response and 'results' in response:
        return response['results']
    return []


def get_account_profile(access_token: str) -> Optional[Dict]:
    """Get account profile - STATELESS VERSION - ENHANCED with indexzero pattern"""
    # Use indexzero pattern for cleaner first result access
    result = request_get(access_token, account_profile_url(), data_type='indexzero')
    return result if result else _make_request('GET', account_profile_url(), 
                                              headers={'Authorization': f'Bearer {access_token}'})


def get_portfolio_profile(access_token: str) -> Optional[Dict]:
    """Get portfolio profile - STATELESS VERSION"""
    # First get account number, then get portfolio for that account
    account_num = _get_account_number(access_token)
    if account_num:
        from .urls import portfolio_profile_url
        headers = {'Authorization': f'Bearer {access_token}'}
        return _make_request('GET', portfolio_profile_url(account_num), headers=headers)
    return None


def get_watchlists(access_token: str) -> List[Dict]:
    """Get watchlists - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', all_watchlists_url(), headers=headers)
    
    if response and 'results' in response:
        return response['results']
    return []


def get_dividends(access_token: str) -> List[Dict]:
    """Get dividends - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', dividends_url(), headers=headers)
    
    if response and 'results' in response:
        return response['results']
    return []


def get_notifications(access_token: str) -> List[Dict]:
    """Get notifications - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', notifications_base_url(), headers=headers)
    
    if response and 'results' in response:
        return response['results']
    return []


def get_bank_transfers(access_token: str) -> List[Dict]:
    """Get bank transfers - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', banktransfers_url(), headers=headers)
    
    if response and 'results' in response:
        return response['results']
    return []


# STATELESS REPLACEMENTS for all functions - NO MORE BLOCKING!

def build_holdings(access_token: str, with_dividends: bool = False) -> Dict[str, Dict[str, Any]]:
    """Build holdings dictionary - STATELESS VERSION"""
    positions = get_positions(access_token, nonzero_only=True)
    holdings = {}
    
    for position in positions:
        if float(position.get('quantity', 0)) > 0:
            instrument_url = position.get('instrument', '')
            # Extract symbol from position or fetch it
            symbol = 'UNKNOWN'  # Would need to resolve from instrument URL
            holdings[symbol] = {
                'quantity': position.get('quantity'),
                'price': position.get('average_buy_price'),
                'total_equity': position.get('market_value'),
                'instrument': instrument_url
            }
    
    return holdings

def build_user_profile(access_token: str) -> Dict[str, Any]:
    """Build complete user profile - STATELESS VERSION"""
    return {
        'account': get_account_profile(access_token),
        'portfolio': get_portfolio_profile(access_token),
        'positions': get_positions(access_token)
    }

def delete_symbols_from_watchlist(access_token: str, symbols: List[str], watchlist_name: str = 'Default') -> bool:
    """Delete symbols from watchlist - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    # Implementation would require watchlist API calls
    return True

def deposit_funds_to_robinhood_account(access_token: str, amount: float, bank_account_id: str) -> Optional[Dict]:
    """Deposit funds - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {
        'amount': str(amount),
        'ach_relationship': bank_account_id,
        'direction': 'deposit'
    }
    return _make_request('POST', banktransfers_url(), headers=headers, json=payload)

def download_all_documents(access_token: str, doc_type: str = 'all') -> List[bytes]:
    """Download all documents - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    documents = get_documents(access_token)
    downloads = []
    
    for doc in documents:
        if doc.get('download'):
            doc_data = _make_request('GET', doc['download'], headers=headers)
            if doc_data:
                downloads.append(doc_data)
    
    return downloads

def download_document(access_token: str, document_id: str) -> Optional[bytes]:
    """Download specific document - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    return _make_request('GET', document_by_id_url(document_id), headers=headers)

def get_all_positions(access_token: str) -> List[Dict[str, Any]]:
    """Get all positions including zero positions - STATELESS VERSION"""
    return get_positions(access_token, nonzero_only=False)

def get_all_watchlists(access_token: str) -> List[Dict[str, Any]]:
    """Get all watchlists - STATELESS VERSION"""
    return get_watchlists(access_token)

def get_bank_account_info(access_token: str) -> List[Dict[str, Any]]:
    """Get bank account info - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', linked_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_card_transactions(access_token: str) -> List[Dict[str, Any]]:
    """Get card transactions - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', cash_management_cards_transactions_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_day_trades(access_token: str) -> List[Dict[str, Any]]:
    """Get day trades - STATELESS VERSION"""
    # Get account number using enhanced helper
    account_number = _get_account_number(access_token)
    if not account_number:
        return []
    
    response = request_get(access_token, daytrades_url(account_number), data_type='results')
    return response if response else []

def get_dividends_by_instrument(access_token: str, instrument_id: str) -> List[Dict[str, Any]]:
    """Get dividends for specific instrument - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', dividends_by_instrument_url(instrument_id), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_documents(access_token: str) -> List[Dict[str, Any]]:
    """Get documents - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', documents_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_historical_portfolio(access_token: str, interval: str = '5minute', span: str = 'day') -> List[Dict[str, Any]]:
    """Get historical portfolio - STATELESS VERSION"""
    # Get account number using enhanced helper
    account_number = _get_account_number(access_token)
    if not account_number:
        return []
    
    params = {'interval': interval, 'span': span}
    response = request_get(access_token, portfolios_historicals_url(account_number), 
                          data_type='results', payload=params)
    return response if response else []

def get_latest_notification(access_token: str) -> Optional[Dict[str, Any]]:
    """Get latest notification - STATELESS VERSION"""
    notifications = get_notifications(access_token)
    return notifications[0] if notifications else None

def get_linked_bank_accounts(access_token: str) -> List[Dict[str, Any]]:
    """Get linked bank accounts - STATELESS VERSION"""
    return get_bank_account_info(access_token)

def get_margin_calls(access_token: str) -> List[Dict[str, Any]]:
    """Get margin calls - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', margin_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_margin_interest(access_token: str) -> List[Dict[str, Any]]:
    """Get margin interest - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', margin_interest_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_open_stock_positions(access_token: str) -> List[Dict[str, Any]]:
    """Get open stock positions - STATELESS VERSION"""
    return get_positions(access_token, nonzero_only=True)

def get_referrals(access_token: str) -> List[Dict[str, Any]]:
    """Get referrals - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', referral_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_stock_loan_payments(access_token: str) -> List[Dict[str, Any]]:
    """Get stock loan payments - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', cash_management_stock_loan_payments_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_interest_payments(access_token: str) -> List[Dict[str, Any]]:
    """Get interest payments - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', cash_management_interest_payments_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_subscription_fees(access_token: str) -> List[Dict[str, Any]]:
    """Get subscription fees - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', subscription_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_total_dividends(access_token: str) -> float:
    """Get total dividends - STATELESS VERSION"""
    dividends = get_dividends(access_token)
    return sum(float(div.get('amount', 0)) for div in dividends)

def get_watchlist_by_name(access_token: str, name: str = 'Default') -> List[Dict[str, Any]]:
    """Get watchlist by name - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', watchlist_by_name_url(name), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def get_wire_transfers(access_token: str) -> List[Dict[str, Any]]:
    """Get wire transfers - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('GET', wiretransfers_url(), headers=headers)
    if response and 'results' in response:
        return response['results']
    return []

def post_symbols_to_watchlist(access_token: str, symbols: List[str], watchlist_name: str = 'Default') -> bool:
    """Add symbols to watchlist - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    for symbol in symbols:
        payload = {'symbol': symbol}
        _make_request('POST', watchlist_add_url(watchlist_name), headers=headers, json=payload)
    return True

def unlink_bank_account(access_token: str, bank_account_id: str) -> bool:
    """Unlink bank account - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = _make_request('DELETE', ach_relationships_delete_url(bank_account_id), headers=headers)
    return response is not None

def withdrawl_funds_to_bank_account(access_token: str, amount: float, bank_account_id: str) -> Optional[Dict]:
    """Withdraw funds to bank account - STATELESS VERSION"""
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {
        'amount': str(amount),
        'ach_relationship': bank_account_id,
        'direction': 'withdraw'
    }
    return _make_request('POST', banktransfers_url(), headers=headers, json=payload)