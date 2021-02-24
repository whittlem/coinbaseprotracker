import json
from models.CoinbasePro import AuthAPI as CBAuthAPI, PublicAPI as CBPublicAPI

try:
    with open('config.json') as config_file:
        config = json.load(config_file)

    if not isinstance(config, dict):
        raise TypeError('config.json is invalid.')

    for portfolio in list(config):
        portfolio_config = config[portfolio]

        if 'api_key' in portfolio_config and 'api_secret' in portfolio_config and 'api_pass' in portfolio_config:
            print ('=== ', portfolio, " =====================================================================\n")

            api_key = portfolio_config['api_key']
            api_secret = portfolio_config['api_secret']
            api_pass = portfolio_config['api_pass']

            api = CBAuthAPI(api_key, api_secret, api_pass)
            orders = api.getOrders()

            if len(orders) > 0:
                last_order = orders.iloc[-1:]
                last_buy_order = last_order[last_order.action == 'buy']
                last_buy_order = last_buy_order.reset_index(drop=True)

                if len(last_buy_order) > 0:
                    print (last_buy_order.to_string(index=False))

                    market = last_buy_order['market'].to_string(index=False).strip()
                    size = float(last_buy_order['size'].to_string(index=False).strip())
                    value = float(last_buy_order['value'].to_string(index=False).strip())
                    price = float(last_buy_order['price'].to_string(index=False).strip())
                    
                    api = CBPublicAPI()
                    ticker = api.getTicker(market)
                    current_value = ticker * size

                    gross_profit = current_value - value
                    net_profit = current_value - value - 2.99
                    margin = (current_value - value - 2.99) / current_value * 100

                    if isinstance(ticker, float): 
                        print ("\n", "       Current Price :", "{:.2f}".format(ticker))

                        print ("\n", "      Purchase Value :", "{:.2f}".format(value))
                        print (     "        Current Value :", "{:.2f}".format(current_value))

                        print ("\n", "        Gross Profit :", "{:.2f}".format(gross_profit))
                        print (     "           Net Profit :", "{:.2f}".format(net_profit))
                        print (     "               Margin :", str("{:.2f}".format(margin)) + '%')

                else:
                    print ('*** no active position open ***')
            
            print ("\n")

        #break

except IOError as err:
    print (err)
except Exception as err:
    print (err)