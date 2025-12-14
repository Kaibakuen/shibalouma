import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# 載入 .env 檔案中的環境變數
# ❗ 確保這個 .env 檔案在本地的 backend/ 資料夾裡，並且填寫了真實金鑰。
load_dotenv()

app = Flask(__name__)
# 啟用 CORS：這是關鍵，允許您的 GitHub Pages 網址呼叫本地伺服器
# ❗ 注意：當您在本地測試時，這個 origins 設定可以允許連線。
CORS(app, resources={r"/api/*": {"origins": "https://kaibakuen.github.io/shibalouma"}}) 

# 載入所有 API 金鑰 (正確地使用變數名稱來獲取值)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Google Maps Key
MOTC_APP_ID = os.getenv("MOTC_APP_ID")                  # MOTC App ID
MOTC_APP_KEY = os.getenv("MOTC_APP_KEY")                # MOTC App Key

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"

# ----------------------------------------------------------------
# AI 代理端點
# ----------------------------------------------------------------
@app.route('/api/gemini-proxy', methods=['POST'])
def gemini_proxy():
    if not GEMINI_API_KEY:
        # 如果金鑰沒設定，回傳錯誤訊息
        return jsonify({"error": "Gemini API Key not configured in environment (Check .env or deployment settings)."}), 500

    try:
        data = request.get_json()
        user_query = data.get('user_query')
        system_prompt = data.get('system_prompt')
        use_grounding = data.get('use_grounding', True)
        
        payload = {
            "contents": [{"parts": [{"text": user_query}]}],
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "tools": [{"google_search": {}}] if use_grounding else None
        }

        headers = { "Content-Type": "application/json" }
        
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload
        )
        
        return jsonify(response.json()), response.status_code

    except Exception as e:
        print(f"Error processing Gemini proxy request: {e}")
        return jsonify({"error": f"Internal server error: {e}"}), 500

# ----------------------------------------------------------------
# MOTC 交通資訊查詢端點 (待實作)
# ----------------------------------------------------------------
@app.route('/api/motc-traffic', methods=['GET'])
def motc_traffic_query():
    if not MOTC_APP_ID or not MOTC_APP_KEY:
        return jsonify({"error": "MOTC API Keys not configured in environment."}), 500
    
    return jsonify({
        "success": True,
        "message": "MOTC API 認證成功，功能待實作。",
        "data": {
            "motc_status": "Keys Loaded"
        }
    })

if __name__ == '__main__':
    # 在本地電腦上，我們使用 8080 端口運行
    print("Backend Proxy running on http://0.0.0.0:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)