#!/usr/bin/env python3
import os, base64, warnings, json
warnings.filterwarnings("ignore")
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

def get_credentials():
    token_data = json.loads(os.environ.get("GOOGLE_TOKEN"))
    token_data["client_id"] = os.environ.get("GOOGLE_CLIENT_ID")
    token_data["client_secret"] = os.environ.get("GOOGLE_CLIENT_SECRET")
    creds = Credentials.from_authorized_user_info(token_data)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

creds = get_credentials()
service = build('gmail', 'v1', credentials=creds)

body = """Hola mi amor,

Te amo mucho. ¡Mucha suerte en clases! Ya te quiero aquí conmigo. ❤️

Patricio"""

msg = MIMEText(body)
msg['To'] = 'renatav-gp@hotmail.com'
msg['From'] = 'pacotouss@gmail.com'
msg['Subject'] = '❤️ Te amo'

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
print(f"Correo enviado a Renata. ID: {result['id']}")
