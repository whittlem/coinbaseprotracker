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

## Results

I only placed these trades now so ignore the profit/margin :)

    ===  Bot - XLM-EUR  =====================================================================

                created_at   market action    type   size       value status     price
    2021-02-24 09:15:59+00:00  XLM-EUR    buy  market  496.0  174.987498   done  0.352797

    Net Purchase Price : 0.35
    Gross Current Price : 0.35
                Sale Fee : 2.99
            Net Profit : -2.99
                Margin : -0.86%


    ===  Bot - ETH-GBP  =====================================================================

                created_at   market action    type     size       value status    price
    2021-02-24 09:07:24+00:00  ETH-GBP    buy  market  0.13213  157.339309   done  1190.79

    Net Purchase Price : 1190.79
    Gross Current Price : 1190.38
                Sale Fee : 2.99
            Net Profit : -3.40
                Margin : -0.03%


    ===  Bot - BTC-GBP  =====================================================================

                created_at   market action    type      size       value status    price
    2021-02-24 09:05:38+00:00  BTC-GBP    buy  market  0.006732  240.996292   done  35800.0

    Net Purchase Price : 35800.00
    Gross Current Price : 35867.48
                Sale Fee : 2.99
            Net Profit : 64.49
                Margin : 0.19%


    ===  Bot - BCH-GBP  =====================================================================

                created_at   market action    type      size       value status   price
    2021-02-24 09:10:24+00:00  BCH-GBP    buy  market  0.485037  189.038363   done  389.74

    Net Purchase Price : 389.74
    Gross Current Price : 385.25
                Sale Fee : 2.99
            Net Profit : -7.48
                Margin : -1.15%


    ===  Bot - LTC-GBP  =====================================================================

                created_at   market action    type      size       value status   price
    2021-02-24 09:08:45+00:00  LTC-GBP    buy  market  1.545617  204.005979   done  131.99

    Net Purchase Price : 131.99
    Gross Current Price : 132.26
                Sale Fee : 2.99
            Net Profit : -2.72
                Margin : 0.20%