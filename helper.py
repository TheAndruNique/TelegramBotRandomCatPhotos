import json
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import logging


load_dotenv()

BOT_LANGUAGE = os.getenv("BOT_LANGUAGE")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

required_values = ["TELEGRAM_BOT_TOKEN"]
missing_values = [value for value in required_values if os.environ.get(value) is None]
if len(missing_values) > 0:
      logging.error(f"The following environment values are missing in your .env: {', '.join(missing_values)}")

with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

def localized_text(key, bot_language):
    try:
        text = translations[bot_language][key]
        if type(text) == list:
            return random.choice(text)
        else:
            return text
    except KeyError:
        logging.warning(f"No translation available for bot_language code '{bot_language}' and key '{key}'")
        if key in translations["en"]:
            text = translations["en"][key]
            if type(text) == list:
                return random.choice(text)
            else:
                return text
        else:
            logging.warning(f"No english definition found for key '{key}' in translations.json")
            return key
        
def random_cat_photo():
    try:
        result = requests.get("https://mimimi.ru/random")
        soup = BeautifulSoup(result.text, "html.parser")
        cat_url_img = soup.find_all("img")[1].get("src")
        return cat_url_img
    except:
        return None
        