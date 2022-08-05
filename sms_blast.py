import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Loading environment variables from dotenv file
load_dotenv()


class SMS_Blast:
    """
    A class for SMS blast.

    ....

    Attributes
    ----------
    code: str
        The international dialing code of the recipients number used to format their numbers.

    Methods
    -------
    __format_phone_numbers(numbers: list)
        Returns a string of recipients phone numbers formatted with international dial code and joined
        by comma(,)
    """
    def __init__(self, code):
        self.code = code
    
    __url = "https://api.ebulksms.com:4433/sendsms?username={0}&apikey={1}&sender={2}&messagetext={3}&flash={4}&recipients={5}"


    def format_message(self, agent_number, message):
        split = agent_number.split(', ')
        pass


    def send_message(self, sender_id, limit, agent_numbers, msg, recipients):
        formatted_numbers = self.__format_phone_numbers(recipients)
        user_name, api_key, sender, message, recipients = self.__encode_values(sender_id, msg, formatted_numbers)

        formatted_url = self.__url.format(user_name,api_key,sender,message,0,recipients)

        try:
            response = requests.request("GET", formatted_url)

            return response.text

        except Exception as error:
            print(error)
            return error


    def __format_phone_numbers(self, numbers: list) -> str:
        # eliminating number with less than 11 digits
        num_list = [num for num in numbers if len(num) > 10]

        # Formatting numbers with international dialing code
        num_list = [num if num[:3]==self.code else (self.code + num[-9:] if len(num)==10 else "234" + num[-10:]) for num in num_list]
        
        formatted_phone_numbers = ",".join(num_list)

        return formatted_phone_numbers


    def __encode_values(self, sender_id, message, recipients):
        user_name = quote_plus(os.environ.get('USER_NAME'))
        api_key = quote_plus(os.environ.get('API_KEY'))
        recipients = quote_plus(recipients)
        sender = quote_plus(sender_id)
        message = quote_plus(message)

        return user_name, api_key, sender, message, recipients

