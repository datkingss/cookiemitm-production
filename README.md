# 🍪 CookieMITM - Production

**Hệ thống thu thập Cookie Trung Gian & Demo Session Hijacking**

Dự án đồ án tốt nghiệp - Xây dựng hệ thống proxy trung gian (MITM) để thu thập cookie và demo tấn công session hijacking trên môi trường production.

## ✨ Tính năng chính
- Trang web giả mạo (Facebook, Shopee, Gmail clone) deploy công khai
- MITM Proxy thu thập cookie realtime
- Dashboard quản lý & phân tích cookie
- Demo Session Hijacking trực tiếp
- Deploy trên cloud (Railway / Render)

## 📁 Cấu trúc dự án
- `fake-sites/` → Các trang web giả mạo
- `backend/` → FastAPI + PostgreSQL
- `proxy/` → mitmproxy addon
- `frontend/` → Dashboard
- `docker/` → Docker Compose

## 🚀 Cách chạy local
```bash
docker-compose up --build
