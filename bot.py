import requests
import time
import telebot
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(TOKEN)

MAX_PRICE = 4500  # TL


def get_price_for_date(date):
    url = "https://flights-scraper-real-time.p.rapidapi.com/flights/search-oneway"

    querystring = {
        "originSkyId": "SAW",
        "destinationSkyId": "EZS",
        "date": date,
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

    dates = [
        "2026-08-23",
        "2026-08-28",
        "2026-08-29"
    ]

    while True:
        best_price = None
        best_date = None

        for d in dates:
            price = get_price_for_date(d)
            print(f"{d} fiyat:", price)

            if price:
                if best_price is None or price < best_price:
                    best_price = price
                    best_date = d

        if best_price and best_price <= MAX_PRICE and best_price != last_sent:
            bot.send_message(
                CHAT_ID,
                f"🔥 UCUZ UÇAK!\nTarih: {best_date}\nSAW → Elazığ\n{int(best_price)} TL"
            )
            last_sent = best_price

        time.sleep(60 * 30)


if __name__ == "__main__":
    check()
