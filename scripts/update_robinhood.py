import pandas as pd
import os
from pandas import json_normalize
import robin_stocks.robinhood as rs
import pyotp

totp_key = os.environ.get('rs_TOTP')
email_key = os.environ.get('rs_email')
pwd_key = os.environ.get('rs_pwd')

# logging in to robinhood
totp = pyotp.TOTP(totp_key).now()
rs.login(email_key, pwd_key, mfa_code=totp)

# stock transactions
df_stock = pd.DataFrame.from_dict(rs.get_all_stock_orders())
print("Number of Stock Transactions: ", len(df_stock))

symbol_list = []
for index, row in df_stock.iterrows():
    sym = rs.request_get(row['instrument'])['symbol']
    symbol_list.insert(0, sym)

df_stock['ticker'] = symbol_list[::-1]
df_stock = df_stock[['side', 'ticker', 'cumulative_quantity',
                     'average_price', 'state', 'last_transaction_at', 'type', 'time_in_force']]
df_stock['category'] = 'stock'
df_stock = df_stock.rename(
    {'cumulative_quantity': 'quantity',
     'average_price': 'price',
     'last_transaction_at': 'date',
     'side': 'action'},
    axis='columns')

# crypto transactions
df_crypto = pd.DataFrame.from_dict(rs.get_all_crypto_orders())
print("Number of Crypto Transactions: ", len(df_crypto))

crypto_symbols = []
for index, row in df_crypto.iterrows():
    sym = rs.crypto.get_crypto_quote_from_id(row['currency_pair_id'])['symbol']

    crypto_symbols.insert(0, sym)

df_crypto['ticker'] = crypto_symbols[::-1]
df_crypto = df_crypto[['side', 'ticker', 'cumulative_quantity',
                       'average_price', 'state', 'last_transaction_at', 'type', 'time_in_force']]
df_crypto['category'] = 'crypto'
df_crypto = df_crypto.rename(
    {'cumulative_quantity': 'quantity',
     'average_price': 'price',
     'last_transaction_at': 'date',
     'side': 'action'},
    axis='columns')

# option transactions
df_option = pd.DataFrame.from_dict(rs.get_all_option_orders())
print("Number of Options Transactions: ", len(df_option))

df_option = df_option[['direction', 'chain_symbol', 'processed_quantity', 'premium',
                       'state', 'updated_at', 'type', 'time_in_force', 'opening_strategy', 'closing_strategy']]
df_option = df_option.rename(
    {'processed_quantity': 'quantity',
     'premium': 'price',
     'updated_at': 'date',
     'direction': 'action',
     'chain_symbol': 'ticker'},
    axis='columns')
df_option['category'] = 'options'

# dividends
df_dividend = pd.DataFrame.from_dict(rs.account.get_dividends())
print("Number of Dividend Transactions: ", len(df_dividend))

symbol_list = []
for index, row in df_dividend.iterrows():
    sym = rs.request_get(row['instrument'])['symbol']

    symbol_list.insert(0, sym)

df_dividend['ticker'] = symbol_list[::-1]
df_dividend = df_dividend[['ticker', 'position',
                           'rate', 'state', 'payable_date']]
df_dividend['category'] = 'dividends'
df_dividend = df_dividend.rename(
    {'position': 'quantity',
     'rate': 'price',
     'payable_date': 'date'},
    axis='columns')
df_dividend['action'] = 'credit'

# ALL TRANSACTIONS
order_history = pd.DataFrame()
order_history = order_history.append(df_stock)
order_history = order_history.append(df_crypto)
order_history = order_history.append(df_option)
order_history = order_history.append(df_dividend)

order_history = order_history.replace({'buy': 'debit', 'sell': 'credit'})
order_history = order_history.sort_values(by='date', ascending=False)

order_history['date'] = pd.to_datetime(order_history['date'])
order_history['price'] = order_history['price'].astype('float')
order_history['quantity'] = order_history['quantity'].astype('float')

order_history['total'] = order_history['quantity'] * order_history['price']

order_history = order_history[order_history['state'].isin(['filled', 'paid'])]
order_history['account'] = 'ROBINHOOD'

order_history = order_history.reset_index(drop=True)
order_history.to_csv(r"C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\data\stocks_orderhistory.csv", index=False)

# current positions
stocks = pd.DataFrame.from_dict(
    rs.build_holdings(), orient='index').reset_index()
stocks = stocks.rename(
    {'index': 'ticker',
     'average_buy_price': 'average_cost'},
    axis='columns')

