import json
from datetime import datetime

import requests


def trend(Y):
    N = len(Y)
    X = range(N)
    Sx = Sy = Sx2 = Sy2 = Sxy = 0.0
    for x, y in zip(X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sx2 = Sx2 + x * x
        Sy2 = Sy2 + y * y
        Sxy = Sxy + x * y
    a = (Sxy * N - Sy * Sx) / (Sx2 * N - Sx * Sx)

    return "DOWN" if a < 0 else "UP"


def yahoo_stock_download(company_symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"

    querystring = {"symbols": company_symbol}

    headers = {
        'x-rapidapi-key': "3c911debf5msh936c29fae5611d7p15ea6cjsn4c4a987aaf33",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)
    result = data['quoteResponse']['result'][0]
    stock_data = dict(regular_price=result['regularMarketPrice'],
                      change=result['regularMarketChange'],
                      change_percentages=result['regularMarketChangePercent'],
                      download_time=datetime.now())
    return stock_data


def historical_data(company_symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-historical-data"

    querystring = {"symbol": company_symbol}

    headers = {
        'x-rapidapi-key': "3c911debf5msh936c29fae5611d7p15ea6cjsn4c4a987aaf33",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    prices = data['prices']
    hist_data = {}
    dates_list = []
    values_list = []

    for i in range(len(prices)):
        if 'adjclose' not in prices[i]:
            continue
        dates_list.append(datetime.fromtimestamp(prices[i]['date']).strftime('%Y-%m-%d'))
        values_list.append(prices[i]['adjclose'])
    hist_data['date'] = dates_list
    hist_data['adjclose price'] = values_list
    return hist_data
