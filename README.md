# What is it

For now it downloades current listing prices for cryptocurrencies from Coinmarketcap API  and updates Google Sheets document


## How to make it run
Create `config.py` file:

```
COINMARKETCAP_API_KEY = ''
COINMARKETCAP_HOST = "https://pro-api.coinmarketcap.com/"
QUOTES_URL='v1/cryptocurrency/quotes/latest?symbol='
DOC_ID=""
CRYPTO_RATE_RANGE="A1:A3"
```

Get Google OAuth2 credentials.json for Google Sheets API + Google Drive API + Google Docs API

Run `python rates-togsheets.py` with Python 3.7+
