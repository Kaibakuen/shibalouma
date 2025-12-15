<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>客途 AI 旅伴 - 浪漫台三線</title>
    <!-- 載入 Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- 載入 Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
        /* 使用 Inter 字體 */
        :root { font-family: 'Inter', sans-serif; }
        
        /* 核心主題色定義 */
        .color-primary { background-color: #103561; } /* 深藍色 */
        .color-secondary { background-color: #1a4270; } /* 稍淺的藍色 */
        .color-accent { background-color: #f59e0b; } /* 橙色 */
        .text-accent { color: #f59e0b; }
        
        body { 
            background-color: #0d284a; 
            min-height: 100vh;
        }

        /* --- 轉場動畫定義 --- */
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes fadeOut { from { opacity: 1; } to { opacity: 0; } }
        
        /* 隱藏警告區域，因為我們已經使用後端代理 */
        #risk-warning { display: none; }

        /* ------------------------ */
        /* SPLASH SCREEN 樣式 */
        /* ------------------------ */
        #splash-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: #103561; /* 深藍色背景 */
            color: white;
            z-index: 1000;
        }
        #splash-video-container {
            width: 90%;
            max-width: 300px;
            margin-bottom: 2rem;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        }
        #splash-video {
            display: block;
            width: 100%;
            height: auto;
        }
        
        /* ------------------------ */
        /* 主 APP 樣式 (聊天介面) */
        /* ------------------------ */
        #app-container {
            min-height: 100vh;
            display: none; /* 預設隱藏，等待Splash Screen結束 */
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }

        #chat-window {
            background-color: #ffffff;
            max-width: 1000px;
            width: 100%;
            height: 90vh; 
            max-height: 800px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
            overflow: hidden;
            display: flex;
            flex-direction: row; 
        }
        
        /* 側邊欄和吉祥物容器 */
        #sidebar {
            width: 300px;
            display: none; 
            padding: 2rem;
            color: white;
            flex-direction: column;
            justify-content: space-between;
        }

        /* 聊天主體 */
        #chat-main {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            background-color: #f7f7f7; 
        }
        
        /* 聊天內容區 */
        #messages {
            flex-grow: 1;
            padding: 1.5rem;
            overflow-y: auto;
            background-color: #f7f7f7;
        }

        /* 覆蓋訊息泡泡樣式 */
        .bot-message, .user-message {
            max-width: 85%;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            font-size: 0.95rem;
        }
        .bot-message {
            background-color: #e2e8f0; 
            color: #103561; 
            border-radius: 15px 15px 15px 5px;
        }
        .user-message {
            background-color: #fde68a; 
            color: #103561; 
            border-radius: 15px 15px 5px 15px;
        }
        .flex-card {
            border-radius: 12px;
            background-color: #ffffff;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        /* 響應式佈局調整 */
        @media (min-width: 768px) {
            #sidebar {
                display: flex;
            }
        }
        
        /* 吉祥物影片調整 */
        #mascot-video {
            width: 100%;
            height: auto;
            max-height: 250px; 
            object-fit: cover;
            border-radius: 8px;
        }
        /* 隱藏原生 video 控件 */
        #splash-video::-webkit-media-controls,
        #mascot-video::-webkit-media-controls { display: none !important; }
        #splash-video,
        #mascot-video { pointer-events: none; }

        /* 地圖模態視窗樣式 */
        #map-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            z-index: 2000;
            display: none;
            justify-content: center;
            align-items: center;
        }
        #map-container {
            width: 90%;
            max-width: 800px;
            height: 80%;
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }
        #map {
            width: 100%;
            height: calc(100% - 40px); /* 留出關閉按鈕空間 */
        }
    </style>
