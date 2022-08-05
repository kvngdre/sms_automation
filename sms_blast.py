import os
import math
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
    __format_message(agent_number: str, message: str)
        Returns a string of recipients phone numbers formatted with international dial code and joined
        by comma(,)
    """

    def __init__(self, code):
        self.code = code

    __url = "https://api.ebulksms.com:4433/sendsms?username={0}&apikey={1}&sender={2}&messagetext={3}&flash={4}&recipients={5}"

    def format_message(self, agent_number: str, message: str):
        agent_number = agent_number.strip()
        split_numbers = agent_number.split(", ")

        return message.format(split_numbers[0])

    def send_message(self, sender_id: str, limit, agent_numbers, msg: str, recipients):
        formatted_numbers_list = self.__format_phone_numbers(limit, recipients)
        agent_numbers = agent_numbers.split(", ")
        
        for agent, number_list in zip(agent_numbers, formatted_numbers_list):
            formatted_numbers = ",".join(number_list)
            

            user_name, api_key, sender, message, recipients = self.__encode_values(
                sender_id, msg.format(agent), formatted_numbers
            )

            formatted_url = self.__url.format(
                user_name, api_key, sender, message, 0, recipients
            )

            try:
                response = requests.request("GET", formatted_url)

            except Exception as error:
                print(error)
                return error

        return response.text

    def __format_phone_numbers(self, limit: int, numbers: list) -> str:
        # eliminating number with less than 11 digits
        num_list = [num for num in numbers if len(num) > 10]

        # Formatting numbers with international dialing code
        num_list = [
            num
            if num[:3] == self.code
            else (self.code + num[-9:] if len(num) == 10 else "234" + num[-10:])
            for num in num_list
        ]

        min = 0
        max = limit
        result = []

        for _ in range(math.ceil(len(num_list) / limit)):
            result.append(num_list[min:max])
            min = max
            max += limit

        print("result====", len(result))

        return result

    def __encode_values(self, sender_id, message, recipients):
        user_name = quote_plus(os.environ.get("USER_NAME"))
        api_key = quote_plus(os.environ.get("API_KEY"))
        recipients = quote_plus(recipients)
        sender = quote_plus(sender_id)
        message = quote_plus(message)

        return user_name, api_key, sender, message, recipients
