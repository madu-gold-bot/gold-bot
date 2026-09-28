import requests, time, os

TELEGRAM_TOKEN = os.getenv("TOKEN", "8811899915:AAEhV4YBg1McSaRSp5i9We_A0R9DJ34f0")
CHAT_ID = os.getenv("CHAT", "-1003973044472")

def get_gold_price():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
        return float(r['price'])
    except: return None

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=data, timeout=10).json()
        print(r)
        return r.get("ok")
    except: return False

print("GOLD BOT 15M - VPS STARTED")
price = get_gold_price()
if price:
    send_telegram(f"🤖 *GOLD BOT STARTED (15M) - 24H VPS*\nPrice: ${price:.2f}")

last = time.time()
base = price
while True:
    p = get_gold_price()
    if not p:
        time.sleep(2)
        continue
    if time.time() - last >= 900:
        ch = p - base
        d = "BUY 🟢" if ch>=0 else "SELL 🔴"
        send_telegram(f"*{d} 15M*\nPrice: ${p:.2f}\nChange: {ch:+.2f}")
        last = time.time()
        base = p
    print(f"${p:.2f}")
    time.sleep(3)
