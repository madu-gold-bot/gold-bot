import requests, time, threading
from flask import Flask

BOT="8811899915:AAFU2VO-5eHhAQPuOyGCZr5MYOrsfLM-7hY"
CHAT="-1003973044472"

app=Flask(__name__)
@app.route('/')
def home(): return "Bot Running 24/7 - MEL GOLD V3 LIVE"

def bot_loop():
    last=None
    closes=[]
    SR=[4050,4100,4150,4180,4200,4220,4250,4280,4300,4320,4350]
    def ema(d,p):
        k=2/(p+1); e=d[0]
        for x in d[1:]: e=x*k+e*(1-k)
        return e
    def get_sr(p):
        for lvl in SR:
            if abs(p-lvl)<20: return lvl
        return None
    # Start message
    try:
        requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage", data={"chat_id": CHAT, "text": "MEL GOLD V3 LIVE - Bot Started on Render 24/7"})
    except: pass
    while True:
        try:
            r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=usd", timeout=15).json()
            price=float(r['pax-gold']['usd'])
            closes.append(price)
            if len(closes)>100: closes=closes[-100:]
            if len(closes)<60:
                print(f"Collecting {len(closes)}/60 Price {price}")
                time.sleep(30)
                continue
            e9=ema(closes[-20:],9); e21=ema(closes[-30:],21); e50=ema(closes[-60:],50)
            print(f"Price {price:.2f}")
            sig=None
            sr=get_sr(price)
            if e9>e21 and e21>e50 and price>e9 and sr:
                sig=f"BUY + SR\nGOLD {price:.2f}\nSR {sr}\nEMA Bull"
            elif e9<e21 and e21<e50 and price<e9 and sr:
                sig=f"SELL + SR\nGOLD {price:.2f}\nSR {sr}\nEMA Bear"
            if sig and sig!=last:
                requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage", data={"chat_id": CHAT, "text": sig})
                last=sig
            time.sleep(30)
        except Exception as e:
            print(e); time.sleep(60)

threading.Thread(target=bot_loop,daemon=True).start()
app.run(host="0.0.0.0",port=10000)
