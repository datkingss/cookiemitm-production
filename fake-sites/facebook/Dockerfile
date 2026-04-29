FROM python:3.11-slim

WORKDIR /app

# Copy requirements trước để cache layer
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]