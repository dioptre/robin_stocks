"""
PURE STATELESS ROBINHOOD API CORE

NO STATE. NO FILES. NO PICKLES. NO BULLSHIT.

This module contains ONLY core infrastructure:
- Authentication (login_and_get_token)
- HTTP request wrapper (_make_request)

All domain-specific functions belong in their proper modules:
- stocks.py for stock data
- orders.py for order management  
- account.py for account data
- etc.
"""

from typing import Dict, List, Any, Optional, Union
import secrets
import time
from .helper import _make_request


def _generate_device_token() -> str:
    """Generate a one-time device token"""
    rands = [secrets.randbelow(256) for _ in range(16)]
    hexa = [str(hex(i + 256)).lstrip("0x")[1:] for i in range(256)]
    token = ""
    for i, r in enumerate(rands):
        token += hexa[r]
        if i in [3, 5, 7, 9]:
            token += "-"
    return token


def login_and_get_token(username: str, password: str, mfa_code: Optional[str] = None) -> Optional[str]:
    """
    Pure login function - returns ONLY the access token, nothing else.
    No state, no sessions, no files, no bullshit.
    """
    device_token = _generate_device_token()
    
    payload = {
        'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
        'expires_in': 86400,
        'grant_type': 'password',
        'password': password,
        'scope': 'internal',
        'username': username,
        'challenge_type': 'sms',
        'device_token': device_token
    }
    
    if mfa_code:
        payload['mfa_code'] = mfa_code
    
    response = _make_request('POST', 'https://robinhood.com/api-token-auth/', json=payload)
    
    if response and 'access_token' in response:
        return response['access_token']
    
    # Handle MFA challenge if needed
    if response and 'mfa_required' in response and not mfa_code:
        print("MFA required. Please call login_and_get_token() again with mfa_code parameter.")
        return None
    
    print(f"Login failed: {response}")
    return None