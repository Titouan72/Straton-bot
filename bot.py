# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
def telegramJob(value):
    api_id = '9337267'
    api_hash = '6596d2e9a28d688929762bc7af6727ec'
    message = value
    phone = '+33640062336'
    client = TelegramClient('session', api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    try:
        for dialog in client.iter_dialogs():
            if not dialog.is_group and dialog.is_channel:
                if 'Ai' == dialog.title:
                    id = dialog.id
        client.send_message(id, message)
    except Exception as e:
        print(e);
    client.disconnect()

def getEmails():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # Check if it exists
    if os.path.exists('token.pickle'):

        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # request a list of all the messages
    result = service.users().messages().list(userId='me').execute()

    result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        headers = payload['headers']
        sender = ''
        body = ''

        #print('Subject', headers[16]['value'])
        #print('time', headers[1]['value'])
        #print('from', headers[17]['value'])
        if 'TradingView <noreply@tradingview.com>' in headers[17]['value'] and 'Trade' in headers[16]['value']:
            sender = 'TradingView <noreply@tradingview.com>'
            body = base64.b64decode(payload['body']['data'])

        if sender == 'TradingView <noreply@tradingview.com>':
            print("From: ", sender)
            print("Message: ", body)
            # DO SOME CHANGE FOR OTHER CRYPTO THAN BTC
            strBody = str(body)
            crypto = strBody[2: 8]
            tp = strBody[24: 29]
            sl = strBody[37: 42]
            message = '📈 Nouvelle prediction sur le ' + crypto + '! je vous conseille de rentrer un trade en short (a la baisse) maintenant\n Stop loss: ' + sl + '\n Take profit: ' + tp + ' !\n\n Bonne chance a tous 🍀'
            #print(message)
            
            telegramJob(message)

getEmails()
