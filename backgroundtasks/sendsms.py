
import africastalking
from app.config import settings
africastalking.initialize(settings.africas_talking_username, settings.africas_talking_api_key)
sms = africastalking.SMS

def sendmessage(number: str, message:str):
   recipients = [number]
   try:
    response = sms.send(message, recipients)
    return response
   except Exception as e:
        print(f"Error: {e}")
        return None