from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_coins():
    data = request.get_json(force=True)
    coins = data['data']

    results = []
    for coin in coins:
        results.append({
            'name': coin['name'],
            'symbol': coin['symbol'],
            'price': coin['quote']['USD']['price'],
            'market_cap': coin['quote']['USD']['market_cap'],
            'timestamp': datetime.datetime.now().isoformat()
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000)