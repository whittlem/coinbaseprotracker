# Coinbase Pro Portfolio Tracker

## Introduction

Follow me on Medium for updates!
https://whittle.medium.com

## Prerequisites

* Python 3.x installed -- https://installpython3.com

    % python3 --version
    
    Python 3.9.1
    
* Python 3 PIP installed -- https://pip.pypa.io/en/stable/installing

    % python3 -m pip --version
    
    pip 21.0.1 from /usr/local/lib/python3.9/site-packages/pip (python 3.9)

 * The app should work with Python 3.x, but to avoid issues try run Python 3.8 or higher

## Installation

    git clone https://github.com/whittlem/coinbaseprotracker
    cd coinbaseprotracker

## Configuration

Create a config.json file with your read-only Coinbase Pro portfolio API keys:

    {
        "Bot - XLM-EUR" : {
            "api_key" : "YOUR_PORTFOLIO_COINBASE_PRO_API_KEY",
            "api_secret" : "YOUR_PORTFOLIO_COINBASE_PRO_API_SECRET",
            "api_pass" : "YOUR_PORTFOLIO_COINBASE_PRO_API_PASSPHRASE"
        },
        "Bot - ETH-GBP" : {
            "api_key" : "YOUR_PORTFOLIO_COINBASE_PRO_API_KEY",
            "api_secret" : "YOUR_PORTFOLIO_COINBASE_PRO_API_SECRET",
            "api_pass" : "YOUR_PORTFOLIO_COINBASE_PRO_API_PASSPHRASE"
        },
        "Bot - BTC-GBP" : {
            "api_key" : "YOUR_PORTFOLIO_COINBASE_PRO_API_KEY",
            "api_secret" : "YOUR_PORTFOLIO_COINBASE_PRO_API_SECRET",
            "api_pass" : "YOUR_PORTFOLIO_COINBASE_PRO_API_PASSPHRASE"
        },
        "Bot - BCH-GBP" : {
            "api_key" : "YOUR_PORTFOLIO_COINBASE_PRO_API_KEY",
            "api_secret" : "YOUR_PORTFOLIO_COINBASE_PRO_API_SECRET",
            "api_pass" : "YOUR_PORTFOLIO_COINBASE_PRO_API_PASSPHRASE"
        },
        "Bot - LTC-GBP" : {
            "api_key" : "YOUR_PORTFOLIO_COINBASE_PRO_API_KEY",
            "api_secret" : "YOUR_PORTFOLIO_COINBASE_PRO_API_SECRET",
            "api_pass" : "YOUR_PORTFOLIO_COINBASE_PRO_API_PASSPHRASE"
        }        
    }

## Run it

% python3 coinbaseprotracker.py