from flask import Flask, request, jsonify
import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/process', methods=['POST'])
def process_coins():
    try:
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

    except KeyError as e:
        logging.error(f"Missing field: {e}")
        raise
    except ValueError as e:
        logging.error(f"Bad Number: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)




    