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

body = """Hola Patricio,

Recuerda que tienes pendiente enseñarle a Enrique el reporte de VOX hoy.

¡Es URGENTE! No lo dejes pasar.

Saludos,
Tu asistente"""

msg = MIMEText(body)
msg['To'] = 'patotouss@gmail.com'
msg['From'] = 'patotouss@gmail.com'
msg['Subject'] = '🚨 URGENTE: Enseñarle a Enrique el reporte de VOX hoy'

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
print(f"Correo enviado. ID: {result['id']}")
