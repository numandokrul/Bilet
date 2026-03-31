import requests
import time
import telebot
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(TOKEN)


def get_prices(date):
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
        itineraries = data.get("data", {}).get("itineraries", [])

        results = []

        for item in itineraries:
            try:
                price = float(item["price"]["amount"])

                segment = item["sector"]["sectorSegments"][0]["segment"]
                airline = segment["carrier"]["name"]

                results.append((airline, price))

            except:
                pass

        return results

    except:
        return []


def check():
    dates = [
        "2026-08-23",
        "2026-08-28",
        "2026-08-29"
    ]

    while True:
        message = "✈️ GÜNCEL UÇAK FİYATLARI\n\n"

        for d in dates:
            flights = get_prices(d)

            if flights:
                message += f"📅 {d}\n"

                for airline, price in flights[:3]:  # ilk 3 göster
                    message += f"{airline} → {int(price)} TL\n"

                message += "\n"
            else:
                message += f"{d} → veri yok\n\n"

        bot.send_message(CHAT_ID, message)

        time.sleep(60 * 30)


if __name__ == "__main__":
    check()
