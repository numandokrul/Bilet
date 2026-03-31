import requests
import time
import telebot

TOKEN = "8534777848:AAH67sCjDpeLtlaJ4jVFvmpYbQ3vfz3nEOY"
CHAT_ID = "877109239"
API_KEY = "1d5b54b893mshb8c4507e1871b29p1d6e2fjsn5184b8543c1d"

bot = telebot.TeleBot(TOKEN)
bot.send_message(CHAT_ID, "TEST MESAJI")


MAX_PRICE = MAX_PRICE = 4500  # TL

def get_price():
    url = "https://flights-scraper-real-time.p.rapidapi.com/flights/search-oneway"

    querystring = {
        "originSkyId": "SAW",
        "destinationSkyId": "EZS",
        "date": "2026-08-26",
        "adults": "1",
        "currency": "TRY",
        "market": "TR",
        "locale": "tr-TR"
    }

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "flights-scraper-real-time.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    try:
        data = response.json()

        #  EN UCUZ FİYATI BUL
        prices = []

        for item in data["data"]["itineraries"]:
            price = float(item["price"]["amount"])
            prices.append(price)

        if prices:
            return min(prices)
        else:
            return None

    except Exception as e:
        print("Hata:", e)
        return None


def check():
    last_sent = None

    while True:
        price = get_price()

        print("Fiyat:", price)

        if price:
          
          

            if price_tl <= MAX_PRICE and price != last_sent:
                bot.send_message(
                    CHAT_ID,
                    f"🔥 UCUZ UÇAK!\nSAW → Elazığ\n{int(price_tl)} TL"
                )
                last_sent = price

        time.sleep(60 * 30)


if __name__ == "__main__":
    check()