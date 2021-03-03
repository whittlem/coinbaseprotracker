import json, sys
from models.CoinbasePro import AuthAPI as CBAuthAPI, PublicAPI as CBPublicAPI

try:
    with open('config.json') as config_file:
        config = json.load(config_file)

    if not isinstance(config, dict):
        raise TypeError('config.json is invalid.')

    for portfolio in list(config):
        portfolio_config = config[portfolio]

        if 'api_key' in portfolio_config and 'api_secret' in portfolio_config and 'api_pass' in portfolio_config:
            print ('=== ', portfolio, " =======================================================\n")

            api_key = portfolio_config['api_key']
            api_secret = portfolio_config['api_secret']
            api_pass = portfolio_config['api_pass']

            api = CBAuthAPI(api_key, api_secret, api_pass)
            orders = api.getOrders()

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

                    if isinstance(ticker, float): 
                        print ("\n", "       Current Price :", "{:.2f}".format(ticker))

                        print ("\n", "      Purchase Value :", "{:.2f}".format(value))
                        print (     "        Current Value :", "{:.2f}".format(current_value))

                        print ("\n", "      Maker Sale Fee :", "{:.2f}".format(maker_sale_fees), '(', str(maker_fee_rate), ')')
                        print (     "        Take Sale Fee :", "{:.2f}".format(taker_sale_fees), '(', str(taker_fee_rate), ')')

                        print ("\n", "        Gross Profit :", "{:.2f}".format(gross_profit))

                        print ("\n", "    Maker Net Profit :", "{:.2f}".format(maker_net_profit))
                        print (     "         Maker Margin :", str("{:.2f}".format(maker_margin)) + '%')

                        print ("\n", "    Taker Net Profit :", "{:.2f}".format(maker_net_profit))
                        print (     "         Taker Margin :", str("{:.2f}".format(maker_margin)) + '%')

                else:
                    print ('*** no active position open ***')
            
            print ("\n")

        #break

except IOError as err:
    print (err)
except Exception as err:
    print (err)