import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# 載入 .env 檔案中的環境變數
load_dotenv()

app = Flask(__name__)

# --- CORS 修正 ---
# 允許 GitHub Pages 的 Origin (https://kaibakuen.github.io) 存取 /api/* 端點
# 這是關鍵，確保前端的請求不會被拒絕。
CORS(app, resources={r"/api/*": {"origins": "https://kaibakuen.github.io"}}) 
# ---

# 載入所有 API 金鑰 (在 Cloud Run 環境變數中設定)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY") 
MOTC_APP_ID = os.getenv("MOTC_APP_ID")
MOTC_APP_KEY = os.getenv("MOTC_APP_KEY")

# API URL 常數
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
IMAGEN_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict"


# ----------------------------------------------------------------
# 1. AI 代理端點 (Gemini)
# ----------------------------------------------------------------
@app.route('/api/gemini-proxy', methods=['POST'])
def gemini_proxy():
    if not GEMINI_API_KEY:
        return jsonify({"error": "Gemini API Key not configured in environment."}), 500

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
        
        # 處理可能的 API 錯誤
        if response.status_code != 200 and "error" in response.json():
            error_msg = response.json().get('error', {}).get('message', 'Unknown Gemini API error')
            print(f"Gemini API Error: {error_msg}")
            return jsonify({"error": f"Gemini API 錯誤: {error_msg}"}), response.status_code
        
        return jsonify(response.json()), response.status_code

    except Exception as e:
        print(f"Error processing Gemini proxy request: {e}")
        return jsonify({"error": f"Internal server error: {e}"}), 500

# ----------------------------------------------------------------
# 2. MOTC 交通資訊查詢端點 (模擬)
# ----------------------------------------------------------------
@app.route('/api/motc-traffic', methods=['GET'])
def motc_traffic_query():
    if not MOTC_APP_ID or not MOTC_APP_KEY:
        return jsonify({"error": "MOTC API Keys not configured in environment."}), 500
        
    # 這裡返回模擬數據
    return jsonify({
        "success": True,
        "message": "MOTC API 認證成功，功能待實作。",
        "data": {
            "motc_status": "Keys Loaded"
        }
    })

# ----------------------------------------------------------------
# 3. IMAGEN 影像生成代理端點
# ----------------------------------------------------------------
@app.route('/api/generate-map-image', methods=['POST'])
def generate_map_image():
    if not GEMINI_API_KEY:
        return jsonify({"error": "Gemini API Key (required for Imagen) not configured."}), 500

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
            error_response = response.json()
            error_msg = error_response.get('error', {}).get('message', 'Unknown Image API error')
            print(f"Imagen API Error: {error_msg}")
            return jsonify({"error": f"Image generation failed: {error_msg}"}), 500

        # Extract base64 encoded image
        predictions = response.json().get('predictions', [])
        if not predictions or not predictions[0].get('bytesBase64Encoded'):
            return jsonify({"error": "Image generation returned no results."}), 500
            
        base64_data = predictions[0].get('bytesBase64Encoded')
        
        return jsonify({"base64_image": base64_data}), 200

    except Exception as e:
        print(f"Error processing Imagen proxy request: {e}")
        return jsonify({"error": f"Internal server error during image generation: {e}"}), 500


if __name__ == '__main__':
    # Cloud Run 啟動最佳實踐：從環境變數中取得 Port
    port = int(os.environ.get('PORT', 8080))
    # 運行在 0.0.0.0 讓 Cloud Run 可以正確存取
    app.run(debug=True, host='0.0.0.0', port=port)
