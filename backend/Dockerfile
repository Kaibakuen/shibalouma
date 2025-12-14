# 使用 Python 3.11 官方映像作為基礎

FROM python:3.11-slim

# 設定工作目錄

WORKDIR /app

# 將 requirements.txt 複製到容器中並安裝依賴

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 將專案中的所有檔案複製到容器中

COPY . .

# 應用程式預設監聽 8080 端口

ENV PORT 8080

# 設定啟動伺服器的命令

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
