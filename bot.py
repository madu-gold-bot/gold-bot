import requests, time, os

TELEGRAM_TOKEN = os.getenv("TOKEN", os.getenv("BOT_TOKEN"))
CHAT_ID = os.getenv("CHAT", os.getenv("CHANNEL_ID"))

def get_gold_price():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
        return float(r['price'])
    except:
        return None

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        r = requests.post(url, data=data, timeout=10)
        print(r.text)
    except: pass

print("GOLD BOT 15M - VPS STARTED")
price = get_gold_price()
if price:
    send_telegram(f"🤖 GOLD BOT STARTED (15M)\nPrice: ${price:.2f}")

last_price = price if price else 0

while True:
    p = get_gold_price()
    if not p:
        time.sleep(60)
        continue
    change = p - last_price
    if abs(change) >= 1.5 and last_price != 0:
        from datetime import datetime
        now = datetime.now().strftime("%I:%M %p")
        if change > 0:
            tp1 = p + 4
            tp2 = p + 8
            sl = p - 4
            msg = f"🚀 GOLD BUY SIGNAL 🚀\n\n💰 Now: ${p:.2f}\n📈 Move: +${change:.2f}\n⏰ {now}\n\nENTRY: BUY\nTP: ${tp1:.2f} / ${tp2:.2f}\nSL: ${sl:.2f}"
        else:
            tp1 = p - 4
            tp2 = p - 8
            sl = p + 4
            msg = f"📉 GOLD SELL SIGNAL 📉\n\n💰 Now: ${p:.2f}\n📉 Move: {change:.2f}\n⏰ {now}\n\nENTRY: SELL\nTP: ${tp1:.2f} / ${tp2:.2f}\nSL: ${sl:.2f}"
        send_telegram(msg)
        last_price = p
    elif last_price == 0:
        last_price = p
    time.sleep(60)
