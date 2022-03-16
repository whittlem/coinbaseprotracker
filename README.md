# Coinbase Pro Portfolio Tracker

## Introduction

Follow me on Medium for updates!
https://whittle.medium.com

## Prerequisites

- Python 3.x installed -- https://installpython3.com

  `python3 --version`

  Python 3.9.1

- Python 3 PIP installed -- https://pip.pypa.io/en/stable/installing

  `python3 -m pip --version`

  pip 21.0.1 from /usr/local/lib/python3.9/site-packages/pip (python 3.9)

- The app should work with Python 3.x, but to avoid issues try run Python 3.8 or higher

## Installation

```
git clone https://github.com/whittlem/coinbaseprotracker
cd coinbaseprotracker
python3 -m pip install -r requirements.txt
```

## Configuration

    Create a config.json:

    * Add 1 or more portfolios with a single market

    {
        "<portfolio_name>" : {
            "api_key" : "<coinbase_pro_api_key>",
            "api_secret" : "<coinbase_pro_api_secret>",
            "api_passphrase" : "<coinbase_pro_api_passphrase>",
            "config" : {
                "base_currency" : "<base_symbol>",
                "quote_currency" : "<quote_symbol>"
            "}
        },
        "<portfolio_name>" : {
            "api_key" : "<coinbase_pro_api_key>",
            "api_secret" : "<coinbase_pro_api_secret>",
            "api_passphrase" : "<coinbase_pro_api_passphrase>",
            "config" : {
                "base_currency" : "<base_symbol>",
                "quote_currency" : "<quote_symbol>"
            "}
        }
    }

    * Add 1 or more portfolios with multiple markets

    {
        "<portfolio_name>" : {
            "api_key" : "<coinbase_pro_api_key>",
            "api_secret" : "<coinbase_pro_api_secret>",
            "api_passphrase" : "<coinbase_pro_api_passphrase>",
            "config" : [{
                "base_currency" : "<base_symbol>",
                "quote_currency" : "<quote_symbol>"
            "}],[{
                "base_currency" : "<base_symbol>",
                "quote_currency" : "<quote_symbol>"
            "}]
        }
    }

    * Notice that to add multiple markets you convert the 'config' from a dictionary to a list.

    <portfolio_name> - Coinbase Pro portfolio name E.g. "Default Portfolio"
    <coinbase_pro_api_key> - Coinbase Pro API key for the portfolio
    <coinbase_pro_api_secret> - Coinbase Pro API secret for the portfolio
    <coinbase_pro_api_passphrase> - Coinbase Pro API passphrase for the portfolio
    <base_symbol> - Base currency E.g. BTC
    <quote_symbol> - Base currency E.g. GBP


    whittlem@Michaels-iMac-2 coinbaseprotracker % /usr/local/opt/python@3.9/bin/python3 /Users/whittlem/Documents/Repos/Python/coinbaseprotracker/coinbaseprotracker.py
    Create a config.json:

    * Add 1 or more portfolios with a single market

    {
        "<portfolio_name>" : {
            "api_key" : "<coinbase_pro_api_key>",
            "api_secret" : "<coinbase_pro_api_secret>",
            "api_passphrase" : "<coinbase_pro_api_passphrase>",
            "config" : {
                "base_currency" : "<base_symbol>",
                "quote_currency" : "<quote_symbol>"
            "}
        },
        "<portfolio_name>" : {
            "api_key" : "<coinbase_pro_api_key>",
            "api_secret" : "<coinbase_pro_api_secret>",
            "api_passphrase" : "<coinbase_pro_api_passphrase>",
            "config" : {
                "base_currency" : "<base_symbol>",
                "quote_currency" : "<quote_symbol>"
            "}
        }
    }

    * Add 1 or more portfolios with multiple markets

    {
        "<portfolio_name>" : {
            "api_key" : "<coinbase_pro_api_key>",
            "api_secret" : "<coinbase_pro_api_secret>",
            "api_passphrase" : "<coinbase_pro_api_passphrase>",
            "config" : [{
                "base_currency" : "<base_symbol>",
                "quote_currency" : "<quote_symbol>"
            "}],[{
                "base_currency" : "<base_symbol>",
                "quote_currency" : "<quote_symbol>"
            "}]
        }
    }

    * Notice that to add multiple markets you convert the 'config' from a dictionary to a list.

    <portfolio_name> - Coinbase Pro portfolio name E.g. "Default Portfolio"
    <coinbase_pro_api_key> - Coinbase Pro API key for the portfolio
    <coinbase_pro_api_secret> - Coinbase Pro API secret for the portfolio
    <coinbase_pro_api_passphrase> - Coinbase Pro API passphrase for the portfolio

    <base_symbol> - Base currency E.g. BTC
    <quote_symbol> - Base currency E.g. GBP

## Run it

% python3 coinbaseprotracker.py

## Docker

### Build

`docker build -t coinbase-pro-tracker .`

### Run

`docker run --name tracker --rm coinbase-pro-tracker`
