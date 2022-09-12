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
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
import pytz

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
sched = BlockingScheduler()
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
    print(r"""

  /$$$$$$   /$$                          /$$                                 /$$        /$$$$$$ 
 /$$__  $$ | $$                         | $$                               /$$$$       /$$$_  $$
| $$  \__//$$$$$$    /$$$$$$  /$$$$$$  /$$$$$$    /$$$$$$  /$$$$$$$       |_  $$      | $$$$\ $$
|  $$$$$$|_  $$_/   /$$__  $$|____  $$|_  $$_/   /$$__  $$| $$__  $$        | $$      | $$ $$ $$
 \____  $$ | $$    | $$  \__/ /$$$$$$$  | $$    | $$  \ $$| $$  \ $$        | $$      | $$\ $$$$
 /$$  \ $$ | $$ /$$| $$      /$$__  $$  | $$ /$$| $$  | $$| $$  | $$        | $$      | $$ \ $$$
|  $$$$$$/ |  $$$$/| $$     |  $$$$$$$  |  $$$$/|  $$$$$$/| $$  | $$       /$$$$$$ /$$|  $$$$$$/
 \______/   \___/  |__/      \_______/   \___/   \______/ |__/  |__/      |______/|__/ \______/ 
                                                                                                
                """)
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
    dt = datetime.now()
    for msg in messages:
        
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        headers = payload['headers']
        sender = ''

        if len(headers) > 16:
            if 'TradingView <noreply@tradingview.com>' in headers[17]['value'] and 'Trade' in headers[16]['value'] and 'sl' in headers[16]['value']:
                sender = 'TradingView <noreply@tradingview.com>'
                t1 = headers[1]['value'][91:93]
                t2 = str(dt)[11:13]
                t3 = int(t2) - int(t1)
                if sender == 'TradingView <noreply@tradingview.com>' and t3 == 9:
                    #print('2')
                    strBody = str(headers[16]['value'])
                    crypto = strBody[8:15]
                    tp = strBody[25:30]
                    sl = strBody[34:40]
                    message = '⏰ \nNouvelle prediction sur le ' + crypto + '! \nJe vous conseille de rentrer un trade en short (a la baisse) maintenant\n \n❎ Stop loss: ' + sl + '$\n✅ Take profit: ' + tp + '$ !\n\nBonne chance a tous \n🍀'
                    print(message)
                    telegramJob(message)
                else:
                    print('No prediction this hour')    

getEmails()
#sched.add_job(getEmails(), 'interval', seconds =600)