stocks['price'] = stocks['price'].astype('float')
stocks['quantity'] = stocks['quantity'].astype('float')
stocks['equity'] = stocks['equity'].astype('float')
stocks['percent_change'] = stocks['percent_change'].astype('float')
stocks['pe_ratio'] = stocks['pe_ratio'].astype('float')
stocks['percentage'] = stocks['percentage'].astype('float')
stocks['equity_change'] = stocks['equity_change'].astype('float')

stocks = stocks.drop(['id'], axis=1)

stocks = stocks.sort_values(by='equity', ascending=False)
stocks = stocks.reset_index(drop=True)

stocks['category'] = 'stock'
stocks['account'] = 'ROBINHOOD'

stocks.append({
    'name': 'CASH',
    'price': rs.profiles.load_account_profile()['cash'],
    'quantity': 1
}, ignore_index=True)

# options
options = pd.DataFrame.from_dict(rs.options.get_open_option_positions())
if(len(options) > 0):
    options = options[['average_price', 'chain_symbol', 'quantity',
                       'updated_at', 'option_id', 'trade_value_multiplier']]
    options

    df_option_detail = pd.DataFrame()
    for index, row in options.iterrows():
        option_temp = pd.DataFrame.from_dict(
            rs.options.get_option_market_data_by_id(row['option_id']))
        option_temp = option_temp[['symbol', 'adjusted_mark_price',
                                   'delta', 'gamma', 'rho', 'theta', 'vega', 'implied_volatility']]

        # grab option type, strike price, exp date
        option_details = rs.options.get_option_instrument_data_by_id(
            row['option_id'])
        option_temp['strike_price'] = option_details['strike_price']
        option_temp['expiration_date'] = option_details['expiration_date']
        option_temp['type'] = option_details['type']
        df_option_detail = df_option_detail.append(option_temp)

    options = pd.merge(options, df_option_detail,
                       left_on='chain_symbol', right_on='symbol')
    for i in ['average_price', 'quantity', 'trade_value_multiplier', 'adjusted_mark_price', 'delta', 'gamma', 'rho', 'theta', 'vega', 'implied_volatility', 'strike_price']:
        options[i] = options[i].astype('float')

    options['average_cost'] = options['average_price'] / \
        options['trade_value_multiplier']
    options['quantity'] = options['quantity']*100
    options = options.drop(
        ['option_id', 'trade_value_multiplier', 'chain_symbol', 'average_price'], axis=1)

    options['category'] = 'options'

    options = options.rename(
        {'symbol': 'ticker',
         'adjusted_mark_price': 'price'},
        axis='columns')

    options['equity'] = options['quantity'].astype(
        'float') * options['price'].astype('float')
    options['account'] = 'ROBINHOOD'

crypto = pd.json_normalize(rs.crypto.get_crypto_positions())

cost_bases = pd.DataFrame()
for index, row in crypto.iterrows():
    cost_bases_detail = json_normalize(row['cost_bases'])
    cost_bases = cost_bases.append(cost_bases_detail)

# this is probably a bad idea... but I can't think of any other way to merge the cost basis into the main crytpo
crypto = crypto.merge(cost_bases, left_on='quantity',
                      right_on='direct_quantity')

crypto = crypto[['quantity', 'updated_at',
                 'currency.code', 'currency.name', 'direct_cost_basis']]
crypto = crypto.rename({
    'direct_cost_basis': 'average_cost',
    'currency.code': 'ticker',
    'currency.name': 'name'
}, axis='columns')

prices = []
symbols = []
for index, row in crypto.iterrows():
    prices.append(rs.crypto.get_crypto_quote(row['ticker'])['mark_price'])
    symbols.append(rs.crypto.get_crypto_quote(row['ticker'])['symbol'])

crypto['price'] = prices
crypto['symbol'] = crypto['ticker']
crypto['ticker'] = symbols

crypto['average_cost'] = crypto['average_cost'].astype(
    'float') / crypto['quantity'].astype('float')
crypto['equity'] = crypto['quantity'].astype(
    'float') * crypto['price'].astype('float')
crypto['category'] = 'crypto'
crypto['type'] = 'crypto'

crypto['account'] = 'ROBINHOOD'

# combining all
all_df = pd.concat([stocks, options, crypto])
for col in ['price', 'quantity', 'average_cost', 'equity', 'percent_change', 'equity_change', 'percentage']:
    all_df[col] = all_df[col].astype('float')

all_df['percent_change'] = (
    all_df['price'] - all_df['average_cost']) / all_df['average_cost']
all_df['equity_change'] = all_df['average_cost'] * \
    all_df['quantity'] * all_df['percent_change']
all_df['percentage'] = all_df['equity']/sum(all_df['equity'])

all_df = all_df.reset_index(drop=True)
all_df.to_csv(r"C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\data\stocks_holdings.csv")