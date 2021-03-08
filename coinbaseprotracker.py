import json, sys
from models.CoinbasePro import AuthAPI as CBAuthAPI, PublicAPI as CBPublicAPI

try:
    with open('config.json') as config_file:
        config = json.load(config_file)

    if not isinstance(config, dict):
        raise TypeError('config.json is invalid.')

    for portfolio in list(config):
        portfolio_config = config[portfolio]

        if 'api_key' in portfolio_config and 'api_secret' in portfolio_config and 'api_pass' in portfolio_config and 'config' in portfolio_config:
            print ('=== ', portfolio, " =======================================================\n")

            api_key = portfolio_config['api_key']
            api_secret = portfolio_config['api_secret']
            api_pass = portfolio_config['api_pass']


            config = portfolio_config['config']
            if ('cryptoMarket' not in config and 'base_currency' not in config) and ('fiatMarket' not in config and 'quote_currency' not in config):
                print ('warning: skipped as cryptoMarket/base_currency and fiatMarket/quote_currency not present under "config" in config.json!', "\n")
                break

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
            orders = api.getOrders(market)

            fees = api.authAPI('GET', 'fees')
            maker_fee_rate = float(fees['maker_fee_rate'].to_string(index=False).strip())
            taker_fee_rate = float(fees['maker_fee_rate'].to_string(index=False).strip())

            if len(orders) > 0:
                last_order = orders.iloc[-1:]
                last_buy_order = last_order[last_order.action == 'buy']
                last_buy_order = last_buy_order.reset_index(drop=True)

                if len(last_buy_order) > 0:
                    print (last_buy_order.to_string(index=False))

                    market = last_buy_order['market'].to_string(index=False).strip()
                    order_type = last_buy_order['type'].to_string(index=False).strip()
                    size = float(last_buy_order['size'].to_string(index=False).strip())
                    value = float(last_buy_order['value'].to_string(index=False).strip())
                    price = float(last_buy_order['price'].to_string(index=False).strip())
                    
                    api = CBPublicAPI()
                    ticker = api.getTicker(market)
                    current_value = ticker * size

                    gross_profit = current_value - value

                    maker_sale_fees = current_value * maker_fee_rate
                    taker_sale_fees = current_value * taker_fee_rate

                    maker_net_profit = current_value - value - maker_sale_fees
                    maker_margin = (current_value - value - maker_fee_rate) / current_value * 100

                    taker_net_profit = current_value - value - taker_sale_fees
                    taker_margin = (current_value - value - taker_fee_rate) / current_value * 100

                    if isinstance(ticker, float): 
                        print ("\n", "       Current Price :", "{:.2f}".format(ticker))

                        print ("\n", "      Purchase Value :", "{:.2f}".format(value))
                        print (     "        Current Value :", "{:.2f}".format(current_value))

                        print ("\n", "      Maker Sale Fee :", "{:.2f}".format(maker_sale_fees), '(', str(maker_fee_rate), ')')
                        print (     "       Taker Sale Fee :", "{:.2f}".format(taker_sale_fees), '(', str(taker_fee_rate), ')')

                        print ("\n", "        Gross Profit :", "{:.2f}".format(gross_profit))

                        print ("\n", "    Maker Net Profit :", "{:.2f}".format(maker_net_profit))
                        print (     "         Maker Margin :", str("{:.2f}".format(maker_margin)) + '%')

                        print ("\n", "    Taker Net Profit :", "{:.2f}".format(taker_net_profit))
                        print (     "         Taker Margin :", str("{:.2f}".format(taker_margin)) + '%')

                else:
                    if len(orders) > 0:
                        second_last_order = orders.iloc[-2:]
                        last_buy_order = second_last_order[second_last_order.action == 'buy']
                        last_buy_order = last_buy_order.reset_index(drop=True)

                        if len(last_buy_order) > 0:
                            orders = api.getOrders(status='open')
                            if len(orders) == 1:
                                last_open_order = orders[orders.action == 'sell']
                                last_open_order = last_open_order.reset_index(drop=True)

                                print (last_buy_order.to_string(index=False))
                                print ("\n", last_open_order.to_string(index=False))
                                
                                market = last_buy_order['market'].to_string(index=False).strip()
                                order_type = last_buy_order['type'].to_string(index=False).strip()
                                size = float(last_buy_order['size'].to_string(index=False).strip())
                                value = float(last_buy_order['value'].to_string(index=False).strip())
                                price = float(last_buy_order['price'].to_string(index=False).strip())

                                future_value = float(last_open_order['value'].to_string(index=False).strip())

                                api = CBPublicAPI()
                                ticker = api.getTicker(market)
                                current_value = ticker * size

                                gross_profit = current_value - value

                                maker_sale_fees = future_value * maker_fee_rate
                                taker_sale_fees = current_value * taker_fee_rate

                                maker_net_profit = future_value - value - maker_sale_fees
                                maker_margin = (future_value - value - maker_fee_rate) / future_value * 100

                                taker_net_profit = current_value - value - taker_sale_fees
                                taker_margin = (current_value - value - taker_fee_rate) / current_value * 100

                                future_gross_profit = future_value - value

                                if isinstance(ticker, float): 
                                    print ("\n", "       Current Price :", "{:.2f}".format(ticker))

                                    print ("\n", "      Purchase Value :", "{:.2f}".format(value))
                                    print (     "        Current Value :", "{:.2f}".format(current_value))
                                    print (     "         Target Value :", "{:.2f}".format(future_value))

                                    print ("\n", "      Maker Sale Fee :", "{:.2f}".format(maker_sale_fees), '(', str(maker_fee_rate), ')')
                                    print (     "       Taker Sale Fee :", "{:.2f}".format(taker_sale_fees), '(', str(taker_fee_rate), ')')

                                    print ("\n", "        Gross Profit :", "{:.2f}".format(gross_profit), '(now)')
                                    print (     "     Taker Net Profit :", "{:.2f}".format(taker_net_profit), '(now)')
                                    print (     "         Taker Margin :", str("{:.2f}".format(taker_margin)) + '%', '(now)')

                                    print ("\n", "        Gross Profit :", "{:.2f}".format(future_gross_profit), '(target)')
                                    print (     "     Maker Net Profit :", "{:.2f}".format(maker_net_profit), '(target)')
                                    print (     "         Maker Margin :", str("{:.2f}".format(maker_margin)) + '%', '(target)')

                            else:
                                print ('*** no active position open ***')

                        else:
                            print ('*** no active position open ***')

                    else:
                        print ('*** no active position open ***')
            
            print ("\n")

        #break

except IOError as err:
    print (err)
except Exception as err:
    print (err)