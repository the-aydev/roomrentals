import os
from twilio.rest import Client


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def send_sms(user_code, number):
    message = client.messages.create(
        body=f'Hi! Your verification code is {user_code}',
        from_='+19892962604',
        to=f'{number}'
    )

    print(message.sid)
