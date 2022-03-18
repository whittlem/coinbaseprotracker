#!/usr/bin/env python3
# encoding: utf-8

import sys
import json
import warnings
import pandas as pd
from models.exchange.coinbase_pro import AuthAPI as CBAuthAPI, PublicAPI as CBPublicAPI

warnings.simplefilter(action="ignore", category=FutureWarning)

def printHelp():
    print("Create a config.json:\n")

    print("* Add 1 or more portfolios with a single market\n")

    print("{")
    print('    "<portfolio_name>" : {')
    print('        "api_key" : "<coinbase_pro_api_key>",')
    print('        "api_secret" : "<coinbase_pro_api_secret>",')
    print('        "api_passphrase" : "<coinbase_pro_api_passphrase>",')
    print('        "config" : {')
    print('            "base_currency" : "<base_symbol>",')
    print('            "quote_currency" : "<quote_symbol>"')
    print('        "}')
    print("    },")
    print('    "<portfolio_name>" : {')
    print('        "api_key" : "<coinbase_pro_api_key>",')
    print('        "api_secret" : "<coinbase_pro_api_secret>",')
    print('        "api_passphrase" : "<coinbase_pro_api_passphrase>",')
    print('        "config" : {')
    print('            "base_currency" : "<base_symbol>",')
    print('            "quote_currency" : "<quote_symbol>"')
    print('        "}')
    print("    }")
    print("}\n")

    print("* Add 1 or more portfolios with multiple markets\n")

    print("{")
    print('    "<portfolio_name>" : {')
    print('        "api_key" : "<coinbase_pro_api_key>",')
    print('        "api_secret" : "<coinbase_pro_api_secret>",')
    print('        "api_passphrase" : "<coinbase_pro_api_passphrase>",')
    print('        "config" : [{')
    print('            "base_currency" : "<base_symbol>",')
    print('            "quote_currency" : "<quote_symbol>"')
    print('        "}],[{')
    print('            "base_currency" : "<base_symbol>",')
    print('            "quote_currency" : "<quote_symbol>"')
    print('        "}]')
    print("    }")
    print("}\n")

    print("* Notice that to add multiple markets you convert the 'config' from a dictionary to a list.\n")

    print('<portfolio_name> - Coinbase Pro portfolio name E.g. "Default Portfolio"')
    print("<coinbase_pro_api_key> - Coinbase Pro API key for the portfolio")
    print("<coinbase_pro_api_secret> - Coinbase Pro API secret for the portfolio")
    print(
        "<coinbase_pro_api_passphrase> - Coinbase Pro API passphrase for the portfolio\n"
    )
    print("<base_symbol> - Base currency E.g. BTC")
    print("<quote_symbol> - Base currency E.g. GBP")
    print("\n")


