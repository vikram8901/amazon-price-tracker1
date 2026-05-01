import requests
from bs4 import BeautifulSoup
import time
import json
from plyer import notification

with open("settings.json", "r") as file:
    settings = json.load(file)

URL = settings["url"]
TARGET_PRICE = settings["budget"]
CHECK_INTERVAL = settings["remind-time"]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_product_details():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.select_one("#productTitle")
        price = soup.select_one(".a-price-whole")

        if not title or not price:
            print("Could not fetch product details.")
            return None, None

        title = title.get_text(strip=True)
        price = float(price.get_text(strip=True).replace(",", ""))

        return title, price

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def send_notification(title, price):
    notification.notify(
        title="Amazon Price Drop Alert!",
        message=f"{title}\nCurrent Price: ₹{price}",
        timeout=10
    )

def main():
    while True:
        title, price = get_product_details()

        if title and price:
            print(f"\nProduct: {title}")
            print(f"Current Price: ₹{price}")

            if price <= TARGET_PRICE:
                send_notification(title, price)
                print("Price dropped! Notification sent.")
                break

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
