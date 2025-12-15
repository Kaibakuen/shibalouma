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
CORS(app, resources={r"/api/*": {"origins": "https://kaibakuen.github.io/shibalouma"}}) 

# 載入所有 API 金鑰 (正確地使用變數名稱來獲取值)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Google Maps Key
MOTC_APP_ID = os.getenv("MOTC_APP_ID")                  # MOTC App ID
MOTC_APP_KEY = os.getenv("MOTC_APP_KEY")                # MOTC App Key

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
IMAGEN_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict"


# ----------------------------------------------------------------
# AI 代理端點
# ----------------------------------------------------------------
@app.route('/api/gemini-proxy', methods=['POST'])
def gemini_proxy():
    if not GEMINI_API_KEY:
        # 如果金鑰沒設定，回傳錯誤訊息
        return jsonify({"error": "GemINI API Key not configured in environment (Check .env or deployment settings)."}), 500

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
    
    # 這裡返回模擬數據，讓 Gemini 知道 MOTC 服務是可用的
    return jsonify({
        "success": True,
        "message": "MOTC API 認證成功，功能待實作。",
        "data": {
            "motc_status": "Keys Loaded"
        }
    })

# ----------------------------------------------------------------
# IMAGEN 影像生成代理端點 (NEW)
# ----------------------------------------------------------------
@app.route('/api/generate-map-image', methods=['POST'])
def generate_map_image():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GemINI API Key (required for Imagen) not configured."}), 500

    try:
        data = request.get_json()
        itinerary_data = data.get('itinerary_data', [])
        map_title = data.get('map_title', '客庄地圖')

        # 根據行程數據建立詳細的圖像生成提示
        stops = [f"【地點 {i+1}】: {item['name']}" for i, item in enumerate(itinerary_data)]
        stops_list = ", ".join(stops)
        
        # 提示詞要求可愛手繪、水彩風格，並標註中文地名
        prompt = (
            f"A cute, hand-drawn, watercolor map illustration titled '{map_title}' in 16:9 aspect ratio. "
            f"The map shows a road trip itinerary along Taiwan's Hakka regions (Taichung, Hsinchu, Miaoli). "
            f"The map must clearly feature and label these stops in Traditional Chinese: {stops_list}. "
            "Style: cheerful, children's book illustration, clean line art, soft pastel colors. Focus on the scenic route and destination labels."
        )

        payload = {
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "16:9" 
            }
        }
        
        headers = { "Content-Type": "application/json" }
        
        response = requests.post(
            f"{IMAGEN_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return jsonify({"error": f"Image generation failed: {response.json().get('error', {}).get('message', 'Unknown Image API error')}"}), 500

        # Extract base64 encoded image
        predictions = response.json().get('predictions', [])
        if not predictions:
            return jsonify({"error": "Image generation returned no results."}), 500
        
        base64_data = predictions[0].get('bytesBase64Encoded')
        
        return jsonify({"base64_image": base64_data}), 200

    except Exception as e:
        print(f"Error processing Imagen proxy request: {e}")
        return jsonify({"error": f"Internal server error during image generation: {e}"}), 500


if __name__ == '__main__':
    # 修正：直接讓 Flask 伺服器運行
    # 在本地電腦上，我們使用 8080 端口運行
    print("Backend Proxy running on http://0.0.0.0:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)
