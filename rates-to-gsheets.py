import requests
import json
import config as conf


import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_crypto_prices(currencies="BTC,ETH,DOGE"):
    crypto_quotes = requests.request("GET", conf.COINMARKETCAP_HOST+conf.QUOTES_URL +
                                     currencies, headers={'X-CMC_PRO_API_KEY': conf.COINMARKETCAP_API_KEY}).json()
    return {c: crypto_quotes['data'][c]['quote']['USD']['price'] for c in currencies.split(",")}


def get_google_sheets_client():
    SCOPES = ['https://www.googleapis.com/auth/documents',
              'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()


if __name__ == "__main__":
    ghandler = get_google_sheets_client()
    crypto_prices = get_crypto_prices()
    new_values = {'values': [
        [crypto_prices['BTC']],
        [crypto_prices['ETH']],
        [crypto_prices['DOGE']],
    ]
    }

    values = ghandler.values().update(spreadsheetId=conf.DOC_ID, range=conf.CRYPTO_RATE_RANGE,
                                      valueInputOption="USER_ENTERED", body=new_values).execute()