try:
    with open("config.json") as config_file:
        json_config = json.load(config_file)

    if not isinstance(json_config, dict):
        raise TypeError("config.json is invalid.")

    if len(list(json_config)) < 1:
        printHelp()
        sys.exit()

    df_tracker = pd.DataFrame()

    for portfolio in list(json_config):
        base_currency = ""
        quote_currency = ""
        market = ""

        portfolio_config = json_config[portfolio]

        if (
            "api_key" in portfolio_config
            and "api_secret" in portfolio_config
            and ("api_passphrase" in portfolio_config or "api_passphrase" in portfolio_config)
            and "config" in portfolio_config
        ):
            print(
                "=== ",
                portfolio,
                " =======================================================\n",
            )

            api_key = portfolio_config["api_key"]
            api_secret = portfolio_config["api_secret"]

            if "api_pass" in portfolio_config:
                api_pass = portfolio_config["api_pass"]
            elif "api_passphrase" in portfolio_config:
                api_pass = portfolio_config["api_passphrase"]

            config = portfolio_config["config"]

            if (
                (isinstance(config, list))
                and (
                    "cryptoMarket" not in config[0] and "base_currency" not in config[0]
                )
                and (
                    "fiatMarket" not in config[0] and "quote_currency" not in config[0]
                )
            ):
                printHelp()
                sys.exit()
            elif (
                (isinstance(config, dict))
                and (
                    "cryptoMarket" not in config and "base_currency" not in config
                )
                and (
                    "fiatMarket" not in config and "quote_currency" not in config
                )
            ):
                printHelp()
                sys.exit()


            if isinstance(config, list):
                config_list = config
            elif isinstance(config, dict):
                config_list = [config]

            total_markets = 0
            total_profit = 0
            total_margin = 0

            for config_item in config_list:
                total_markets += 1

                if "cryptoMarket" in config_item:
                    base_currency = config_item["cryptoMarket"]
                elif "base_currency" in config_item:
                    base_currency = config_item["base_currency"]

                if "fiatMarket" in config_item:
                    quote_currency = config_item["fiatMarket"]
                elif "base_currency" in config_item:
                    quote_currency = config_item["quote_currency"]

                market = base_currency + "-" + quote_currency

                api = CBAuthAPI(api_key, api_secret, api_pass)
                orders = api.getOrders(market)

                last_action = ""
                if len(orders) > 0:
                    for market in orders["market"].sort_values().unique():
                        df_market = orders[orders["market"] == market]
                else:
                    df_market = pd.DataFrame()

                df_buy = pd.DataFrame()
                df_sell = pd.DataFrame()

                pair = 0
                # pylint: disable=unused-variable
                for index, row in df_market.iterrows():
                    if row["action"] == "buy":
                        pair = 1

                    if pair == 1 and (row["action"] != last_action):
                        if row["action"] == "buy":
                            df_buy = row
                        elif row["action"] == "sell":
                            df_sell = row

                    if row["action"] == "sell" and len(df_buy) != 0:
                        df_pair = pd.DataFrame(
                            [
                                [
                                    df_sell["status"],
                                    df_buy["market"],
                                    df_buy["created_at"],
                                    df_buy["type"],
                                    df_buy["size"],
                                    df_buy["filled"],
                                    df_buy["fees"],
                                    df_buy["price"],
                                    df_sell["created_at"],
                                    df_sell["type"],
                                    df_sell["size"],
                                    df_sell["filled"],
                                    df_sell["fees"],
                                    df_sell["price"],
                                ]
                            ],
                            columns=[
                                "status",
                                "market",
                                "buy_at",
                                "buy_type",
                                "buy_size",
                                "buy_filled",
                                "buy_fees",
                                "buy_price",
                                "sell_at",
                                "sell_type",
                                "sell_size",
                                "sell_filled",
                                "sell_fees",
                                "sell_price",
                            ],
                        )

                        df_tracker = df_tracker.append(df_pair, ignore_index=True)
                        pair = 0

                    last_action = row["action"]

                fees = api.authAPI("GET", "fees")

                maker_fee_rate = float(
                    fees["maker_fee_rate"].to_string(index=False).strip()
                )
                taker_fee_rate = float(
                    fees["taker_fee_rate"].to_string(index=False).strip()
                )

                if len(orders) > 0:
                    last_order = orders.iloc[-1:]
                    last_buy_order = last_order[last_order.action == "buy"]
                    last_buy_order = last_buy_order.reset_index(drop=True)

                    if len(last_buy_order) > 0:
                        print(last_buy_order.to_string(index=False))

                        api = CBPublicAPI()
                        ticker = api.getTicker(market)
                        current_price = ticker[1]

                        market = last_buy_order["market"].to_string(index=False).strip()
                        buy_type = last_buy_order["type"].to_string(index=False).strip()
                        buy_size = round(
                            float(last_buy_order["size"].to_string(index=False).strip()), 8
                        )
                        buy_filled = round(
                            float(last_buy_order["filled"].to_string(index=False).strip()),
                            8,
                        )
                        buy_fees = round(
                            float(last_buy_order["fees"].to_string(index=False).strip()), 8
                        )
                        buy_price = round(
                            float(last_buy_order["price"].to_string(index=False).strip()), 8
                        )

                        sell_fees = (buy_filled * current_price) * taker_fee_rate

                        current_size = buy_filled * current_price - (
                            (buy_filled * current_price) * taker_fee_rate
                        )

                        net_profit = round(current_size - buy_size, 2)
                        margin = (net_profit / buy_size) * 100

                        if isinstance(current_price, float):
                            print("\n", "       Current Price :", current_price)

                            print("\n", "      Purchase Value :", "{:.2f}".format(buy_size))
                            print("        Current Value :", "{:.2f}".format(current_size))

                            if buy_type == "market":
                                print(
                                    "\n",
                                    "             Buy Fee :",
                                    "{:.6f}".format(buy_fees),
                                    "(",
                                    str(taker_fee_rate),
                                    ")",
                                )
                                print(
                                    "             Sell Fee :",
                                    "{:.6f}".format(sell_fees),
                                    "(",
                                    str(taker_fee_rate),
                                    ")",
                                )
                            elif buy_type == "limit":
                                print(
                                    "\n",
                                    "             Buy Fee :",
                                    "{:.6f}".format(buy_fees),
                                    "(",
                                    str(maker_fee_rate),
                                    ")",
                                )
                                print(
                                    "             Sell Fee :",
                                    "{:.6f}".format(sell_fees),
                                    "(",
                                    str(maker_fee_rate),
                                    ")",
                                )

                            print(
                                "\n",
                                "              Profit :",
                                "{:.2f}".format(net_profit),
                            )
                            total_profit += net_profit
                            print(
                                "               Margin :",
                                str("{:.2f}".format(margin)) + "%",
                            )
                            total_margin += margin

                    else:
                        if len(orders) > 0:
                            second_last_order = orders.iloc[-2:-1]
                            last_buy_order = second_last_order[
                                second_last_order.action == "buy"
                            ]
                            last_buy_order = last_buy_order.reset_index(drop=True)

                            if len(last_buy_order) > 0:
                                orders = api.getOrders(status="open")
                                if len(orders) == 1:
                                    last_open_order = orders[orders.action == "sell"]
                                    last_open_order = last_open_order.reset_index(drop=True)

                                    print(last_buy_order.to_string(index=False))
                                    print("\n", last_open_order.to_string(index=False))

                                    api = CBPublicAPI()
                                    ticker = api.getTicker(market)
                                    current_price = ticker[1]
                                    future_price = float(last_open_order["price"].values[0])

                                    market = (
                                        last_buy_order["market"]
                                        .to_string(index=False)
                                        .strip()
                                    )
                                    buy_type = (
                                        last_buy_order["type"]
                                        .to_string(index=False)
                                        .strip()
                                    )
                                    buy_size = round(
                                        float(
                                            last_buy_order["size"]
                                            .to_string(index=False)
                                            .strip()
                                        ),
                                        8,
                                    )
                                    buy_filled = round(
                                        float(
                                            last_buy_order["filled"]
                                            .to_string(index=False)
                                            .strip()
                                        ),
                                        8,
                                    )
                                    buy_fees = round(
                                        float(
                                            last_buy_order["fees"]
                                            .to_string(index=False)
                                            .strip()
                                        ),
                                        8,
                                    )
                                    buy_price = round(
                                        float(
                                            last_buy_order["price"]
                                            .to_string(index=False)
                                            .strip()
                                        ),
                                        8,
                                    )

                                    sell_fees = (
                                        buy_filled * current_price
                                    ) * taker_fee_rate

                                    current_size = buy_filled * current_price - (
                                        (buy_filled * current_price) * taker_fee_rate
                                    )

                                    net_profit = round(current_size - buy_size, 2)
                                    margin = (net_profit / buy_size) * 100

                                    sell_size = round(
                                        float(
                                            last_open_order["value"]
                                            .to_string(index=False)
                                            .strip()
                                        ),
                                        8,
                                    )

                                    sell_filled = round(
                                        float(
                                            last_open_order["size"]
                                            .to_string(index=False)
                                            .strip()
                                        ),
                                        8,
                                    )

                                    future_size = sell_filled * future_price - (
                                        (sell_filled * future_price) * taker_fee_rate
                                    )

                                    maker_net_profit = round(sell_size - buy_filled, 2)
                                    maker_margin = (maker_net_profit / sell_size) * 100

                                    if isinstance(current_price, float):
                                        print("\n", "       Current Price :", current_price)

                                        print(
                                            "\n",
                                            "      Purchase Value :",
                                            "{:.2f}".format(buy_size),
                                        )
                                        print(
                                            "        Current Value :",
                                            "{:.2f}".format(current_size),
                                        )
                                        print(
                                            "         Target Value :",
                                            "{:.2f}".format(sell_size),
                                        )

                                        if buy_type == "market":
                                            print(
                                                "\n",
                                                "             Buy Fee :",
                                                "{:.6f}".format(buy_fees),
                                                "(",
                                                str(taker_fee_rate),
                                                ")",
                                            )
                                            print(
                                                "             Sell Fee :",
                                                "{:.6f}".format(sell_fees),
                                                "(",
                                                str(taker_fee_rate),
                                                ")",
                                            )
                                        elif buy_type == "limit":
                                            print(
                                                "\n",
                                                "             Buy Fee :",
                                                "{:.6f}".format(buy_fees),
                                                "(",
                                                str(maker_fee_rate),
                                                ")",
                                            )
                                            print(
                                                "             Sell Fee :",
                                                "{:.6f}".format(sell_fees),
                                                "(",
                                                str(maker_fee_rate),
                                                ")",
                                            )

                                        print(
                                            "\n",
                                            "              Profit :",
                                            "{:.2f}".format(net_profit),
                                            "(now)",
                                        )
                                        total_profit += net_profit
                                        print(
                                            "               Margin :",
                                            str("{:.2f}".format(margin)) + "% (now)",
                                        )
                                        total_margin += margin

                                else:
                                    print("*** no active position open ***")

                            else:
                                print("*** no active position open ***")

                        else:
                            print("*** no active position open ***")

                print("\n")


            print("=============================================================================\n")

            print("        Total Profit :", "{:.2f}".format(total_profit))
            print("        Total Margin :", "{:.2f}".format(total_margin / total_markets) + "%", "\n")

            print("=============================================================================\n")

        else:
            printHelp()
            sys.exit()

    df_tracker = df_tracker[df_tracker["status"] == "done"]
    df_tracker["profit"] = df_tracker["sell_filled"] - df_tracker["buy_size"]
    df_tracker["margin"] = (df_tracker["profit"] / df_tracker["buy_size"]) * 100
    df_2022 = df_tracker[df_tracker["buy_at"] >= "2022-01-01"]

    try:
        """CSV of completed trades in 2022"""
        df_2022.to_csv("completed_trades_2022.csv", index=False)
    except OSError as err:
        SystemExit("Unable to save", err)

except IOError as err:
    print(err)
#except Exception as err:
#    print(err)
