
import requests, time, threading
from flask import Flask

BOT=8811899915:AAFUzVO-5eHhAQPuOyGCZr5MY0rsfLM-7hY
CHAT="-1003973044472"

app=Flask(__name__)
@app.route('/')
def home(): return "Bot Running 24/7"

def bot_loop():
 last=None
 while True:
  try:
   url="https://api.binance.com/api/v3/klines?symbol=PAXGUSDT&interval=5m&limit=30"
   closes=[float(c[4]) for c in requests.get(url).json()]
   def ema(d,p):
    k=2/(p+1); e=d[0]
    for x in d[1:]: e=x*k+e*(1-k)
    return e
   e9=ema(closes[-10:],9); e21=ema(closes,21)
   pe9=ema(closes[:-1][-10:],9); pe21=ema(closes[:-1],21)
   sig=None
   if pe9<=pe21 and e9>e21: sig="BUY"
   if pe9>=pe21 and e9<e21: sig="SELL"
   if sig and sig!=last:
    txt=f"GOLD SIGNAL\n{sig} CROSS\nPrice: {closes[-1]}\nEMA 9/21\nEducational Only"
    requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage",data={"chat_id":CHAT,"text":txt})
    last=sig
   time.sleep(60)
  except Exception as e:
   print(e); time.sleep(10)

threading.Thread(target=bot_loop,daemon=True).start()
app.run(host="0.0.0.0",port=10000)
