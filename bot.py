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

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# get your api_id, api_hash, token
# from telegram as described above
def findChannelID(client: TelegramClient, channelTitle):
    for dialog in client.iter_dialogs():
        if not dialog.is_group and dialog.is_channel:
            if channelTitle == dialog.title:
                return dialog.id
def findChannelEntity(client: TelegramClient, channelTitle):
    channelID = findChannelID(client, channelTitle)
    channelEntity=client.get_entity(channelID)

    return channelEntity
def telegramJob():
    
    api_id = '9337267'
    api_hash = '6596d2e9a28d688929762bc7af6727ec'
    token = 'bot token'
    message = "Working..."
    channel = '1982970708'
    channelEntity = findChannelEntity(TelegramClient, 'Ai')
 # your phone number
    phone = '+33640062336'
    client = TelegramClient('session', api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
  
        client.send_code_request(phone)
     
    # signing in the client
        client.sign_in(phone, input('Enter the code: '))
    try:
        #client(ImportChatInviteRequest(channel))
    # receiver user_id and access_hash, use
    # my user_id and access_hash for reference
        receiver = InputPeerUser('user_id', 'user_hash')
        send_as = 'peepoo ai'
    # sending message using telegram client
        client.send_message(channelEntity, 'hello to myself')
    except Exception as e:
     
    # there may be many error coming in while like peer
    # error, wrong access_hash, flood_error, etc
        print(e);
 
# disconnecting the telegram session
    client.disconnect()

def getEmails():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
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

    # We can also pass maxResults to get any number of emails. Like this:
    result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')

    # messages is a list of dictionaries where each dictionary contains a message id.

    # iterate through all the messages
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        # Use try-except to avoid any Errors
            # Get value of 'payload' from dictionary 'txt'
        payload = txt['payload']
        
        headers = payload['headers']
        sender = ''
        body = ''
        
        if 'cryptohawk.ai' in headers[14]['value']:
            sender = 'cryptohawk.ai'
            # here parse the string with the data I want 
            # get the time if its 10 minutes ago max
            body = base64.b64decode(payload['body']['data'][100:300])
        #for d in headers:
        #    if d['name'] == 'Subject':
        #        subject = d['value']
        #    if d['name'] == 'From':
        #        sender = d['value']

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
        #parts = payload.get('parts')[0]
        #data = parts['body']['data']
        #data = data.replace("-","+").replace("_","/")
        
        #decoded_data = 'grosse pute' #base64.b64decode(data)
            # Now, the data obtained is in lxml. So, we will parse
            # it with BeautifulSoup library
        #soup = BeautifulSoup(decoded_data , "lxml")
        #print('test', parts)
        #body = soup.body()

        if sender == 'cryptohawk.ai':
            print("From: ", sender)
            print("Message: ", body)
            print('\n')


#getEmails()
telegramJob()