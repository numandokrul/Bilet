import requests
import time
import telebot
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(TOKEN)

MAX_PRICE = 4500


def get_best_flight(date):
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

        if not itineraries:
            print("❌ Uçuş yok:", date)
            return None

        best = None

        for item in itineraries:
            try:
                price = float(item["price"]["amount"])

                segment = item["sector"]["sectorSegments"][0]["segment"]

                airline = segment["carrier"]["name"]
                departure = segment["source"]["localTime"]
                arrival = segment["destination"]["localTime"]

                if best is None or price < best["price"]:
                    best = {
                        "price": price,
                        "airline": airline,
                        "departure": departure,
                        "arrival": arrival
                    }

            except Exception as e:
                print("Parse hata:", e)

        print("BEST:", best)
        return best

    except Exception as e:
        print("GENEL HATA:", e)
        return None


def check():
    last_sent = None

    dates = [
        "2026-08-23",
        "2026-08-28",
        "2026-08-29"
    ]

    while True:
        best_overall = None
        best_date = None

        for d in dates:
            flight = get_best_flight(d)

            if flight:
                print(f"{d}:", flight["price"], flight["airline"])

                if best_overall is None or flight["price"] < best_overall["price"]:
                    best_overall = flight
                    best_date = d

        if best_overall and best_overall["price"] <= MAX_PRICE:
            if last_sent != best_overall["price"]:
                bot.send_message(
                    CHAT_ID,
                    f"🔥 UCUZ UÇAK!\n"
                    f"Tarih: {best_date}\n"
                    f"Firma: {best_overall['airline']}\n"
                    f"Saat: {best_overall['departure']} - {best_overall['arrival']}\n"
                    f"Fiyat: {int(best_overall['price'])} TL"
                )
                last_sent = best_overall["price"]

        time.sleep(60 * 30)


if __name__ == "__main__":
    check()
