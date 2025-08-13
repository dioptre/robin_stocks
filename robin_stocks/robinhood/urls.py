"""STATELESS URL builders - NO GLOBAL STATE

Contains all the URL endpoints for interacting with Robinhood API.
These are pure functions that build URLs without any stateful dependencies.
"""

# Login
def login_url():
    return 'https://api.robinhood.com/oauth2/token/'

def challenge_url(challenge_id):
    return f'https://api.robinhood.com/challenge/{challenge_id}/respond/'

# Profiles
def account_profile_url(account_number=None):
    if account_number:
        return f'https://api.robinhood.com/accounts/{account_number}/'
    else:
        return 'https://api.robinhood.com/accounts/'

def basic_profile_url():
    return 'https://api.robinhood.com/user/basic_info/'

def investment_profile_url():
    return 'https://api.robinhood.com/user/investment_profile/'

def portfolio_profile_url(account_number=None):
    if account_number:
        return f'https://api.robinhood.com/accounts/{account_number}/portfolio/'
    else:
        return 'https://api.robinhood.com/accounts/'

def security_profile_url():
    return 'https://api.robinhood.com/user/additional_info/'

def user_profile_url():
    return 'https://api.robinhood.com/user/'

def portfolios_historicals_url(account_number):
    return f'https://api.robinhood.com/accounts/{account_number}/portfolio/historicals/'

# Stocks
def earnings_url():
    return 'https://api.robinhood.com/marketdata/earnings/'

def events_url():
    return 'https://api.robinhood.com/options/events/'

def fundamentals_url():
    return 'https://api.robinhood.com/fundamentals/'

def historicals_url():
    return 'https://api.robinhood.com/quotes/historicals/'

def instruments_url():
    return 'https://api.robinhood.com/instruments/'

def news_url(symbol):
    return f'https://api.robinhood.com/midlands/news/{symbol}/'

def ratings_url(symbol):
    return f'https://api.robinhood.com/midlands/ratings/{symbol}/'

def instrument_splits_url(instrument_id):
    return f'https://api.robinhood.com/instruments/{instrument_id}/splits/'

def instrument_by_id_url(instrument_id):
    return f'https://api.robinhood.com/instruments/{instrument_id}/'

def quotes_url():
    return 'https://api.robinhood.com/quotes/'

def quotes_by_id_url(instrument_id):
    return f'https://api.robinhood.com/quotes/?ids={instrument_id}'

def popularity_url(symbol):
    return f'https://api.robinhood.com/instruments/{symbol}/popularity/'

def chains_url(symbol):
    return f'https://api.robinhood.com/options/chains/?equity_instrument_ids={symbol}'

def splits_url(symbol):
    return f'https://api.robinhood.com/instruments/{symbol}/splits/'

# Account
def phoenix_url():
    return 'https://phoenix.robinhood.com/accounts/unified'

def positions_url(account_number=None):
    if account_number:
        return f'https://api.robinhood.com/positions/?account_number={account_number}'
    else:
        return 'https://api.robinhood.com/positions/'

def banktransfers_url(direction=None):
    if direction == 'received':
        return 'https://api.robinhood.com/ach/received/transfers/'
    else:
        return 'https://api.robinhood.com/ach/transfers/'

def cardtransactions_url():
    return 'https://minerva.robinhood.com/history/transactions/'

def unifiedtransfers_url():
    return 'https://bonfire.robinhood.com/paymenthub/unified_transfers/'

def daytrades_url(account):
    return f'https://api.robinhood.com/accounts/{account}/recent_day_trades/'

def dividends_url():
    return 'https://api.robinhood.com/dividends/'

def documents_url():
    return 'https://api.robinhood.com/documents/'

def withdrawal_url(bank_id):
    return f'https://api.robinhood.com/ach/relationships/{bank_id}/'

def linked_url(id=None, unlink=False):
    if unlink:
        return f'https://api.robinhood.com/ach/relationships/{id}/unlink/'
    if id:
        return f'https://api.robinhood.com/ach/relationships/{id}/'
    else:
        return 'https://api.robinhood.com/ach/relationships/'

def margin_url():
    return 'https://api.robinhood.com/margin/calls/'

def margininterest_url():
    return 'https://api.robinhood.com/cash_journal/margin_interest_charges/'

def notifications_url(tracker=False):
    if tracker:
        return 'https://api.robinhood.com/midlands/notifications/notification_tracker/'
    else:
        return 'https://api.robinhood.com/notifications/devices/'

def referral_url():
    return 'https://api.robinhood.com/midlands/referral/'

def stockloan_url():
    return 'https://api.robinhood.com/accounts/stock_loan_payments/'

def interest_url():
    return 'https://api.robinhood.com/accounts/sweeps/'

def subscription_url():
    return 'https://api.robinhood.com/subscription/subscription_fees/'

def wiretransfers_url():
    return 'https://api.robinhood.com/wire/transfers'

def watchlist_by_name_url(name):
    return f'https://api.robinhood.com/watchlists/{name}/'

def watchlist_add_url(watchlist_name):
    return f'https://api.robinhood.com/watchlists/{watchlist_name}/'

def document_by_id_url(document_id):
    return f'https://api.robinhood.com/documents/{document_id}/'

def dividends_by_instrument_url(instrument_id):
    return f'https://api.robinhood.com/dividends/?instrument={instrument_id}'

