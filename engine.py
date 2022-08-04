import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

url = "https://api.ebulksms.com:4433/sendsms?username={0}&apikey={1}&sender={2}&messagetext={3}&flash={4}&recipients={5}"


def format_phone_numbers(numbers):
    num_list = [num for num in numbers if len(num) > 10]

    num_list = [num if num[:3]=="234" else ("234" + num[-9:] if len(num)==10 else "234" + num[-10:]) for num in num_list]
    
    result = ",".join(num_list)

    return result


def encode_values(sender_id, message, recipients):
    user_name = quote_plus(os.environ.get('USER_NAME'))
    api_key = quote_plus(os.environ.get('API_KEY'))
    recipients = quote_plus(recipients)
    sender = quote_plus(sender_id)
    message = quote_plus(message)

    return user_name, api_key, sender, message, recipients


def send_message(sender_id, msg, recipients):
    formatted_numbers = format_phone_numbers(recipients)
    user_name, api_key, sender, message, recipients = encode_values(sender_id, msg, formatted_numbers)

    print(user_name, api_key)

    formatted_url = url.format(user_name,api_key,sender,message,0,recipients)
    print(formatted_url)

    try:
        response = requests.request("GET", formatted_url)

        return response.text

    except Exception as error:
        print(error)
        return error

