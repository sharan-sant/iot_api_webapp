from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    # Bitcoin chart data (last 7 days)
    api_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': '7',
        'interval': 'daily'
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    # Extract timestamps and prices
    timestamps = [point[0] for point in data['prices']]
    prices = [round(point[1], 2) for point in data['prices']]

    # Convert timestamps to readable dates
    chart_labels = [datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%d') for ts in timestamps]
    chart_data = prices

    return render_template('index.html', chart_labels=chart_labels, chart_data=chart_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)