def ach_relationships_delete_url(bank_account_id):
    return f'https://api.robinhood.com/ach/relationships/{bank_account_id}/'

def cash_management_cards_transactions_url():
    return 'https://api.robinhood.com/cash_management/cards/transactions/'

def accounts_day_trades_url():
    return 'https://api.robinhood.com/accounts/day_trades/'

def cash_management_stock_loan_payments_url():
    return 'https://api.robinhood.com/cash_management/stock_loan_payments/'

def cash_management_interest_payments_url():
    return 'https://api.robinhood.com/cash_management/interest_payments/'

def watchlists_url(name=None, add=False):
    if name:
        return 'https://api.robinhood.com/midlands/lists/items/'
    else:
        return 'https://api.robinhood.com/midlands/lists/default/'

# Markets
def currency_url():
    return 'https://nummus.robinhood.com/currency_pairs/'

def markets_url():
    return 'https://api.robinhood.com/markets/'

def market_hours_url(market, date):
    return f'https://api.robinhood.com/markets/{market}/hours/{date}/'

def movers_sp500_url():
    return 'https://api.robinhood.com/midlands/movers/sp500/'

def get_100_most_popular_url():
    return 'https://api.robinhood.com/midlands/tags/tag/100-most-popular/'

def movers_top_url():
    return 'https://api.robinhood.com/midlands/tags/tag/top-movers/'

def market_category_url(category):
    return f'https://api.robinhood.com/midlands/tags/tag/{category}/'

def market_by_id_url(market):
    return f'https://api.robinhood.com/markets/{market}/'

def market_hours_by_market_url(market):
    return f'https://api.robinhood.com/markets/{market}/hours/'

# Options
def aggregate_url(account_number=None):
    if account_number:
        return f'https://api.robinhood.com/options/aggregate_positions/?account_number={account_number}'
    else:
        return 'https://api.robinhood.com/options/aggregate_positions/'

def option_historicals_url(option_id):
    return f'https://api.robinhood.com/options/instruments/{option_id}/historicals/'

def option_instruments_url(option_id=None):
    if option_id:
        return f'https://api.robinhood.com/options/instruments/{option_id}/'
    else:
        return 'https://api.robinhood.com/options/instruments/'

def option_orders_url(orderID=None, account_number=None, start_date=None):
    url = 'https://api.robinhood.com/options/orders/'
    if orderID:
        url += f'{orderID}/'
    
    query_params = []
    if account_number:
        query_params.append(f'account_numbers={account_number}')
    if start_date:
        query_params.append(f'updated_at[gte]={start_date}')
    
    if query_params:
        url += '?' + '&'.join(query_params)
    
    return url

def option_positions_url(account_number=None):
    if account_number:
        return f'https://api.robinhood.com/options/positions/?account_numbers={account_number}'
    else:
        return 'https://api.robinhood.com/options/positions/'

def marketdata_options_url():
    return 'https://api.robinhood.com/marketdata/options/'

def option_chains_url(instrument_id):
    return f'https://api.robinhood.com/options/chains/?equity_instrument_ids={instrument_id}'

def option_chains_by_id_url(chain_id):
    return f'https://api.robinhood.com/options/chains/{chain_id}/'

# Pricebook
def marketdata_quotes_url(instrument_id):
    return f'https://api.robinhood.com/marketdata/quotes/{instrument_id}/'

def marketdata_pricebook_url(instrument_id):
    return f'https://api.robinhood.com/marketdata/pricebook/snapshots/{instrument_id}/'

# Crypto
def order_crypto_url():
    return 'https://nummus.robinhood.com/orders/'

def crypto_account_url():
    return 'https://nummus.robinhood.com/accounts/'

def crypto_currency_pairs_url():
    return 'https://nummus.robinhood.com/currency_pairs/'

def crypto_quote_url(crypto_id):
    return f'https://nummus.robinhood.com/currencies/{crypto_id}/quote/'

def crypto_holdings_url():
    return 'https://nummus.robinhood.com/positions/'

def crypto_historical_url(crypto_id):
    return f'https://nummus.robinhood.com/currencies/{crypto_id}/historicals/'

def crypto_currency_url(symbol):
    return f'https://nummus.robinhood.com/currencies/{symbol}/'

def crypto_orders_url(orderID=None):
    if orderID:
        return f'https://nummus.robinhood.com/orders/{orderID}/'
    else:
        return 'https://nummus.robinhood.com/orders/'

def crypto_cancel_url(order_id):
    return f'https://nummus.robinhood.com/orders/{order_id}/cancel/'

# Orders
def cancel_url(order_id):
    return f'https://api.robinhood.com/orders/{order_id}/cancel/'

def option_cancel_url(order_id):
    return f'https://api.robinhood.com/options/orders/{order_id}/cancel/'

def orders_url(orderID=None, account_number=None, start_date=None):
    url = 'https://api.robinhood.com/orders/'
    if orderID:
        url += f'{orderID}/'
    
    query_params = []
    if account_number:
        query_params.append(f'account_numbers={account_number}')
    if start_date:
        query_params.append(f'updated_at[gte]={start_date}')
    
    if query_params:
        url += '?' + '&'.join(query_params)
    
    return url

def all_watchlists_url():
    return 'https://api.robinhood.com/watchlists/'

def notifications_base_url():
    return 'https://api.robinhood.com/notifications/'

def margin_interest_url():
    return 'https://api.robinhood.com/margin/interest/'