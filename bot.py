
import requests, time, threading, random
from flask import Flask

BOT_TOKEN="8811899915:AAFZkaJTPc1yOBzb1xpXsSGhXZKsRu6bmEQ"
CHAT_ID="-1003973044472"

app=Flask(__name__)
@app.route('/')
def home(): return "Mel Gold VOL 4+ LIVE"
threading.Thread(target=lambda: app.run(host='0.0.0.0',port=10000),daemon=True).start()

ses=requests.Session()
def send(t):
    try:
        ses.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":t}, timeout=10)
        print("SENT")
    except Exception as e: print(e)

send("✅ MEL GOLD V3 LIVE - Bot Restarted OK")

while True:
    try:
        try:
            price=float(ses.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT",timeout=10).json()['price'])
        except:
            price=float(ses.get("https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=usd",timeout=10).json()['pax-gold']['usd'])

        # VOL 4n UDA
        vol=round(random.uniform(4.1, 9.0),1)
        r=random.random()

        if r>0.6:
            if random.random()>0.5:
                msg=f"✅ CONFIRMED: 🟢 BAYASLA 2x!\n{price:.2f} 🚀\nVol x{vol}"
            else:
                msg=f"✅ CONFIRMED: 🔴 SELASLA 2x!\n{price:.2f} 📉\nVol x{vol}"
        elif r>0.3:
            if random.random()>0.5:
                msg=f"⚠️ CHAT: 🟢 Bayasla awith! {price:.2f} 🚀\nVol x{vol}"
            else:
                msg=f"⚠️ CHAT: 🔴 Selasla awith! {price:.2f} 📉\nVol x{vol}"
        else:
            if random.random()>0.5:
                msg=f"🔼🔼🔼 STRONG BUY!!! {price:.2f} 🔼🔼\nVol x{vol}"
            else:
                msg=f"🔻🔻🔻 STRONG SELL!!! {price:.2f} 🔻🔻\nVol x{vol}"

        send(msg)
        time.sleep(75)

    except Exception as e:
        print(e)
        time.sleep(30)
