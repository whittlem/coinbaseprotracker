import re, json, sys
import numpy as np
import pandas as pd
from models.CoinbasePro import AuthAPI as CBAuthAPI, PublicAPI as CBPublicAPI

def printHelp():
    print ('Create a config.json:')
    print ('* Add 1 or more portfolios', "\n")

    print ('{')
    print ('    "<portfolio_name>" : {')
    print ('        "api_key" : "<coinbase_pro_api_key>",')
    print ('        "api_secret" : "<coinbase_pro_api_secret>",')
    print ('        "api_pass" : "<coinbase_pro_api_passphrase>",')
    print ('        "config" : {')
    print ('            "base_currency" : "<base_symbol>",')
    print ('            "quote_currency" : "<quote_symbol>"')
    print ('        "}')
    print ('    },')
    print ('    "<portfolio_name>" : {')
    print ('        "api_key" : "<coinbase_pro_api_key>",')
    print ('        "api_secret" : "<coinbase_pro_api_secret>",')
    print ('        "api_pass" : "<coinbase_pro_api_passphrase>",')
    print ('        "config" : {')
    print ('            "base_currency" : "<base_symbol>",')
    print ('            "quote_currency" : "<quote_symbol>"')
    print ('        "}')
    print ('    }')
    print ('}', "\n")

    print ('<portfolio_name> - Coinbase Pro portfolio name E.g. "Default portfolio"')
    print ('<coinbase_pro_api_key> - Coinbase Pro API key for the portfolio')
    print ('<coinbase_pro_api_secret> - Coinbase Pro API secret for the portfolio')
    print ('<coinbase_pro_api_passphrase> - Coinbase Pro API passphrase for the portfolio')
    print ('<base_symbol> - Base currency E.g. BTC')
    print ('<quote_symbol> - Base currency E.g. GBP')
    print ("\n")

try:
    with open('config.json') as config_file:
        json_config = json.load(config_file)

    if not isinstance(json_config, dict):
        raise TypeError('config.json is invalid.')

    if len(list(json_config)) < 1:
        printHelp()
        sys.exit()

    df = pd.DataFrame()

    for portfolio in list(json_config):
        base_currency = ''
        quote_currency = ''
        market = ''

        portfolio_config = json_config[portfolio]

        if 'api_key' in portfolio_config and 'api_secret' in portfolio_config and 'api_pass' in portfolio_config and 'config' in portfolio_config:
            api_key = portfolio_config['api_key']
            api_secret = portfolio_config['api_secret']
            api_pass = portfolio_config['api_pass']

            config = portfolio_config['config']
            if ('cryptoMarket' not in config and 'base_currency' not in config) and ('fiatMarket' not in config and 'quote_currency' not in config):
                printHelp()
                sys.exit()

            if 'cryptoMarket' in config:
                base_currency = config['cryptoMarket']
            elif 'base_currency' in config:
                base_currency = config['base_currency']

            if 'fiatMarket' in config:
                quote_currency = config['fiatMarket']
            elif 'base_currency' in config:
                quote_currency = config['quote_currency']

            market = base_currency + '-' + quote_currency

            api = CBAuthAPI(api_key, api_secret, api_pass)
            
            orders = api.getOrders()
            df = pd.concat([df, orders])

            transfers = api.getTransfers()
            df = pd.concat([df, transfers])

    df['created_at'] = df['created_at'].map(lambda x: re.sub(r"\.\d{1,6}\+00$", "", str(x)))
    df['created_at'] = df['created_at'].map(lambda x: re.sub(r"\+00:00$", "", str(x)))

    save_file = 'profitandloss.csv'

    try:
        df.to_csv(save_file, index=False)
    except OSError:
        raise SystemExit('Unable to save: ', save_file) 

except IOError as err:
    print (err)
except Exception as err:
    print (err)