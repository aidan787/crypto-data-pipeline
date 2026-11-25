# Crypto Data Pipeline

An n8n workflow and a small Flask app that pull the top cryptocurrency prices from the CoinMarketCap API, clean the data, and log it to Google Sheets on a schedule.

## How it works

```
Schedule Trigger -> HTTP Request -> HTTP Request1 -> Append row in sheet
                    (CoinMarketCap)  (Flask /process)  (Google Sheets)
```

1. **Schedule Trigger** starts the workflow on a timer.
2. **HTTP Request** calls the CoinMarketCap API and fetches the latest listings (top 10 coins).
3. **HTTP Request1** sends that raw data to the Flask app at `/process`.
4. **Flask app** keeps only the fields that matter and returns a clean list: `name`, `symbol`, `price`, `market_cap`, and `timestamp`.
5. **Append row in sheet** writes each coin as a new row in Google Sheets, so you build a price history over time.

Why a separate Flask app? n8n's built-in Python Code node runs in a sandbox and can't make HTTP requests or use normal Python libraries, so the data processing lives in its own small service that n8n calls.

## What you need

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with n8n running in it
- [Python 3](https://www.python.org/downloads/)
- A free [CoinMarketCap API key](https://coinmarketcap.com/api/)
- A Google account (for Google Sheets)
- A Google Sheet with these column headers in row 1: `market_cap`, `name`, `price`, `symbol`, `timestamp`

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/aidan787/n8n-crypto-pipeline.git
cd n8n-crypto-pipeline
```

### 2. Start the Flask app

```bash
pip install -r requirements.txt
python app.py
```

Leave this window open. The app listens on port `5000`. It must listen on all interfaces (`host="0.0.0.0"`), not just `127.0.0.1`, or n8n running in Docker can't reach it.

> TODO (Aidan): explain what `pipeline.py` does and whether people need to run it.

### 3. Import the workflow

1. Open n8n (usually `http://localhost:5678`) and create a new workflow.
2. Click the three dots menu, then **Import from File**.
3. Choose `workflows/data-pipeline-workflow.json`.

The workflow file has no logins, keys, or personal info, so you need to add your own next.

### 4. Add your own keys and accounts

- **HTTP Request:** replace `YOUR_COINMARKETCAP_API_KEY` in the `X-CMC_PRO_API_KEY` header with your key.
- **Append row in sheet:** connect your own Google Sheets credential, then replace `YOUR_GOOGLE_SHEET_ID` with your spreadsheet's ID. It's the long string in the sheet's URL between `/d/` and `/edit`.

### 5. Run it

Click **Execute workflow** to test. Then set how often it should run in the **Schedule Trigger** and publish the workflow.

## Troubleshooting

- **"The service refused the connection" on HTTP Request1:** the Flask app isn't running, or it's only listening on `127.0.0.1`. Start it and make sure it uses `host="0.0.0.0"`.
- **404 Not Found on the first HTTP Request:** check that the CoinMarketCap URL ends in `/listings/latest`.
- **Sheets node shows a warning:** connect your Google credential and set your sheet ID (step 4).

## Notes

- `host.docker.internal` is how n8n, running inside Docker Desktop, reaches an app running on your own computer.
- Never commit your real API key. Keep it only inside your own n8n.