</head>
<body class="p-0 flex flex-col items-center justify-center min-h-screen">
    
    <!-- 1. SPLASH SCREEN (起始畫面) -->
    <div id="splash-screen">
        <h1 class="text-4xl font-extrabold mb-4 animate-pulse">客途 AI 旅伴</h1>
        <p class="text-lg opacity-80 mb-8">台三線客庄生態博物館</p>

        <div id="splash-video-container">
            <!-- 還原影片連結 -->
            <video id="splash-video" autoplay loop muted playsinline>
                <source src="asset/video/1213.mp4" type="video/mp4">
                您的瀏覽器不支援影片標籤。
            </video>
        </div>

        <button id="start-button" 
                class="color-accent hover:bg-amber-600 text-white text-xl font-bold px-8 py-3 rounded-full shadow-lg transition duration-300 transform hover:scale-105">
            <i data-lucide="play" class="w-5 h-5 inline-block mr-2"></i> 點我開始旅程
        </button>
    </div>

    <!-- 2. MAIN APPLICATION CONTAINER (主應用程式介面) -->
    <div id="app-container" class="w-full">
        <div id="chat-window">
            
            <!-- 側邊欄 (Sidebar) - 視覺與吉祥物 -->
            <div id="sidebar" class="color-primary p-6">
                <div>
                    <h2 class="text-2xl font-extrabold mb-4 border-b pb-2 border-white/50">小阿客 AI 旅伴</h2>
                    <p class="text-sm opacity-80 mb-6">台三線客庄生態博物館，專屬的個人化行程規劃服務。</p>
                    
                    <div class="mb-6">
                        <div class="font-semibold text-accent mb-2">您的 ID 資訊</div>
                        <div id="user-id-display" class="text-xs break-all bg-white/10 p-2 rounded-lg">
                            載入中...
                        </div>
                    </div>
                    
                    <!-- 警告區域：提醒金鑰風險 -->
                    <div id="risk-warning">
                        ❗ **警告：** 金鑰已直接公開在程式碼中，請勿用於實際應用。
                    </div>

                    <!-- API 狀態檢查區塊 -->
                    <div class="mt-6">
                        <div class="font-semibold text-accent mb-2">服務狀態</div>
                        <div id="api-status" class="text-xs space-y-1">
                            <!-- 狀態將由 JS 動態填入 -->
                            <p id="status-gemini"><i data-lucide="minus" class="w-4 h-4 mr-1 inline-block text-gray-400"></i> Gemini AI</p>
                            <p id="status-maps"><i data-lucide="minus" class="w-4 h-4 mr-1 inline-block text-gray-400"></i> Google Maps</p>
                            <p id="status-motc"><i data-lucide="minus" class="w-4 h-4 mr-1 inline-block text-gray-400"></i> MOTC 交通</p>
                        </div>
                    </div>
                </div>
                
                <!-- 還原影片連結 -->
                <div class="text-center">
                    <p class="text-xs opacity-70 mb-2">吉祥物：小阿客</p>
                    <video id="mascot-video" autoplay loop muted playsinline>
                        <source src="asset/video/1213.mp4" type="video/mp4">
                        您的瀏覽器不支援影片標籤。
                    </video>
                </div>
            </div>

            <!-- 聊天主體 (Chat Main) -->
            <div id="chat-main">
                <!-- Chat Header -->
                <div class="p-4 bg-white text-gray-800 shadow-md flex items-center justify-center border-b border-gray-200">
                    <h1 class="text-xl font-bold flex items-center">
                        <i data-lucide="route" class="w-5 h-5 mr-2 text-accent"></i> 客製化行程規劃
                    </h1>
                </div>

                <!-- Messages Container -->
                <div id="messages" class="space-y-4">
                    <!-- Initial Message Placeholder -->
                </div>

                <!-- Input Area (Rich Menu & Text Input Simulation) -->
                <div id="input-area" class="p-4 bg-white border-t border-gray-200">
                    <!-- 快速按鈕區 (Rich Menu Simulation) -->
                    <div id="rich-menu-sim" class="flex justify-center space-x-3 mb-4">
                        <button onclick="handleMessage('我想規劃行程')" class="bg-blue-700 hover:bg-blue-800 text-white text-xs px-4 py-2 rounded-full shadow-md transition duration-200 flex items-center">
                            <i data-lucide="map-pin" class="w-3 h-3 inline-block mr-1"></i> 直接規劃
                        </button>
                        <button onclick="handleMessage('重新測驗')" class="color-accent hover:bg-amber-600 text-white text-xs px-4 py-2 rounded-full shadow-md transition duration-200 flex items-center">
                            <i data-lucide="list-checks" class="w-3 h-3 inline-block mr-1"></i> 開始問卷
                        </button>
                        <a href="https://example.com/AR_App_Download" target="_blank" class="bg-gray-400 hover:bg-gray-500 text-white text-xs px-4 py-2 rounded-full shadow-md transition duration-200 flex items-center">
                            <i data-lucide="link" class="w-3 h-3 inline-block mr-1"></i> 外部連結
                        </a>
                    </div>
                    <!-- 文字輸入框 -->
                    <div class="flex">
                        <input type="text" id="user-input" placeholder="輸入需求，例如：新竹峨眉，戶外活動 或 什麼是客家擂茶?" class="flex-1 p-3 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-accent focus:border-accent focus:outline-none transition duration-150" onkeyup="if(event.key === 'Enter') sendMessage()">
                        <button onclick="sendMessage()" class="color-primary hover:bg-blue-800 text-white px-4 rounded-r-lg shadow-md transition duration-200">
                            <i data-lucide="send" class="w-5 h-5"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 3. MAP MODAL (地圖模態視窗) -->
    <div id="map-modal" style="display: none;">
        <div id="map-container">
            <button onclick="hideMap()" class="absolute top-2 right-2 z-30 bg-red-600 text-white p-2 rounded-full shadow-lg hover:bg-red-700 transition">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>
            <div id="map" class="w-full h-full"></div>
            <div id="map-title" class="absolute top-0 left-0 right-0 color-primary text-white p-2 text-center text-sm font-semibold z-20">地圖載入中...</div>
        </div>
    </div>


    <!-- 載入核心邏輯 (使用標準 script 標籤解決 lucide 錯誤) -->
    <script>
        
        // ----------------------------------------------------
        // ❗❗❗ 第 0 步：設定 API 連線 - 所有金鑰已移到前端 ❗❗❗
        // ----------------------------------------------------
        // [1] Gemini API 資訊
        const GEMINI_API_KEY = "AIzaSyCrY3D5a_PRNuyx_ymqH5AU7XlUogM6N2M";
        const GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent";
        
        // [2] Google Maps 金鑰
        const GOOGLE_MAPS_API_KEY = "AIzaSyDn4p7dNICj-iFjWEI1rn08FoWNEHHProo"; 
        
        // [3] MOTC 交通資訊
        const MOTC_APP_ID = "U1158028-99d98f63-dc86-480d";
        const MOTC_APP_KEY = "a523ea8a-7464-48ef-b589-3a4a0bfd1990";
        
        // 最終 API 終端點 (直接呼叫 Google API)
        const FINAL_GEMINI_ENDPOINT = `${GEMINI_API_BASE_URL}?key=${GEMINI_API_KEY}`;
        
        // --- 核心變數和函式定義 ---

        const messagesContainer = document.getElementById('messages');
        const userInput = document.getElementById('user-input');
        const userIdDisplay = document.getElementById('user-id-display');

        const PREFERENCE_DIMENSIONS = {
            "Culture": 0, "Outdoor": 0, "Pace": 0, "LowCarbon": 0,
            "Family": 0, "Accessibility": 0, "CultureDepth": 0,
            "Indoor": 0, "RiskAversion": 0
        };

        let currentPreferences = { ...PREFERENCE_DIMENSIONS }; 
        let currentQuizStep = 0; 
        let directionsService; 
        let directionsRenderer; 
        let isMapApiLoaded = false;
        
        // [Start] Local Storage Ops
        const loadStateFromLocalStorage = () => {
            try {
                const storedState = localStorage.getItem('hakka_quiz_state');
                if (storedState) {
                    const data = JSON.parse(storedState);
                    currentPreferences = data.preferences || { ...PREFERENCE_DIMENSIONS };
                    currentQuizStep = data.quiz_step || 0;
                    return true;
                }
            } catch (e) {
                console.error("Error loading state from localStorage:", e);
            }
            return false;
        };

        const saveStateToLocalStorage = () => {
            try {
                const stateToSave = {
                    preferences: currentPreferences,
                    quiz_step: currentQuizStep,
                    timestamp: new Date().toISOString()
                };
                localStorage.setItem('hakka_quiz_state', JSON.stringify(stateToSave));
            } catch (e) {
                console.error("Error saving state to localStorage:", e);
            }
        };

        const updatePreferenceVector = (valString) => {
            (valString || "").split(',').forEach(item => {
                if (!item) return;
                const matches = item.match(/([+-]\d+)([A-Za-z]+)/);
                if (matches && matches.length === 3) {
                    const val = parseInt(matches[1]);
                    const dim = matches[2];
                    if (dim in currentPreferences) {
                        currentPreferences[dim] += val;
                    }
                }
            });
        };
        // [End] Local Storage Ops
        
        // [Start] UI Helpers
        const addMessage = (type, contentHTML, isQuiz = false) => {
            const isBot = (type === 'bot' || type === 'quiz');
            const messageDiv = document.createElement('div');
            messageDiv.className = `flex ${isBot ? 'justify-start' : 'justify-end'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = `p-3 ${isBot ? 'bot-message' : 'user-message'}`; 

            if (isQuiz) {
                contentDiv.classList.add('flex-card', 'bg-white', 'p-4', 'shadow-lg', 'text-gray-800');
                contentDiv.classList.remove('p-3');
            } 

            if (isBot && !isQuiz) {
                contentDiv.innerHTML = `<i data-lucide="bot" class="w-4 h-4 mr-1 inline-block text-blue-900"></i> ${contentHTML}`;
            } else if (!isBot) {
                contentDiv.innerHTML = contentHTML;
            } else if (isQuiz) {
                contentDiv.innerHTML = contentHTML;
            }

            messageDiv.appendChild(contentDiv);
            messagesContainer.appendChild(messageDiv);
            
            if (typeof lucide !== 'undefined' && lucide.createIcons) {
                lucide.createIcons();
            }
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            return contentDiv;
        };
        // [End] UI Helpers

        // [Start] Quiz & Itinerary Data
        const HAKKA_ATTRACTIONS = [
            { id: 1, region: "桃園", name: "大溪老街 (Daxi Old Street)", theme: ["Culture", "Indoor", "Pace"], description: "充滿巴洛克式立面建築的歷史街區，適合室內文化探索與慢步調。", map_url: "https://maps.app.goo.gl/yQ9fQ7k7yJ6eLg9v9", lat: 24.8722, lng: 121.2882 },
            { id: 2, region: "新竹", name: "北埔老街/金廣福公館", theme: ["Culture", "CultureDepth", "Indoor"], description: "北台灣客家文化的中心，必嚐擂茶，適合文史愛好者深度探索。", map_url: "https://maps.maps.app.goo.gl/6E6oN2hV1r9XJz3f7", lat: 24.6946, lng: 121.0506 },
            { id: 3, region: "新竹", name: "峨眉湖/細茅埔吊橋", theme: ["Outdoor", "LowCarbon", "Pace"], description: "湖畔步道與生態景觀，適合戶外、騎單車的低碳慢活路線。", map_url: "https://maps.app.goo.gl/DkK8Z7yB7N8xT6rD7", lat: 24.6865, lng: 121.0425 },
            { id: 4, region: "苗栗", name: "獅頭山風景區", theme: ["Outdoor", "CultureDepth", "RiskAversion"], description: "健行步道與古道文化，是挑戰型的戶外登山健行首選。", map_url: "https://maps.app.goo.gl/yP7jG4Z1b6hC5rP9", lat: 24.6468, lng: 120.9702 },
            { id: 5, region: "苗栗", name: "南庄老街 (桂花巷)", theme: ["Culture", "Indoor", "Family"], description: "輕鬆逛街、品嚐客家小吃，具備親子友善設施。", map_url: "https://maps.app.goo.gl/wU2aD6yZ9k7qL5xK8", lat: 24.5902, lng: 121.0101 },
            { id: 6, region: "台中", name: "東勢客家文化園區 (自行車道)", theme: ["LowCarbon", "Outdoor", "Pace"], description: "舊火車站改建，結合鐵道文化與綠色廊道，是單車活動的最佳起點。", map_url: "https://maps.app.goo.gl/Gj8xN4bY5rE2pA3c6", lat: 24.2541, lng: 120.8351 }
        ];

        const QUIZ_QUESTIONS = {
            1: { "text": "Q1: 旅程規劃時，比起聊天，您更喜歡安靜做自己的事嗎？", "options": [{ label: "A: 是的，我需要時間獨自沉澱或思考", val: "+3Indoor,+2Pace,-1Outdoor" }, { label: "B: 否，我喜歡與旅伴討論，共同決定", val: "+3Outdoor,-1Indoor,-2Pace" }] },
            2: { "text": "Q2: 您覺得能睡飽，比早起趕行程、看美景更重要嗎？", "options": [{ label: "A: 是的，休息是旅行的重點", val: "+3Pace,+2Indoor,-2Outdoor" }, { label: "B: 否，我願意早起把握時間多玩一點", val: "-3Pace,+2Outdoor,+2RiskAversion" }] },
            3: { "text": "Q3: 在人多熱鬧的老街或聚會場所，您會感到活力充沛嗎？", "options": [{ label: "A: 是的，我享受社交和人群的熱鬧", val: "-3Indoor,+2Culture,-1Pace" }, { label: "B: 否，我更喜歡安靜的自然或歷史景點", val: "+3Indoor,+2Pace,-2Culture" }] },
            4: { "text": "Q4: 您對住宿環境有潔癖，或是在意舒適度嗎？", "options": [{ label: "A: 是的，住宿的品質會影響我的心情", val: "+3Indoor,+2RiskAversion,-1LowCarbon" }, { label: "B: 否，只要有基本功能，便宜即可", val: "-3Indoor,-2RiskAversion,+1LowCarbon" }] },
            5: { "text": "Q5: 您喜歡走路，長時間的徒步探索不是問題嗎？", "options": [{ label: "A: 是的，我喜歡用雙腳深度探索", val: "+4Outdoor,+3LowCarbon,+2CultureDepth" }, { label: "B: 否，我偏好搭乘交通工具或短程移動", val: "-3Outdoor,-2LowCarbon,+2Pace" }] },
            6: { "text": "Q6: 規劃行程時，您會先考量是否有兒童或長者友善設施嗎？", "options": [{ label: "A: 是的，所有人的舒適度是我的首要考量", val: "+4Family,+4Accessibility,+2RiskAversion" }, { label: "B: 否，我以景點的獨特性和個人興趣為主", val: "-3Family,-3Accessibility,-1RiskAversion" }] },
            7: { "text": "Q7: 旅程中遇到突發狀況，您傾向立即啟動備用方案，避免任何風險嗎？", "options": [{ label: "A: 是的，我討厭行程被打亂", val: "+4RiskAversion,+2Indoor,-2Pace" }, { label: "B: 否，我願意隨機應變，甚至接受意外的驚喜", val: "-4RiskAversion,+2Outdoor,+2Pace" }] },
            8: { "text": "Q8: 您會設定旅程預算並且實際控管，捨不得花太多錢享受美食嗎？", "options": [{ label: "A: 是的，控制預算比美食享受重要", val: "+3LowCarbon,-3Indoor" }, { label: "B: 否，我蠻捨得花錢享受美食的", val: "-3LowCarbon,+3Indoor" }] },
            9: { "text": "Q9: 哪種客庄體驗對您更有吸引力？", "options": [{ label: "A: 參觀客家宗祠，聽宗族遷徙的深度歷史", val: "+4CultureDepth,+3Culture" }, { label: "B: 採茶、農場體驗，親手接觸土地與自然", val: "+4Outdoor,+2LowCarbon" }] },
            10: { "text": "Q10: 您喜歡按照規劃好的行程走，不喜歡旅途中變動嗎？", "options": [{ label: "A: 是的，規劃好的路線最有效率", val: "-3Pace,-2RiskAversion,+2CultureDepth" }, { label: "B: 否，我喜歡彈性、即興，隨時改變方向", val: "+3Pace,+2RiskAversion,-2CultureDepth" }] },
        };
        const TOTAL_QUIZ_STEPS = Object.keys(QUIZ_QUESTIONS).length; 
        // [End] Quiz & Itinerary Data


        // [Start] Gemini API
        /**
         * 呼叫 Gemini API (使用 Canvas 內建的 API Key)
         * 修正點：切換為直接呼叫 Google Generative Language API
         */
        const callGeminiAPI = async (userQuery, systemPrompt, useGrounding = true) => {
            
            // 修正點：使用直接 API Payload 格式
            const payload = {
                contents: [{ parts: [{ text: userQuery }] }],
                systemInstruction: { parts: [{ text: systemPrompt }] },
                tools: useGrounding ? [{ "google_search": {} }] : undefined,
            };

            // 實作指數退避 (Exponential Backoff) 重試機制
            const MAX_RETRIES = 3;
            let lastError = null;

            for (let i = 0; i < MAX_RETRIES; i++) {
                try {
                    // 修正：直接呼叫 Canvas 可用的終端點，並使用硬編碼的 GEMINI_API_KEY
                    const response = await fetch(`${GEMINI_API_BASE_URL}?key=${GEMINI_API_KEY}`, { 
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (!response.ok) {
                        try {
                            const errorBody = await response.json();
                            throw new Error(`API 錯誤: ${response.status} - ${errorBody.error?.message || '未知錯誤碼。'}`);
                        } catch (e) {
                            throw new Error(`連線失敗 (狀態碼: ${response.status})。`);
                        }
                    }
                    
                    const result = await response.json();
                    const candidate = result.candidates?.[0];
                    const text = candidate?.content?.parts?.[0]?.text;
                    let sources = [];
                    
                    const groundingMetadata = candidate?.groundingMetadata;
                    if (groundingMetadata && groundingMetadata.groundingAttributions) {
                        sources = groundingMetadata.groundingAttributions.map(attr => ({ uri: attr.web?.uri, title: attr.web?.title }));
                    }
                    
                    return { text, sources };
                } catch (error) {
                    lastError = error;
                    
                    if (error instanceof TypeError) {
                        lastError = new Error(`網路連線失敗 (TypeError)：請確認網路或 API 終端點配置。`);
                    } else {
                        lastError = error;
                    }

                    if (i < MAX_RETRIES - 1) {
                        const delay = Math.pow(2, i) * 1000;
                        await new Promise(resolve => setTimeout(resolve, delay));
                    }
                }
            }
            throw lastError; // 拋出最後一次錯誤
        };

        const handleDeepDive = async (attractionName) => {
            addMessage('user', `✨ 請給我景點【${attractionName}】的深度解說。`);
            
            const loadingMessageDiv = addMessage('bot', `<i data-lucide="loader" class="w-4 h-4 mr-1 inline-block animate-spin text-blue-700"></i> 小阿客正在透過網路查詢【${attractionName}】的歷史文化背景...`);
            
            const systemPrompt = "你是一位專門提供台灣客庄歷史、文化和旅遊資訊的專家。請根據 Google Search 提供的資訊，為用戶生成一段約 150 字的深度解說，內容需包含歷史淵源、客家文化連結以及旅遊亮點。請使用繁體中文。";
            const userQuery = `景點名稱: ${attractionName}. 請詳細說明這個景點的歷史和客家文化意義。`;

            try {
                const { text, sources } = await callGeminiAPI(userQuery, systemPrompt, true);
                
                let sourceHTML = '';
                if (sources && sources.length > 0) {
                    sourceHTML = sources.map(s => 
                        `<a href="${s.uri}" target="_blank" class="text-xs text-blue-600 hover:underline block truncate" title="${s.title}">${s.title}</a>`
                    ).join('');
                    sourceHTML = `<div class="mt-2 pt-2 border-t border-gray-100"><div class="text-xs font-semibold text-gray-500">資訊來源:</div>${sourceHTML}</div>`;
                }

                const responseHTML = `
                    <div class="font-bold text-blue-900 mb-2">✨【${attractionName} 深度解說】</div>
                    <p class="text-sm text-gray-700">${text}</p>
                    ${sourceHTML}
                `;
                
                loadingMessageDiv.innerHTML = responseHTML; 
                if (typeof lucide !== 'undefined' && lucide.createIcons) { lucide.createIcons(); }

            } catch (error) {
                loadingMessageDiv.innerHTML = `<div class="text-red-600">抱歉，深度解說功能失敗。錯誤訊息: ${error.message}</div>`;
                console.error("Deep Dive Error:", error);
            }
        };

        const knowledgeBase = `
            以下是從政府資料庫中提取的客庄相關資訊（CSV 摘要）：
            - 客家美食認證：桃園市共有 20 家餐廳通過客家美食認證，提供正宗的粄條、客家小炒等。這些餐廳致力於保留客家飲食文化。
            - 優質旅宿：新竹市和苗栗縣有多家合法旅宿資料名冊，特別推薦 2020 桃園金牌好棧，具備高標準的服務和設施。
            - 文化資源：臺中市的客家文化園區和特定旅遊館提供豐富的文史展示，是深入了解客家拓墾歷史的好去處。
        `;

        const handleCultureQA = async (userQuery) => {
            // 處理一般文化問答，並連結到內建知識庫
            const loadingMessageDiv = addMessage('bot', `<i data-lucide="loader" class="w-4 h-4 mr-1 inline-block animate-spin text-blue-700"></i> 小阿客正在思考您的客庄文化問題...`);
            
            // 將本地數據庫內容注入 System Prompt
            const systemPrompt = `
                你是一位專門回答台灣客家文化、歷史、習俗和美食的專家。
                請參考 Google Search 提供的資訊，並優先考量以下本地知識庫的內容進行回答：
                --- 本地知識庫 ---
                ${knowledgeBase}
                ---
                請用清晰、友善的語氣回答用戶的提問。請使用繁體中文。
            `;
            
            try {
                const { text, sources } = await callGeminiAPI(userQuery, systemPrompt, true);
                
                let sourceHTML = '';
                if (sources && sources.length > 0) {
                    sourceHTML = sources.map(s => 
                        `<a href="${s.uri}" target="_blank" class="text-xs text-blue-600 hover:underline block truncate" title="${s.title}">${s.title}</a>`
                    ).join('');
                    sourceHTML = `<div class="mt-2 pt-2 border-t border-gray-100"><div class="text-xs font-semibold text-gray-500">資訊來源:</div>${sourceHTML}</div>`;
                }

                const responseHTML = `
                    <div class="font-bold text-blue-900 mb-2">💡 客庄文化小知識</div>
                    <p class="text-sm text-gray-700">${text}</p>
                    ${sourceHTML}
                `;
                
                loadingMessageDiv.innerHTML = responseHTML; 
                if (typeof lucide !== 'undefined' && lucide.createIcons) { lucide.createIcons(); }

            } catch (error) {
                loadingMessageDiv.innerHTML = `<div class="text-red-600">抱歉，文化問答功能失敗。錯誤訊息: ${error.message}</div>`;
                console.error("Culture QA Error:", error);
            }
        };
        // [End] Gemini API

        // [Start] Map Logic
        /**
         * 載入 Google Maps API，並初始化 Directions 服務。
         * 修正：改用 Promise 模式，確保非同步載入的穩定性。
         */
        const loadGoogleMapsApi = () => {
            return new Promise((resolve, reject) => {
                if (isMapApiLoaded) {
                    resolve();
                    return;
                }
                const mapsApiKey = GOOGLE_MAPS_API_KEY;

                // 修正點：放寬對 Canvas 預設金鑰的檢查，避免啟動錯誤
                if (mapsApiKey === "AIzaSyDn4p7dNICj-iFjWEI1rn08FoWNEHHProo" || !mapsApiKey) {
                    console.error("Google Maps API Key is missing or default. Maps functionality will be disabled.");
                    isMapApiLoaded = false;
                    resolve();
                    return;
                }

                const script = document.createElement('script');
                script.src = `https://maps.googleapis.com/maps/api/js?key=${mapsApiKey}&libraries=routes`;
                script.async = true;
                script.defer = true;

                script.onload = () => {
                    isMapApiLoaded = true;
                    // 確保 google.maps 存在
                    if (typeof google !== 'undefined' && google.maps.DirectionsService) {
                        directionsService = new google.maps.DirectionsService();
                        directionsRenderer = new google.maps.DirectionsRenderer({ suppressMarkers: true });
                        resolve();
                    } else {
                        isMapApiLoaded = false;
                        reject(new Error("Google Maps API loaded, but services not found."));
                    }
                };

                script.onerror = () => {
                    reject(new Error("無法載入 Google Maps API 腳本。請檢查金鑰。"));
                };

                document.head.appendChild(script);
            });
        };
        
        const showItineraryMap = async (itineraryDataString, mapTitle) => {
            const mapModal = document.getElementById('map-modal');
            const mapTitleElement = document.getElementById('map-title');
            const mapDiv = document.getElementById('map');
            
            mapModal.style.display = 'flex';
            mapTitleElement.textContent = `載入路線: ${mapTitle}...`;

            try {
                const itinerary = JSON.parse(itineraryDataString);
                
                if (itinerary.length < 2) {
                     mapTitleElement.textContent = `規劃失敗：至少需要兩個景點來繪製路線。`;
                     return;
                }
                
                // 使用修正後的 Promise 載入
                await loadGoogleMapsApi();

                if (!isMapApiLoaded || typeof google === 'undefined') {
                    mapTitleElement.textContent = `地圖載入失敗：Google Maps API 金鑰可能錯誤或未啟用。`;
                    return;
                }

                const origin = { lat: parseFloat(itinerary[0].lat), lng: parseFloat(itinerary[0].lng) };
                const destination = { lat: parseFloat(itinerary[itinerary.length - 1].lat), lng: parseFloat(itinerary[itinerary.length - 1].lng) };
                
                const waypoints = itinerary.slice(1, -1).map(item => ({
                    location: { lat: parseFloat(item.lat), lng: parseFloat(item.lng) },
                    stopover: true 
                }));

                const map = new google.maps.Map(mapDiv, {
                    zoom: 11,
                    center: origin, 
                    mapId: "DEMO_MAP_ID" 
                });
                directionsRenderer.setMap(map);

                // Start Marker (A)
                new google.maps.Marker({
                    position: origin,
                    map: map,
                    title: itinerary[0].name,
                    label: 'A',
                    icon: { url: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png' }
                });

                // End Marker (Z)
                new google.maps.Marker({
                    position: destination,
                    map: map,
                    title: itinerary[itinerary.length - 1].name,
                    label: 'Z',
                    icon: { url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png' }
                });

                directionsService.route({
                    origin: origin,
                    destination: destination,
                    waypoints: waypoints,
                    optimizeWaypoints: true, 
                    travelMode: google.maps.TravelMode.DRIVING 
                }, (response, status) => {
                    if (status === 'OK') {
                        directionsRenderer.setDirections(response);
                        mapTitleElement.textContent = `規劃路線: ${mapTitle}`;
                    } else {
                        mapTitleElement.textContent = `路線計算失敗: ${status}`;
                        console.error('Directions request failed due to ' + status);
                    }
                });

            } catch (error) {
                mapTitleElement.textContent = `地圖載入失敗: ${error.message}`;
                console.error("Google Maps failed to load or initialize:", error);
            }
        };
        
        const hideMap = () => {
            document.getElementById('map-modal').style.display = 'none';
        };
        // [End] Map Logic

        // [Start] Main Logic
        const createQuizMessage = (questionData, currentStep) => {
            const q = questionData.text;
            const options = questionData.options;
            
            let quizHTML = `
                <div class="text-xs text-gray-500 mb-2">客途 AI 旅伴 - 旅遊偏好問卷 (第 ${currentStep}/${TOTAL_QUIZ_STEPS} 題)</div>
                <div class="text-lg font-bold text-blue-900 mb-3">${q}</div>
                <div class="space-y-2">
            `;

            options.forEach(option => {
                const nextStep = currentStep + 1;
                const postbackData = `action=next_quiz&step=${nextStep}&val=${option.val}`;
                
                quizHTML += `
                    <button onclick="handlePostback('${postbackData}')" 
                            class="w-full text-left p-3 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-lg text-sm transition duration-150 text-gray-800">
                        ${option.label}
                    </button>
                `;
            });

            quizHTML += `</div>`;
            
            addMessage('quiz', quizHTML, true);
        };

        const createItineraryCard = (itineraryJson) => {
            let itineraryItemsHTML = '';
            itineraryJson.itinerary.forEach((item, index) => {
                itineraryItemsHTML += `
                    <div class="py-2 border-b border-gray-100 last:border-b-0">
                        <div class="flex items-center text-sm font-semibold text-gray-700 mb-1">
                            <i data-lucide="clock" class="w-4 h-4 mr-2 text-amber-500"></i>
                            ${item.time} - ${item.name}
                        </div>
                        <p class="text-xs text-gray-500 pl-6">${item.description}</p>
                        <a href="${item.location_url}" target="_blank" class="text-xs text-blue-600 hover:text-blue-800 transition duration-150 pl-6 underline flex items-center mt-1">
                            <i data-lucide="map-pin" class="w-3 h-3 mr-1"></i> Google 地圖
                        </a>
                        <!-- 新增：Gemini 深度解說按鈕 -->
                        <button onclick="handleDeepDive('${item.name}')" class="mt-2 ml-6 text-xs text-white bg-blue-500 hover:bg-blue-600 px-2 py-1 rounded transition duration-150">
                            ✨ 景點深度解說
                        </button>
                    </div>
                `;
            });
            
            // 處理 JSON 格式，以便傳遞給 showItineraryMap 函數
            const itineraryDataString = JSON.stringify(itineraryJson.itinerary.map(item => ({
                name: item.name,
                lat: item.lat,
                lng: item.lng
            })));
            const mapTitle = itineraryJson.title;


            const cardHTML = `
                <div class="flex-card w-full max-w-sm text-gray-800">
                    <div class="p-3 color-primary text-white rounded-t-xl">
                        <div class="text-xl font-bold">${itineraryJson.title}</div>
                        <div class="text-xs opacity-80 mt-1">主題: ${itineraryJson.theme}</div>
                    </div>
                    
                    <div class="p-4 space-y-3">
                        <div class="border-b pb-3">
                            <div class="text-xs font-semibold text-blue-900 mb-1">小阿客推薦理由:</div>
                            <p class="text-sm">${itineraryJson.recommendation_reason}</p>
                        </div>
                        
                        <div class="text-sm font-bold mt-3">【詳細行程 - 台三線客庄】</div>
                        ${itineraryItemsHTML}

                        <div class="text-right text-xs text-blue-600 font-medium pt-2">
                            低碳估算（參考值）: ${itineraryJson.carbon_footprint_estimate}
                        </div>
                    </div>

                    <div class="flex flex-col p-3 border-t bg-gray-50 space-y-2">
                        <!-- 地圖按鈕 (呼叫新的路線繪製功能) -->
                        <button onclick="showItineraryMap('${itineraryDataString.replace(/'/g, "\\'")}', '${mapTitle}')" class="w-full text-center py-2 bg-green-500 hover:bg-green-600 text-white text-sm font-semibold rounded-lg transition duration-200 shadow-md">
                            <i data-lucide="map" class="w-4 h-4 inline-block mr-1"></i> 查看完整路線地圖
                        </button>
                        <!-- 雨天備案按鈕 -->
                        <button onclick="handlePostback('action=get_rain_plan')" class="w-full text-center py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 text-sm font-semibold rounded-lg transition duration-200">
                            <i data-lucide="umbrella" class="w-4 h-4 inline-block mr-1"></i> 雨天備案
                        </button>
                    </div>
                </div>
            `;
            addMessage('bot', cardHTML, true);
        };
        
        const generatePersonalityMessage = async (finalPrefs) => {
            const score = (dim) => finalPrefs[dim] || 0;

            let mainPersonality = ""; 
            let traitDescription = ""; 
            let itineraryFocus = ""; 
            
            const outdoorScore = score('Outdoor') - score('Indoor');
            const paceScore = score('Pace') * 0.5 - (score('CultureDepth') * 0.5 + score('RiskAversion') * 0.5); 
            const focusScore = score('CultureDepth') * 2 + score('Culture');
            
            if (focusScore > 8 && outdoorScore > 0) {
                mainPersonality = "精緻探索家 (The Cultured Explorer)";
                traitDescription = "您的基因：**內斂、規劃、知識享受、探索**。您重視旅程的知識性與效率，喜歡深入挖掘文化，並願意花費時間與精力去探索獨特景點。";
                itineraryFocus = "【精緻探索家】您需要結合**歷史古蹟深度導覽**與**高質量戶外體驗**。您的行程應包含明確的學習目標和高效率的移動，專注於質量而非數量。";
            } else if (outdoorScore < -4 && score('Pace') > 4) {
                mainPersonality = "悠活度假客 (The Relaxed Retreat)";
                traitDescription = "您的基因：**隨和、悠閒、物質享受、內斂**。您追求無壓力的放鬆與舒適度，住宿與美食的品質對您很重要。";
                itineraryFocus = "【悠活度假客】您應選擇主打**高品質客庄旅宿**、**在地客家慢食**、**室內手作體驗**。您的旅行哲學是『慢下來，享受當下』。";
            } else if (outdoorScore > 4 && paceScore < -2) {
                mainPersonality = "行動拓荒者 (The Action Pioneer)";
                traitDescription = "您的基因：**外向、緊湊、效率、開拓**。您擁有高強度的行動力，追求在有限的時間內走訪最多的戶外景點，行程通常高效且充滿挑戰性。";
                itineraryFocus = "【行動拓荒者】您需要緊湊且高強度的行程。建議行程：**挑戰型山區健行**、**長距離單車騎行**，將台三線的自然景點一網打盡。";
            } else {
                mainPersonality = "平和優遊家 (The Harmonious Wanderer)";
                traitDescription = "您的基因：**隨和、平衡、共享、無爭**。您希望旅程平順、舒適，樂於配合旅伴的需求。重視低風險、親子/長者友善的環境。";
                itineraryFocus = "【平和優遊家】您適合選擇**交通便利、配套設施完善**的景點（如大型客家文化園區、易達老街），確保行程流暢且所有旅伴都能舒適參與。";
            }
            
            let finalMessageContent = `
                <div class="p-3 w-full">
                    <div class="text-xl font-bold text-blue-900 border-b-2 border-blue-900 pb-2 mb-3 text-center">您的旅型人格揭曉！</div>
                    <div class="text-3xl font-extrabold text-amber-600 mb-2 text-center">${mainPersonality}</div>
                    <div class="text-sm text-gray-700 font-medium mb-4 text-center">${traitDescription}</div>
                    
                    <div class="mt-4 pt-3 border-t border-gray-100">
                        <div class="text-sm font-semibold text-blue-900 mb-1">小阿客的客製化行程建議：</div>
                        <p class="text-sm text-gray-600">${itineraryFocus}</p>
                        <p class="mt-3 text-xs text-blue-600">現在請輸入您的旅遊需求 (例如：『新竹峨眉，戶外活動』 或 『想去苗栗南庄，慢活主題』)，小阿客會立即為您規劃**最客製化**的台三線客庄行程！</p>
                    </div>
                </div>
            `;
            
            addMessage('quiz', finalMessageContent, true);
        };
        
        const generateHakkaItinerary = (query, prefs) => {
            // 這個函式目前在客戶端模擬行程生成的回應。在實際應用中，這個邏輯會被發送到後端，由 Gemini 根據 prefs 和 query 動態生成。
            const score = (dim) => prefs[dim] || 0;
            const isOutdoor = score('Outdoor') > score('Indoor');
            const isPace = score('Pace') > 0;
            const isCultureDepth = score('CultureDepth') > 0;

            const regionMatch = query.includes('新竹') ? '新竹' : query.includes('苗栗') ? '苗栗' : '桃園';
            
            let filteredAttractions = HAKKA_ATTRACTIONS.filter(a => a.region === regionMatch);
            
            if (isOutdoor) {
                filteredAttractions = filteredAttractions.filter(a => a.theme.includes('Outdoor'));
            } else if (isCultureDepth) {
                filteredAttractions = filteredAttractions.filter(a => a.theme.includes('CultureDepth'));
            }
            if (filteredAttractions.length < 2) {
                 filteredAttractions = HAKKA_ATTRACTIONS.filter(a => a.region === regionMatch);
            }

            const itinerary = [
                {
                    time: "09:00",
                    name: filteredAttractions[0].name,
                    description: isPace ? "慢活啟動，享受早晨的寧靜。" : "快速抵達並開始深度導覽。",
                    location_url: filteredAttractions[0].map_url,
                    lat: filteredAttractions[0].lat,
                    lng: filteredAttractions[0].lng,
                },
                {
                    time: "12:00",
                    name: "客家在地美食 (午餐)",
                    description: "推薦您品嚐傳統擂茶或粄條。",
                    location_url: "https://maps.app.goo.gl/g6zXJ4r5eQ7c3B9q7", // 模擬美食地點
                    lat: 24.6940, lng: 121.0500,
                },
                {
                    time: "14:00",
                    name: filteredAttractions[filteredAttractions.length - 1].name,
                    description: isCultureDepth ? "下午進行文化體驗，如手作 DIY 或參觀宗祠。" : "輕鬆騎行或散步於戶外美景。",
                    location_url: filteredAttractions[filteredAttractions.length - 1].map_url,
                    lat: filteredAttractions[filteredAttractions.length - 1].lat,
                    lng: filteredAttractions[filteredAttractions.length - 1].lng,
                },
            ];

            const theme = isPace ? "慢活悠遊" : "高效探索";
            
            return {
                title: `${regionMatch} 客庄一日遊：${theme} 主題`,
                theme: theme,
                recommendation_reason: `根據您的 **${generatePersonality(prefs).mainPersonality}** 人格，我們專注於 ${isCultureDepth ? '深度文化體驗' : '自然環境與戶外休閒'}，行程節奏 ${isPace ? '舒適緩慢' : '緊湊且高效'}。`,
                carbon_footprint_estimate: "低碳中高 (參考值)",
                itinerary: itinerary
            };
        };

        const generatePersonality = (finalPrefs) => {
            const score = (dim) => finalPrefs[dim] || 0;
            const outdoorScore = score('Outdoor') - score('Indoor');
            const focusScore = score('CultureDepth') * 2 + score('Culture');
            
            if (focusScore > 8 && outdoorScore > 0) return { mainPersonality: "精緻探索家" };
            if (outdoorScore < -4 && score('Pace') > 4) return { mainPersonality: "悠活度假客" };
            if (outdoorScore > 4) return { mainPersonality: "行動拓荒者" };
            return { mainPersonality: "平和優遊家" };
        };

        // [End] Main Logic

        // [Start] Event Handlers
        const handlePostback = async (data) => {
            const params = new URLSearchParams(data);
            const action = params.get('action');

            if (action === 'next_quiz') {
                const nextStep = parseInt(params.get('step'));
                const valString = params.get('val');
                
                updatePreferenceVector(valString);
                currentQuizStep = nextStep; 

                if (nextStep <= TOTAL_QUIZ_STEPS) {
                    const quizData = QUIZ_QUESTIONS[nextStep];
                    createQuizMessage(quizData, nextStep);
                    saveStateToLocalStorage();
                } else {
                    currentQuizStep = TOTAL_QUIZ_STEPS;
                    saveStateToLocalStorage();
                    await generatePersonalityMessage(currentPreferences);
                }

            } else if (action === 'get_rain_plan') {
                addMessage('bot', '好的，小阿客收到雨天備案請求！若遇下雨，建議將戶外步道改為參觀附近的**客家文化會館**或**室內DIY體驗**（如米食製作）。');
            }
        };

        const handleMessage = async (text) => {
            
            addMessage('user', text);

            const isRestart = text === "重新測驗" || text === "開始問卷";
            const isFinished = currentQuizStep >= TOTAL_QUIZ_STEPS;
            const isPlanning = text.includes('規劃行程') || text.includes('行程') || text.includes('顯示結果');
            
            if (isRestart) {
                currentQuizStep = 0;
                currentPreferences = { ...PREFERENCE_DIMENSIONS };
                saveStateToLocalStorage();
            }

            if (currentQuizStep === 0) {
                if (isPlanning && !isRestart) {
                    addMessage('bot', "小阿客了解您的需求！請先點擊「開始問卷」按鈕，完成 **10 題客庄旅遊問卷**，以獲得最客製化的行程建議。");
                    return; 
                }
                const quizData = QUIZ_QUESTIONS[1];
                createQuizMessage(quizData, 1);
                currentQuizStep = 1;
                saveStateToLocalStorage();
                return;
            }

            if (isPlanning && isFinished) {
                try {
                    const loadingMessageDiv = addMessage('bot', `<i data-lucide="loader" class="w-4 h-4 mr-1 inline-block animate-spin text-blue-700"></i> 小阿客正在根據您的旅型人格和「${text}」規劃**台三線客庄行程**中... 請稍候。`);
                    
                    // Call proxy to generate itinerary (simulated on client for now)
                    // 實際應用中，這個延遲將被實際的 callGeminiAPI(itinerary generation)取代
                    setTimeout(() => {
                        // 這裡不需要檢查 AI Service Ready，因為這是客戶端模擬的行程
                        const itineraryJson = generateHakkaItinerary(text, currentPreferences);
                        // 移除載入中的訊息，並顯示行程卡
                        messagesContainer.removeChild(loadingMessageDiv.parentElement);
                        createItineraryCard(itineraryJson);
                    }, 1500);

                } catch (e) {
                    addMessage('bot', `對不起，行程規劃系統出現錯誤: ${e.message}`);
                    console.error("行程規劃錯誤:", e);
                }
            } else if (isFinished || (currentQuizStep > 0 && !isPlanning)) {
                // 這是處理一般文化問答的區塊
                if (text.length > 5 && !text.includes('顯示結果')) {
                     await handleCultureQA(text);
                } else if (!isFinished) {
                     addMessage('bot', `請先回答目前的第 ${currentQuizStep} 題，才能繼續喔！`);
                }
            }
        };

        const sendMessage = () => {
            const text = userInput.value.trim();
            if (text) {
                handleMessage(text);
                userInput.value = ''; 
            }
        };
        // [End] Event Handlers

        // [Start] App Initialization
        const generateAnonUserId = () => {
            return 'anon_' + Math.random().toString(36).substring(2, 15);
        };
        
        const startApp = () => {
            const splash = document.getElementById('splash-screen');
            const app = document.getElementById('app-container');
            
            splash.style.animation = 'fadeOut 0.5s ease-in forwards';
            
            setTimeout(() => {
                splash.style.display = 'none';
                app.style.display = 'flex';
                app.style.animation = 'fadeIn 0.5s ease-out';
                
                // 檢查是否已完成問卷
                let initialBotMessage = `您好，我是您的客途 AI 旅伴 — **小阿客**！<br>
                                         我們將探索台三線（浪漫客庄大道）的獨特魅力。<br>`;
                
                if (currentQuizStep >= TOTAL_QUIZ_STEPS) {
                    initialBotMessage += `歡迎回來！您已完成問卷，現在請輸入您的旅遊需求或文化問題。`;
                } else if (currentQuizStep > 0) {
                    initialBotMessage += `您上次停在第 ${currentQuizStep} 題。請點擊「開始問卷」繼續完成。`;
                } else {
                    initialBotMessage += `為了給您最貼心的行程建議，請先點擊下方「開始問卷」。`;
                }
                
                addMessage('bot', initialBotMessage);
                
                userIdDisplay.innerHTML = generateAnonUserId(); 
                displayApiKeyStatus(); 
                
                if (currentQuizStep >= TOTAL_QUIZ_STEPS) {
                    setTimeout(async () => {
                          await generatePersonalityMessage(currentPreferences);
                    }, 500);
                } else {
                    setTimeout(() => {
                        const quizStartButton = `
                            <div class="w-full text-center">
                                <button onclick="handleMessage('重新測驗')" class="color-accent hover:bg-amber-600 text-white px-4 py-2 rounded-lg text-sm transition duration-200 shadow-md">
                                    點我開始問卷！
                                </button>
                            </div>
                        `;
                        addMessage('quiz', quizStartButton, true);
                    }, 500);
                }
            }, 500); 
        };
        
        const displayApiKeyStatus = () => {
            // 檢查 API 金鑰是否已設定
            const isGeminiSet = GEMINI_API_KEY && GEMINI_API_KEY.length > 5;
            const isMapsSet = GOOGLE_MAPS_API_KEY && GOOGLE_MAPS_API_KEY.length > 5;
            const isMotcSet = MOTC_APP_ID && MOTC_APP_KEY;

            const updateStatus = (id, isConnected, name) => {
                const element = document.getElementById(id);
                if (!element) return;

                if (isConnected) {
                     element.innerHTML = `<i data-lucide="check-circle" class="w-4 h-4 mr-1 inline-block text-green-500"></i> ${name} (已連線)`;
                } else {
                     element.innerHTML = `<i data-lucide="x-circle" class="w-4 h-4 mr-1 inline-block text-red-500"></i> ${name} (未連線或需設定)`;
                }
            };

            updateStatus('status-gemini', isGeminiSet, 'Gemini AI');
            updateStatus('status-maps', isMapsSet, 'Google Maps');
            updateStatus('status-motc', isMotcSet, 'MOTC 交通');
            
            if (typeof lucide !== 'undefined' && lucide.createIcons) { lucide.createIcons(); }
        };

        // 綁定全域函式
        window.handleMessage = handleMessage;
        window.handlePostback = handlePostback;
        window.sendMessage = sendMessage;
        window.handleDeepDive = handleDeepDive; 
        window.startApp = startApp; 
        window.showItineraryMap = showItineraryMap; 
        window.hideMap = hideMap;


        // --- 9. 網頁載入初始化 ---
        
        document.addEventListener('DOMContentLoaded', () => {
            
            loadStateFromLocalStorage();

            document.getElementById('start-button').addEventListener('click', startApp);

            if (typeof lucide !== 'undefined' && lucide.createIcons) {
                lucide.createIcons();
            }
            
            displayApiKeyStatus();
        });

    </script>
</body>
</html>
