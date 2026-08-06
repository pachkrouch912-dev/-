from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str
    opponent_name: str = "Gemini ជើងខ្លាំង"

@app.post("/api/gemini-chat")
async def gemini_chat(req: ChatRequest):
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return {"reply": "ហាសហា! ខ្ញុំត្រៀមខ្លួនរួចជាស្រេចហើយ ចាំមើលរឿងអស្ចារ្យលើក្ដារអុកនេះ!"}
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"អ្នកគឺជាគូប្រកួតអុកខ្មែរដ៏កំប្លែង ឌឺដងបន្តិច ប៉ុន្តែរួសរាយ និងស្រស់ស្រាយ។ អ្នកលេងបាននិយាយមកកាន់អ្នកថា: '{req.message}'។ សូមតបមកវិញជាភាសាខ្មែរខ្លីៗ ប្រកបដោយភាពកំប្លែង ស្វាហាប់ និងរស់រវើកក្នុងនាមជាគូប្រកួតអុក。"
        response = model.generate_content(prompt)
        return {"reply": response.text.strip()}
    except Exception as e:
        return {"reply": "អូ៎ អ៊ីនធឺណិតរាងទាក់បន្តិចហើយ ប៉ុន្តែទឹកមុខខ្ញុំនៅតែញញឹមហៅគូប្រកួតលេងដដែល!"}

@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "ok"}

@app.get("/manifest.json")
async def get_manifest():
    return JSONResponse({
        "name": "អុកខ្មែរអនឡាញ - WebRTC & Gemini",
        "short_name": "អុកខ្មែរ",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a0f18",
        "theme_color": "#1b2838",
        "description": "ហ្គេមអុកខ្មែរអនឡាញ ជាមួយ WebRTC Voice Call និង Gemini AI",
        "id": "OukkhmerWebRTC",
        "icons": [
            {
                "src": "https://dummyimage.com/192x192/1b2838/ffffff.png&text=Ouk",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "https://dummyimage.com/512x512/1b2838/ffffff.png&text=Ouk",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

@app.get("/sw.js")
async def get_sw():
    sw_code = """
    self.addEventListener('install', (event) => { self.skipWaiting(); });
    self.addEventListener('activate', (event) => { return self.clients.claim(); });
    self.addEventListener('fetch', (event) => {
        event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
    });
    """
    return PlainTextResponse(sw_code, media_type="application/javascript")

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>អុកខ្មែរអនឡាញ - WebRTC Voice & AI</title>
    
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#1b2838">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: radial-gradient(circle at center, #1b2838, #0a0f18);
            text-align: center; margin: 0; padding: 2px; color: #fff; 
            height: 100vh; height: 100dvh; overflow: hidden; 
            display: flex; flex-direction: column; justify-content: space-between; align-items: center;
        }

        .bg-chess {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            overflow: hidden; z-index: 0; pointer-events: none; opacity: 0.15;
        }
        .floating-piece {
            position: absolute; font-size: 30px; animation: floatUp 8s infinite linear;
        }
        @keyframes floatUp {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            50% { opacity: 1; }
            100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
        }

        .container { 
            position: relative; z-index: 1; width: 100%; max-width: 420px; 
            height: 100%; display: flex; flex-direction: column; justify-content: space-between; 
            padding: 4px;
        }
        
        .header-row {
            display: flex; align-items: center; justify-content: space-between;
            width: 100%; margin: 4px 0; position: relative; z-index: 30;
        }

        h1 { 
            color: #f1c40f; text-shadow: 0 0 10px rgba(241, 196, 15, 0.7);
            font-size: 11px; margin: 0; letter-spacing: 0.2px; flex-grow: 1; text-align: center;
        }

        .profile-dropdown-container {
            position: relative; display: inline-block; text-align: left;
        }

        .user-logo-btn {
            width: 32px; height: 32px; background: rgba(15, 25, 35, 0.95);
            border-radius: 50%; border: 1px solid rgba(241, 196, 15, 0.6);
            display: flex; align-items: center; justify-content: center;
            font-size: 15px; cursor: pointer; color: #f1c40f;
            box-shadow: 0 2px 8px rgba(0,0,0,0.5); transition: 0.2s;
        }
        .user-logo-btn:hover { background: rgba(30, 45, 65, 0.95); border-color: #f1c40f; transform: scale(1.05); }

        .dropdown-menu {
            position: absolute; top: 120%; left: 0; background: #1b2838;
            border: 1px solid rgba(241, 196, 15, 0.4); border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.8); width: 180px; display: none;
            flex-direction: column; overflow: hidden; z-index: 100;
        }
        .dropdown-menu.show { display: flex; }
        
        .dropdown-header-info {
            padding: 10px; background: rgba(241, 196, 15, 0.1);
            border-bottom: 1px solid rgba(255,255,255,0.1); text-align: center;
        }
        .dropdown-username { font-size: 12px; font-weight: bold; color: #f1c40f; margin-bottom: 2px; }
        .dropdown-points { font-size: 10px; color: #ddd; }

        .dropdown-item {
            padding: 8px 12px; font-size: 11px; color: #fff; text-decoration: none;
            display: flex; align-items: center; gap: 6px; cursor: pointer; transition: background 0.2s;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .dropdown-item:hover { background: rgba(241, 196, 15, 0.15); color: #f1c40f; }
        .dropdown-item.logout { color: #e74c3c; border-bottom: none; }
        .dropdown-item.logout:hover { background: rgba(231, 76, 60, 0.15); color: #e74c3c; }

        .clean-menu-layout {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            backdrop-filter: none !important;
            padding: 0 !important;
            margin: auto 0 !important;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            max-height: 94dvh;
            overflow-y: visible;
        }

        .game-clean-layout {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            backdrop-filter: none !important;
            padding: 0 !important;
            margin: 0 !important;
            height: 100% !important;
            justify-content: space-between !important;
        }

        input {
            padding: 7px; font-size: 12px; border: 2px solid #34495e; border-radius: 8px;
            margin: 3px 0; width: 100%; background: rgba(0, 0, 0, 0.6);
            color: #fff; text-align: center; outline: none; transition: 0.3s;
        }
        input:focus { border-color: #f1c40f; box-shadow: 0 0 8px rgba(241,196,15,0.5); }

        .menu-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; width: 100%; margin: 4px 0;
        }
        .menu-box-btn {
            background: rgba(20, 30, 45, 0.95); border: 1px solid rgba(241, 196, 15, 0.3);
            border-radius: 12px; padding: 10px 6px; display: flex; flex-direction: column;
            align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5); color: #fff; text-decoration: none;
        }
        .menu-box-btn:hover { transform: translateY(-2px); border-color: #f1c40f; background: rgba(30, 45, 65, 0.95); }
        .menu-icon { font-size: 22px; margin-bottom: 4px; }
        .menu-label { font-size: 11px; font-weight: bold; text-align: center; line-height: 1.2; }

        .btn-gold-box { border-color: #f1c40f; background: linear-gradient(to bottom, rgba(241,196,15,0.2), rgba(212,172,13,0.35)); }
        .btn-green-box { border-color: #2ecc71; background: linear-gradient(to bottom, rgba(46,204,113,0.2), rgba(39,174,96,0.35)); }
        .btn-blue-box { border-color: #3498db; background: linear-gradient(to bottom, rgba(52,152,219,0.2), rgba(41,128,185,0.35)); }
        .full-width-box { grid-column: span 2; display: flex; flex-direction: row; gap: 6px; align-items: center; padding: 6px 10px; }
        .full-width-box input { margin: 0; flex-grow: 1; }

        button {
            padding: 8px 12px; font-size: 12px; font-weight: 800; text-transform: uppercase;
            color: white; border: none; border-radius: 20px; cursor: pointer; 
            margin: 2px 0; width: 100%; letter-spacing: 0.5px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4); transition: all 0.2s ease;
        }
        button:hover { filter: brightness(1.15); }
        .btn-green { background: linear-gradient(to bottom, #2ecc71, #27ae60); border: 1px solid #1e8449; }
        .btn-blue { background: linear-gradient(to bottom, #3498db, #2980b9); border: 1px solid #1f618d; }
        .btn-red { background: linear-gradient(to bottom, #e74c3c, #c0392b); border: 1px solid #922b21; }
        .btn-purple { background: linear-gradient(to bottom, #9b59b6, #8e44ad); border: 1px solid #6c3483; }

        .deco-board-container {
            margin: 4px 0; width: 100%; display: flex; justify-content: center; pointer-events: none;
        }
        .deco-board {
            display: grid; grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr); gap: 1px;
            border: 2px solid #f1c40f; background-color: #2c3e50;
            border-radius: 10px; width: 240px; height: 240px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.7);
        }
        .deco-square {
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; user-select: none; width: 100%; height: 100%; position: relative;
        }
        .deco-light { background-color: #95a5a6; color: #2c3e50; }
        .deco-dark { background-color: #34495e; color: #ecf0f1; }
        .deco-boked {
            position: absolute; bottom: 0px; right: 0px; font-size: 5px;
            background: #e74c3c; color: #fff; padding: 0px 1px; border-radius: 2px;
            font-weight: bold;
        }

        .leaderboard-box {
            margin-top: 4px; background: rgba(15, 25, 35, 0.85);
            border-radius: 10px; padding: 6px 8px; border: 1px solid rgba(241, 196, 15, 0.2);
            text-align: left; width: 100%; max-height: 68px; overflow-y: auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        .leaderboard-title { color: #f1c40f; font-size: 10px; font-weight: bold; text-align: center; margin-bottom: 3px; }
        .lb-item { display: flex; justify-content: space-between; font-size: 10px; padding: 2px 2px; border-bottom: 1px solid rgba(255,255,255,0.05); }

        .player-hud {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(30, 40, 55, 0.85); padding: 4px 8px; border-radius: 8px;
            width: 100%; border: 1px solid rgba(241, 196, 15, 0.2); font-size: 11px;
        }
        .hud-user-info { display: flex; align-items: center; gap: 6px; }
        .hud-avatar { width: 24px; height: 24px; background: #34495e; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; border: 1px solid #f1c40f; }
        .hud-timer { background: rgba(0,0,0,0.6); padding: 2px 6px; border-radius: 6px; font-family: monospace; font-size: 11px; color: #fff; border: 1px solid rgba(255,255,255,0.2); }

        .bubble-speech {
            background: #f1c40f; color: #111; padding: 3px 10px; border-radius: 10px;
            font-size: 10px; font-weight: bold; box-shadow: 0 3px 6px rgba(241,196,15,0.4);
            position: relative; margin: 1px auto; max-width: 100%; word-break: break-word;
        }

        /* ផ្នែកកែប្រែទំហំក្ដារអុកឱ្យធំពេញល្មម និងទុក Margin ១០ភីកសែល (10px) សងខាង */
        .chessboard-wrapper {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 0 10px; /* ទុកគម្លាត Margin សងខាង ១០px */
            box-sizing: border-box;
            margin: 2px auto;
        }

        #board {
            display: grid; grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr); gap: 1px;
            justify-content: center;
            border: 2px solid #2c3e50; background-color: #2c3e50;
            border-radius: 6px; 
            width: calc(100vw - 20px); /* ទទឹងពេញអេក្រង់ ដក ២០px សម្រាប់សងខាង (១០px ម្នាក់) */
            max-width: 360px;          /* ទំហំអតិបរមា កុំឱ្យធំពេកលើអេក្រង់ធំ */
            height: auto;
            aspect-ratio: 1 / 1;       /* រក្សាទម្រង់ជាការ៉េស្មើគ្នា */
            box-shadow: 0 6px 15px rgba(0,0,0,0.8);
        }
        .square {
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; font-weight: bold; cursor: pointer; user-select: none;
            width: 100%; height: 100%; transition: background 0.2s; position: relative;
        }
        .light { background-color: #95a5a6; color: #111; }
        .dark { background-color: #34495e; color: #fff; }
        .selected { background-color: #7b61ff !important; box-shadow: inset 0 0 6px #fff; }
        .highlight { background-color: #2ecc71 !important; }
        .last-move { background-color: rgba(241, 196, 15, 0.45) !important; }

        .white-piece { color: #ffffff; text-shadow: 0 2px 4px #000; font-size: 24px; }
        .black-piece { color: #111111; text-shadow: 0 2px 4px #fff; font-size: 24px; }
        
        .king-warning {
            background-color: #e74c3c !important;
            animation: pulseWarning 0.8s infinite alternate;
        }
        @keyframes pulseWarning {
            0% { transform: scale(1); filter: brightness(1); }
            100% { transform: scale(1.05); filter: brightness(1.3); }
        }

        .boked-badge {
            position: absolute; bottom: 1px; right: 1px; font-size: 5px;
            background: #e74c3c; color: #fff; padding: 1px 2px; border-radius: 2px;
            font-weight: bold;
        }

        .webrtc-controls {
            display: flex; gap: 6px; width: 100%; justify-content: center; margin: 2px 0;
        }
        .webrtc-controls button { width: auto; padding: 4px 10px; font-size: 10px; margin: 0; }

        .chat-box {
            display: flex; gap: 4px; width: 100%; margin: 2px 0;
        }
        .chat-box input { margin: 0; flex-grow: 1; padding: 4px 6px; font-size: 11px; }
        .chat-box button { width: 50px; margin: 0; padding: 4px; font-size: 11px; }

        .modal {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); display: flex; justify-content: center; align-items: center;
            z-index: 10; backdrop-filter: blur(5px);
        }
        .modal-content {
            background: #1b2838; border: 2px solid #f1c40f; padding: 15px;
            border-radius: 16px; text-align: center; width: 90%; max-width: 280px;
        }
        .modal-title { font-size: 16px; color: #f1c40f; margin-bottom: 6px; font-weight: bold; }
        .modal-text { font-size: 12px; margin-bottom: 10px; color: #ddd; }

        .hidden { display: none !important; }
        .toggle-text { font-size: 10px; color: #3498db; cursor: pointer; margin-top: 4px; text-decoration: underline; }
    </style>
</head>
<body>

    <div class="bg-chess">
        <div class="floating-piece" style="left: 10%; animation-duration: 7s;">♔</div>
        <div class="floating-piece" style="left: 30%; animation-duration: 10s; animation-delay: 2s;">♕</div>
        <div class="floating-piece" style="left: 50%; animation-duration: 6s; animation-delay: 1s;">♖</div>
        <div class="floating-piece" style="left: 70%; animation-duration: 9s; animation-delay: 3s;">♗</div>
        <div class="floating-piece" style="left: 90%; animation-duration: 8s; animation-delay: 2s;">♘</div>
    </div>

    <div class="container">
        <div class="header-row">
            <div class="profile-dropdown-container">
                <div class="user-logo-btn" onclick="toggleProfileDropdown(event)" title="ប្រវត្តិរូប">
                    👤
                </div>
                <div class="dropdown-menu" id="profileDropdown">
                    <div class="dropdown-header-info">
                        <div class="dropdown-username" id="dropdownUsername">អ្នកលេង</div>
                        <div class="dropdown-points">⭐ <span id="userPoints">0</span> ពិន្ទុ</div>
                    </div>
                    <div class="dropdown-item" style="cursor: default;">
                        📊 ឈ្នះ: <span id="statWins">0</span> | ចាញ់: <span id="statLosses">0</span>
                    </div>
                    <div class="dropdown-item logout" onclick="logoutUser()">
                        🚪 ចាកចេញពីគណនី
                    </div>
                </div>
            </div>

            <h1>♟️ សូមគិតអោយបានឆ្ងាយមុនសម្រេចចិត្ត ♟️</h1>
            
            <div style="width: 32px;"></div>
        </div>

        <div id="login-box" class="clean-menu-layout hidden">
            <h3 id="auth-title" style="color: #f1c40f; margin: 0 0 8px 0; font-size: 14px;">ចូលគណនីរបស់អ្នក</h3>
            <input type="text" id="usernameInput" placeholder="ឈ្មោះអ្នកលេង (ចុះឈ្មោះ)" class="hidden">
            <input type="email" id="emailInput" placeholder="អ៊ីមែល (Email)">
            <input type="password" id="passwordInput" placeholder="ពាក្យសម្ងាត់ (Password)">
            
            <button id="authBtn" class="btn-green" onclick="handleAuth()">ចូលគណនី</button>
            <div class="toggle-text" id="toggleAuthMode" onclick="toggleAuthMode()">មិនទាន់មានគណនី? ចុះឈ្មោះថ្មី</div>
        </div>

        <div id="main-menu" class="clean-menu-layout hidden">
            <div class="deco-board-container">
                <div class="deco-board" id="decoBoard"></div>
            </div>

            <div class="menu-grid">
                <div class="menu-box-btn btn-gold-box" onclick="startTournamentRoom()">
                    <div class="menu-icon">🏆</div>
                    <div class="menu-label">ប្រកួតដណ្ដើមពាន</div>
                </div>
                <div class="menu-box-btn btn-green-box" onclick="quickJoinRoom()">
                    <div class="menu-icon">⚡</div>
                    <div class="menu-label">លេងជាមួយ AI</div>
                </div>
                <div class="menu-box-btn btn-blue-box" onclick="createPrivateRoom()">
                    <div class="menu-icon">🏠</div>
                    <div class="menu-label">បង្កើតបន្ទប់</div>
                </div>
                <div class="menu-box-btn btn-green-box" onclick="joinPrivateRoom()">
                    <div class="menu-icon">🔗</div>
                    <div class="menu-label">ចូលតាមកូដ</div>
                </div>
                <div class="menu-box-btn full-width-box btn-blue-box" style="grid-column: span 2; padding: 4px 8px;">
                    <input type="text" id="roomCodeInput" placeholder="បញ្ចូលកូដ (ឧ. Room_1234)">
                    <button class="btn-green" onclick="joinPrivateRoom()" style="margin: 0; width: auto; padding: 5px 10px;">ចូល</button>
                </div>
            </div>

            <div class="leaderboard-box">
                <div class="leaderboard-title">🏆 តារាងចំណាត់ថ្នាក់ពូកែលេងជាងគេ 🏆</div>
                <div id="leaderboardList">កំពុងទាញយក...</div>
            </div>
        </div>

        <div id="game-container" class="clean-menu-layout game-clean-layout hidden">
            <div class="player-hud">
                <div class="hud-user-info">
                    <div class="hud-avatar" id="oppAvatarIcon">🤖</div>
                    <div>
                        <div id="opponentName" style="font-weight: bold; color: #f1c40f;">Gemini AI ជើងខ្លាំង</div>
                        <div id="opponentStatus" style="font-size: 9px; color: #aaa;">Online & Ready</div>
                    </div>
                </div>
                <div class="hud-timer" id="timerTop">09:28</div>
            </div>

            <div class="bubble-speech" id="bubbleMsg">សួស្តី! ត្រៀមខ្លួនចាញ់កលល្បិចអុកខ្ញុំហើយឬនៅ? ហាសហា!</div>
            
            <div class="webrtc-controls" id="webrtcBox">
                <button class="btn-purple" onclick="toggleVoiceCall()" id="callBtn">📞 បើកសំឡេងនិយាយគ្នា</button>
                <span id="callStatus" style="font-size: 10px; color: #2ecc71; align-self: center;"></span>
            </div>
            <audio id="remoteAudio" autoplay></audio>

            <!-- ក្ដារអុកដាក់ក្នុង wrapper ដែលមាន Margin 10px សងខាង -->
            <div class="chessboard-wrapper">
                <div id="board"></div>
            </div>

            <div class="chat-box">
                <input type="text" id="chatInput" placeholder="និយាយអ្វីមួយជាមួយគូប្រកួត...">
                <button class="btn-blue" onclick="sendChatMsg()">ផ្ញើ</button>
            </div>

            <div class="player-hud">
                <div class="hud-user-info">
                    <div class="hud-avatar" style="background: #f1c40f; color: #111;">😊</div>
                    <div>
                        <div id="myHudName" style="font-weight: bold; color: #fff;">Player</div>
                        <div id="myTurnStatus" style="font-size: 9px; color: #2ecc71;">● Your turn</div>
                    </div>
                </div>
                <div class="hud-timer" id="timerBottom">09:30</div>
            </div>

            <button class="btn-red" style="width: 100%; margin-top: 2px; padding: 4px; font-size: 11px;" onclick="leaveRoom()">ចាកចេញពីបន្ទប់</button>
            
            <div style="width: 100%; display: flex; justify-content: center; margin-top: 2px; overflow: hidden;">
                <script type="text/javascript">
                    atOptions = {
                        'key' : '5959695',
                        'format' : 'iframe',
                        'height' : 50,
                        'width' : 320,
                        'params' : {}
                    };
                </script>
                <script type="text/javascript" src="//www.highperformanceformat.com/5959695/invoke.js"></script>
            </div>
        </div>
    </div>

    <div id="gameOverModal" class="modal hidden">
        <div class="modal-content">
            <div class="modal-title" id="modalTitle">លទ្ធផលហ្គេម</div>
            <div class="modal-text" id="modalText">តើអ្នកចង់លេងម្ដងទៀតទេ?</div>
            <button class="btn-green" onclick="playAgain()">🔄 លេងម្ដងទៀត</button>
            <button class="btn-red" onclick="closeModalAndMenu()">🏠 ត្រឡប់ទៅមីនុយដើម</button>
        </div>
    </div>

    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
        import { getDatabase, ref, set, get, update, onValue, remove, onDisconnect } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";

        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW error:', err));
            });
        }

        const firebaseConfig = {
            apiKey: "AIzaSyB2A-i0K1APedqO21pllsOisHIu-gb4HeI",
            authDomain: "ouk-e348e.firebaseapp.com",
            databaseURL: "https://ouk-e348e-default-rtdb.firebaseio.com",
            projectId: "ouk-e348e",
            storageBucket: "ouk-e348e.firebasestorage.app",
            messagingSenderId: "166337664392",
            appId: "1:166337664392:web:ae5740689b1f62ecbd163d",
            measurementId: "G-QZY7PJNR11"
        };

        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        const db = getDatabase(app);

        let isRegisterMode = false;
        window.toggleAuthMode = function() {
            isRegisterMode = !isRegisterMode;
            document.getElementById("auth-title").textContent = isRegisterMode ? "ចុះឈ្មោះគណនីថ្មី" : "ចូលគណនីរបស់អ្នក";
            document.getElementById("authBtn").textContent = isRegisterMode ? "ចុះឈ្មោះ" : "ចូលគណនី";
            document.getElementById("toggleAuthMode").textContent = isRegisterMode ? "មានគណនីរួចហើយ? ចូលគណនី" : "មិនទាន់មានគណនី? ចុះឈ្មោះថ្មី";
            document.getElementById("usernameInput").classList.toggle("hidden", !isRegisterMode);
        }

        window.toggleProfileDropdown = function(event) {
            event.stopPropagation();
            const dropdown = document.getElementById("profileDropdown");
            dropdown.classList.toggle("show");
        }

        window.addEventListener('click', () => {
            const dropdown = document.getElementById("profileDropdown");
            if (dropdown && dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
            }
        });

        window.handleAuth = async function() {
            initAudio();
            const email = document.getElementById("emailInput").value.trim();
            const password = document.getElementById("passwordInput").value.trim();
            const username = document.getElementById("usernameInput").value.trim();

            if (!email || !password) { alert("សូមបំពេញអ៊ីមែល និងពាក្យសម្ងាត់ឱ្យបានត្រឹមត្រូវ!"); return; }
            if (isRegisterMode && !username) { alert("សូមបញ្ចូលឈ្មោះអ្នកលេងរបស់អ្នក!"); return; }

            try {
                if (isRegisterMode) {
                    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
                    await set(ref(db, `users/${userCredential.user.uid}`), { name: username, points: 100, wins: 0, losses: 0 });
                } else {
                    await signInWithEmailAndPassword(auth, email, password);
                }
            } catch (error) { alert("មានបញ្ហា៖ " + error.message); }
        }

        window.logoutUser = function() { signOut(auth); }

        let audioCtx = null;
        function initAudio() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();
        }

        function playSound(type) {
            initAudio();
            if (!audioCtx) return;
            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            let now = audioCtx.currentTime;

            if (type === 'move') {
                osc.type = 'sine'; osc.frequency.setValueAtTime(400, now); osc.frequency.exponentialRampToValueAtTime(600, now + 0.1);
                gainNode.gain.setValueAtTime(0.2, now); gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
                osc.start(now); osc.stop(now + 0.1);
            } else if (type === 'capture') {
                osc.type = 'triangle'; osc.frequency.setValueAtTime(250, now); osc.frequency.exponentialRampToValueAtTime(100, now + 0.15);
                gainNode.gain.setValueAtTime(0.3, now); gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
                osc.start(now); osc.stop(now + 0.15);
            } else if (type === 'warning') {
                osc.type = 'sawtooth'; osc.frequency.setValueAtTime(600, now); osc.frequency.setValueAtTime(900, now + 0.12);
                gainNode.gain.setValueAtTime(0.3, now); gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
                osc.start(now); osc.stop(now + 0.35);
            } else if (type === 'win') {
                osc.type = 'square'; osc.frequency.setValueAtTime(300, now); osc.frequency.setValueAtTime(450, now + 0.1);
                gainNode.gain.setValueAtTime(0.25, now); gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
                osc.start(now); osc.stop(now + 0.35);
            } else if (type === 'lose') {
                osc.type = 'sawtooth'; osc.frequency.setValueAtTime(300, now); osc.frequency.exponentialRampToValueAtTime(120, now + 0.3);
                gainNode.gain.setValueAtTime(0.25, now); gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
                osc.start(now); osc.stop(now + 0.3);
            }
        }

        const initialBoard = [
            [ {p:"♜", b:false}, {p:"♞", b:false}, {p:"♝", b:false}, {p:"♛", b:false}, {p:"♚", b:false}, {p:"♝", b:false}, {p:"♞", b:false}, {p:"♜", b:false} ],
            [ {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false} ],
            [ {p:"♟", b:false}, {p:"♟", b:false}, {p:"♟", b:false}, {p:"♟", b:false}, {p:"♟", b:false}, {p:"♟", b:false}, {p:"♟", b:false}, {p:"♟", b:false} ],
            [ {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false} ],
            [ {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false} ],
            [ {p:"♙", b:false}, {p:"♙", b:false}, {p:"♙", b:false}, {p:"♙", b:false}, {p:"♙", b:false}, {p:"♙", b:false}, {p:"♙", b:false}, {p:"♙", b:false} ],
            [ {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false}, {p:"", b:false} ],
            [ {p:"♖", b:false}, {p:"♘", b:false}, {p:"♗", b:false}, {p:"♕", b:false}, {p:"♔", b:false}, {p:"♗", b:false}, {p:"♘", b:false}, {p:"♖", b:false} ]
        ];

        let myUid = "", myName = "", rawDisplayName = "", myPoints = 100, myWins = 0, myLosses = 0;
        let currentRoomId = "", myRole = "", board = JSON.parse(JSON.stringify(initialBoard));
        let turn = "white", gameOver = false, selectedPiece = null, validMoves = [], isVsAI = false, isTournament = false;
        let lastMove = null;

        let peerConnection = null;
        let localStream = null;
        let isCallActive = false;
        const servers = { iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] };

        let decoBoardState = JSON.parse(JSON.stringify(initialBoard));
        let decoTurn = "white", decoInterval = null;
        const strategicOpenings = [
            {from: {r: 5, c: 3}, to: {r: 4, c: 3}},
            {from: {r: 2, c: 3}, to: {r: 3, c: 3}},
            {from: {r: 7, c: 1}, to: {r: 5, c: 2}},
            {from: {r: 0, c: 1}, to: {r: 2, c: 2}},
        ];
        let decoMoveIndex = 0;

        function startDecoAutoPlay() {
            if (decoInterval) clearInterval(decoInterval);
            decoBoardState = JSON.parse(JSON.stringify(initialBoard));
            decoMoveIndex = 0; decoTurn = "white";
            renderDecoBoard();
            decoInterval = setInterval(() => {
                if (decoMoveIndex < strategicOpenings.length) {
                    let m = strategicOpenings[decoMoveIndex];
                    let movingCell = decoBoardState[m.from.r][m.from.c];
                    let isBokedNow = movingCell.b;
                    if (movingCell.p === "♙" && m.to.r === 2) isBokedNow = true;
                    if (movingCell.p === "♟" && m.to.r === 5) isBokedNow = true;
                    decoBoardState[m.to.r][m.to.c] = { p: movingCell.p, b: isBokedNow };
                    decoBoardState[m.from.r][m.from.c] = { p: "", b: false };
                    decoMoveIndex++;
                } else {
                    let allMoves = getAllValidMovesForColor(decoBoardState, decoTurn === "white");
                    if (allMoves.length > 0) {
                        let m = allMoves[Math.floor(Math.random() * allMoves.length)];
                        let movingCell = decoBoardState[m.fromR][m.fromC];
                        let isBokedNow = movingCell.b;
                        if (movingCell.p === "♙" && m.toR === 2) isBokedNow = true;
                        if (movingCell.p === "♟" && m.toR === 5) isBokedNow = true;
                        decoBoardState[m.toR][m.toC] = { p: movingCell.p, b: isBokedNow };
                        decoBoardState[m.fromR][m.fromC] = { p: "", b: false };
                    } else {
                        decoBoardState = JSON.parse(JSON.stringify(initialBoard));
                        decoMoveIndex = 0;
                    }
                    decoTurn = decoTurn === "white" ? "black" : "white";
                }
                renderDecoBoard();
            }, 1800);
        }

        function renderDecoBoard() {
            const decoEl = document.getElementById("decoBoard");
            if (!decoEl) return;
            decoEl.innerHTML = "";
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const sq = document.createElement("div");
                    sq.className = "deco-square " + ((r + c) % 2 === 0 ? "deco-light" : "deco-dark");
                    let cell = decoBoardState[r][c];
                    if (cell.p !== "") {
                        sq.textContent = cell.p;
                        sq.style.color = ["♖", "♘", "♗", "♕", "♔", "♙"].includes(cell.p) ? "#fff" : "#111";
                        if (cell.b) {
                            let bTag = document.createElement("div");
                            bTag.className = "deco-boked";
                            bTag.textContent = "បក";
                            sq.appendChild(bTag);
                        }
                    }
                    decoEl.appendChild(sq);
                }
            }
        }
        startDecoAutoPlay();

        function loadLeaderboard() {
            onValue(ref(db, 'users'), (snapshot) => {
                const lbEl = document.getElementById("leaderboardList");
                if (!lbEl) return;
                if (!snapshot.exists()) { lbEl.innerHTML = "<div style='text-align:center; color:#888;'>មិនទាន់មានទិន្នន័យ</div>"; return; }
                let usersData = snapshot.val();
                let usersArray = [];
                for (let u in usersData) { usersArray.push({ name: usersData[u].name || "អ្នកលេង", points: usersData[u].points || 0 }); }
                usersArray.sort((a, b) => b.points - a.points);
                lbEl.innerHTML = "";
                usersArray.slice(0, 5).forEach((user, index) => {
                    let rankIcon = index === 0 ? "🥇" : (index === 1 ? "🥈" : (index === 2 ? "🥉" : `🏅 #${index+1}`));
                    let item = document.createElement("div");
                    item.className = "lb-item";
                    item.innerHTML = `<span>${rankIcon} ${user.name}</span> <span style="color:#f1c40f;">⭐ ${user.points} ពិន្ទុ</span>`;
                    lbEl.appendChild(item);
                });
            });
        }
        loadLeaderboard();

        onAuthStateChanged(auth, async (user) => {
            if (user) {
                myUid = user.uid;
                const snapshot = await get(ref(db, `users/${myUid}`));
                if (snapshot.exists()) {
                    let data = snapshot.val();
                    rawDisplayName = data.name || "អ្នកលេង";
                    myPoints = data.points ?? 100;
                    myWins = data.wins ?? 0;
                    myLosses = data.losses ?? 0;
                } else {
                    rawDisplayName = user.email.split('@')[0];
                    myPoints = 100; myWins = 0; myLosses = 0;
                    await set(ref(db, `users/${myUid}`), { name: rawDisplayName, points: myPoints, wins: myWins, losses: myLosses });
                }
                myName = rawDisplayName.replace(/[.#$\/\[\]]/g, "_");
                updateUIStats();
                document.getElementById("login-box").classList.add("hidden");
                document.getElementById("main-menu").classList.remove("hidden");
                document.getElementById("dropdownUsername").textContent = rawDisplayName;
            } else {
                document.getElementById("login-box").classList.remove("hidden");
                document.getElementById("main-menu").classList.add("hidden");
            }
        });

        function updateUIStats() {
            document.getElementById("userPoints").textContent = myPoints;
            document.getElementById("statWins").textContent = myWins;
            document.getElementById("statLosses").textContent = myLosses;
        }

        async function recordGameResult(didWin, tournamentWin = false) {
            if (tournamentWin) { myWins += 1; myPoints += 50; playSound('win'); }
            else if (didWin) { myWins += 1; myPoints += 15; playSound('win'); }
            else { myLosses += 1; myPoints = Math.max(0, myPoints - 10); playSound('lose'); }
            updateUIStats();
            if (myUid) {
                await update(ref(db, `users/${myUid}`), { name: rawDisplayName, points: myPoints, wins: myWins, losses: myLosses }).catch(e => {});
            }
        }

        function isWhitePiece(p) { return ["♖", "♘", "♗", "♕", "♔", "♙"].includes(p); }
        function isBlackPiece(p) { return ["♜", "♞", "♝", "♛", "♚", "♟"].includes(p); }

        function getAllValidMovesForColor(currentBoard, isWhiteTurn) {
            let allMoves = [];
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    let cell = currentBoard[r][c];
                    if (cell.p !== "" && ((isWhiteTurn && isWhitePiece(cell.p)) || (!isWhiteTurn && isBlackPiece(cell.p)))) {
                        let moves = getValidMovesForBoard(r, c, cell, currentBoard);
                        for (let m of moves) allMoves.push({fromR: r, fromC: c, toR: m.r, toC: m.c});
                    }
                }
            }
            return allMoves;
        }

        function findKingPosition(currentBoard, isWhiteKing) {
            let kingSymbol = isWhiteKing ? "♔" : "♚";
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    if (currentBoard[r][c].p === kingSymbol) return {r, c};
                }
            }
            return null;
        }

        function isKingInCheck(currentBoard, isWhiteKing) {
            let kingPos = findKingPosition(currentBoard, isWhiteKing);
            if (!kingPos) return false;
            let enemyMoves = getAllValidMovesForColor(currentBoard, !isWhiteKing);
            return enemyMoves.some(m => m.toR === kingPos.r && m.toC === kingPos.c);
        }

        function getValidMovesForBoard(r, c, cell, currentBoard) {
            let moves = [];
            let piece = cell.p, isWhite = isWhitePiece(piece);
            
            if (piece === "♔" || piece === "♚") {
                let directions = [[-1,0], [1,0], [0,-1], [0,1], [-1,-1], [-1,1], [1,-1], [1,1]];
                for (let d of directions) {
                    let nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = currentBoard[nr][nc].p;
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) moves.push({r: nr, c: nc});
                    }
                }
                let jumpingDirections = [[-2, -2], [-2, 2], [2, -2], [2, 2]];
                for (let jd of jumpingDirections) {
                    let nr = r + jd[0], nc = c + jd[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = currentBoard[nr][nc].p;
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) moves.push({r: nr, c: nc});
                    }
                }
            } else if (piece === "♕" || piece === "♛") {
                let directions = [[-1,-1], [-1,1], [1,-1], [1,1]];
                for (let d of directions) {
                    let nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = currentBoard[nr][nc].p;
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) moves.push({r: nr, c: nc});
                    }
                }
            } else if (piece === "♗" || piece === "♝") {
                let directions = isWhite ? [[-1,0], [-1,-1], [-1,1], [1,-1], [1,1]] : [[1,0], [-1,-1], [-1,1], [1,-1], [1,1]];
                for (let d of directions) {
                    let nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = currentBoard[nr][nc].p;
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) moves.push({r: nr, c: nc});
                    }
                }
            } else if (piece === "♘" || piece === "♞") {
                let jmps = [[-2,-1], [-2,1], [-1,-2], [-1,2], [1,-2], [1,2], [2,-1], [2,1]];
                for (let d of jmps) {
                    let nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = currentBoard[nr][nc].p;
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) moves.push({r: nr, c: nc});
                    }
                }
            } else if (piece === "♖" || piece === "♜") {
                let directions = [[-1,0], [1,0], [0,-1], [0,1]];
                for (let d of directions) {
                    let step = 1;
                    while (true) {
                        let nr = r + d[0] * step, nc = c + d[1] * step;
                        if (nr < 0 || nr >= 8 || nc < 0 || nc >= 8) break;
                        let target = currentBoard[nr][nc].p;
                        if (target === "") { moves.push({r: nr, c: nc}); }
                        else {
                            if ((isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) moves.push({r: nr, c: nc});
                            break;
                        }
                        step++;
                    }
                }
            } else if (piece === "♙" || piece === "♟") {
                if (cell.b) {
                    let directions = [[-1,-1], [-1,1], [1,-1], [1,1]];
                    for (let d of directions) {
                        let nr = r + d[0], nc = c + d[1];
                        if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                            let target = currentBoard[nr][nc].p;
                            if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) moves.push({r: nr, c: nc});
                        }
                    }
                } else {
                    let fwd = isWhite ? -1 : 1;
                    let nr = r + fwd, nc = c;
                    if (nr >= 0 && nr < 8 && currentBoard[nr][nc].p === "") moves.push({r: nr, c: nc});
                    if (nr >= 0 && nr < 8) {
                        if (c - 1 >= 0) {
                            let targetLeft = currentBoard[nr][c - 1].p;
                            if (targetLeft !== "" && ((isWhite && isBlackPiece(targetLeft)) || (!isWhite && isWhitePiece(targetLeft)))) moves.push({r: nr, c: c - 1});
                        }
                        if (c + 1 < 8) {
                            let targetRight = currentBoard[nr][c + 1].p;
                            if (targetRight !== "" && ((isWhite && isBlackPiece(targetRight)) || (!isWhite && isWhitePiece(targetRight)))) moves.push({r: nr, c: c + 1});
                        }
                    }
                }
            }
            return moves;
        }

        function evaluateBoard(currentBoard) {
            let score = 0;
            const values = { "♟": 12, "♙": -12, "♞": 35, "♘": -35, "♝": 35, "♗": -35, "♜": 60, "♖": -60, "♛": 110, "♕": -110, "♚": 1200, "♔": -1200 };
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    let cell = currentBoard[r][c], p = cell.p;
                    if (values[p] !== undefined) {
                        score += values[p];
                        if (cell.b) score += (p === "♟" ? 30 : -30);
                        if (p === "♟" && (r >= 3 && r <= 5)) score += 5;
                    }
                }
            }
            return score;
        }

        function minimax(currentBoard, depth, alpha, beta, isMaximizing) {
            if (depth === 0) return evaluateBoard(currentBoard);
            let allMoves = getAllValidMovesForColor(currentBoard, !isMaximizing);
            if (allMoves.length === 0) return evaluateBoard(currentBoard);

            allMoves.sort((a, b) => {
                let targetA = currentBoard[a.toR][a.toC].p;
                let targetB = currentBoard[b.toR][b.toC].p;
                return (targetB !== "" ? 1 : 0) - (targetA !== "" ? 1 : 0);
            });

            if (isMaximizing) {
                let maxEval = -Infinity;
                for (let m of allMoves) {
                    let tempBoard = JSON.parse(JSON.stringify(currentBoard));
                    let movingCell = tempBoard[m.fromR][m.fromC];
                    if (tempBoard[m.toR][m.toC].p === "♔") return 15000;
                    let isBokedNow = movingCell.b;
                    if (movingCell.p === "♟" && m.toR === 5) isBokedNow = true;
                    tempBoard[m.toR][m.toC] = { p: movingCell.p, b: isBokedNow };
                    tempBoard[m.fromR][m.fromC] = { p: "", b: false };
                    let evalScore = minimax(tempBoard, depth - 1, alpha, beta, false);
                    maxEval = Math.max(maxEval, evalScore);
                    alpha = Math.max(alpha, evalScore);
                    if (beta <= alpha) break;
                }
                return maxEval;
            } else {
                let minEval = Infinity;
                for (let m of allMoves) {
                    let tempBoard = JSON.parse(JSON.stringify(currentBoard));
                    let movingCell = tempBoard[m.fromR][m.fromC];
                    if (tempBoard[m.toR][m.toC].p === "♚") return -15000;
                    let isBokedNow = movingCell.b;
                    if (movingCell.p === "♙" && m.toR === 2) isBokedNow = true;
                    tempBoard[m.toR][m.toC] = { p: movingCell.p, b: isBokedNow };
                    tempBoard[m.fromR][m.fromC] = { p: "", b: false };
                    let evalScore = minimax(tempBoard, depth - 1, alpha, beta, true);
                    minEval = Math.min(minEval, evalScore);
                    beta = Math.min(beta, evalScore);
                    if (beta <= alpha) break;
                }
                return minEval;
            }
        }

        function aiMakeMove() {
            if (gameOver) return;
            let allMoves = getAllValidMovesForColor(board, false);
            if (allMoves.length === 0) return;

            let bestMove;
            if (Math.random() < 0.25) {
                bestMove = allMoves[Math.floor(Math.random() * allMoves.length)];
            } else {
                let bestEval = -Infinity, bestMoves = [];
                for (let m of allMoves) {
                    let tempBoard = JSON.parse(JSON.stringify(board));
                    let movingCell = tempBoard[m.fromR][m.fromC];
                    if (tempBoard[m.toR][m.toC].p === "♔") { bestMoves = [m]; break; }
                    let isBokedNow = movingCell.b;
                    if (movingCell.p === "♟" && m.toR === 5) isBokedNow = true;
                    tempBoard[m.toR][m.toC] = { p: movingCell.p, b: isBokedNow };
                    tempBoard[m.fromR][m.fromC] = { p: "", b: false };
                    let evalScore = minimax(tempBoard, 2, -Infinity, Infinity, false);
                    if (evalScore > bestEval) { bestEval = evalScore; bestMoves = [m]; }
                    else if (evalScore === bestEval) { bestMoves.push(m); }
                }
                bestMove = bestMoves[Math.floor(Math.random() * bestMoves.length)];
            }

            let movingCell = board[bestMove.fromR][bestMove.fromC];
            let targetPiece = board[bestMove.toR][bestMove.toC].p;
            let isBokedNow = movingCell.b;
            if (movingCell.p === "♟" && bestMove.toR === 5) isBokedNow = true;

            if (targetPiece !== "") playSound('capture'); else playSound('move');

            board[bestMove.toR][bestMove.toC] = { p: movingCell.p, b: isBokedNow };
            board[bestMove.fromR][bestMove.fromC] = { p: "", b: false };
            lastMove = { fromR: bestMove.fromR, fromC: bestMove.fromC, toR: bestMove.toR, toC: bestMove.toC };

            if (targetPiece === "♔") {
                gameOver = true;
                showGameOverModal("😔 អ្នកបានចាញ់គូប្រកួតហើយ!", false, false);
            } else {
                turn = "white";
                updateStatusDisplay();
            }
            renderBoard();
        }

        function showGameOverModal(message, didWin, tournamentWin = false) {
            document.getElementById("modalTitle").textContent = tournamentWin ? "🏆 ជើងឯកពានរង្វាន់!" : (didWin ? "🎉 អបអរសាទរ!" : "😢 ចាញ់បាត់ហើយ!");
            document.getElementById("modalText").textContent = message;
            document.getElementById("gameOverModal").classList.remove("hidden");
            recordGameResult(didWin, tournamentWin);
        }

        window.playAgain = function() {
            if (isTournament) { startTournamentRoom(); } else { quickJoinRoom(); }
        }

        window.closeModalAndMenu = function() {
            document.getElementById("gameOverModal").classList.add("hidden");
            window.leaveRoom();
        }

        window.startTournamentRoom = function() {
            initAudio(); isVsAI = true; isTournament = true;
            document.getElementById("webrtcBox").classList.add("hidden");
            board = JSON.parse(JSON.stringify(initialBoard));
            turn = "white"; gameOver = false; selectedPiece = null; validMoves = []; lastMove = null;
            document.getElementById("gameOverModal").classList.add("hidden");
            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("opponentName").textContent = "Gemini AI ជើងខ្លាំង";
            document.getElementById("oppAvatarIcon").textContent = "🤖";
            updateStatusDisplay();
            renderBoard();
        }

        window.quickJoinRoom = function() {
            initAudio(); isVsAI = true; isTournament = false;
            document.getElementById("webrtcBox").classList.add("hidden");
            board = JSON.parse(JSON.stringify(initialBoard));
            turn = "white"; gameOver = false; selectedPiece = null; validMoves = []; lastMove = null;
            document.getElementById("gameOverModal").classList.add("hidden");
            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("opponentName").textContent = "Gemini AI រហ័ស";
            document.getElementById("oppAvatarIcon").textContent = "🤖";
            updateStatusDisplay();
            renderBoard();
        }

        window.createPrivateRoom = async function() {
            initAudio(); isVsAI = false; isTournament = false;
            try {
                const targetRoom = "Room_" + Math.floor(Math.random() * 9000 + 1000);
                await set(ref(db, `rooms/${targetRoom}`), { board: initialBoard, turn: "white", gameOver: false, message: "រង់ចាំគូប្រកួត...", players: {} });
                await joinRoomProcess(targetRoom);
                alert(`កូដបន្ទប់របស់អ្នក៖ ${targetRoom}`);
            } catch (error) { alert("មានបញ្ហាក្នុងការបង្កើតបន្ទប់!"); }
        }

        window.joinPrivateRoom = async function() {
            initAudio(); isVsAI = false; isTournament = false;
            const rCode = document.getElementById("roomCodeInput").value.trim();
            if (!rCode) { alert("សូមបញ្ចូលកូដបន្ទប់សិន!"); return; }
            try {
                if (!(await get(ref(db, `rooms/${rCode}`))).exists()) { alert("រកមិនឃើញបន្ទប់នេះទេ!"); return; }
                await joinRoomProcess(rCode);
            } catch(e) { alert("មានបញ្ហាក្នុងការចូលបន្ទប់!"); }
        }

        async function joinRoomProcess(roomId) {
            currentRoomId = roomId;
            document.getElementById("webrtcBox").classList.remove("hidden");
            try {
                const pSnap = await get(ref(db, `rooms/${currentRoomId}/players`));
                let players = pSnap.exists() ? pSnap.val() : {};
                if (!players.white) { myRole = "white"; players.white = myName; }
                else if (!players.black) { myRole = "black"; players.black = myName; }
                else { myRole = "observer"; }

                await update(ref(db, `rooms/${currentRoomId}`), { players: players });
                if (myRole === 'white') onDisconnect(ref(db, `rooms/${currentRoomId}/players/white`)).remove();
                else if (myRole === 'black') onDisconnect(ref(db, `rooms/${currentRoomId}/players/black`)).remove();
            } catch(e) { myRole = "white"; }

            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("oppAvatarIcon").textContent = "👤";
            listenToRoom();
            renderBoard();
        }

        function updateStatusDisplay() {
            let isMyTurn = isVsAI ? (turn === "white") : (turn === myRole);
            let oppStatus = document.getElementById("opponentStatus");
            let myTurnSt = document.getElementById("myTurnStatus");
            let bubble = document.getElementById("bubbleMsg");

            if (isMyTurn) {
                myTurnSt.textContent = "● Your turn";
                myTurnSt.style.color = "#2ecc71";
                oppStatus.textContent = "Online & Ready";
                if (isVsAI && !bubble.dataset.aiSpoken) bubble.textContent = "វេនអ្នកដើរហើយ! រក្សាស្មារតីឱ្យបានល្អ!";
            } else {
                myTurnSt.textContent = "Waiting...";
                myTurnSt.style.color = "#aaa";
                oppStatus.textContent = "● Thinking...";
                if (isVsAI) bubble.textContent = "Gemini AI កំពុងគិតកលល្បិចឌឺដង...";
            }
            if (isKingInCheck(board, isMyTurn ? (isVsAI ? true : myRole === 'white') : (isVsAI ? false : myRole !== 'white'))) {
                playSound('warning');
                if (isVsAI) bubble.textContent = "⚠️ ប្រយ័ត្នរងគ្រោះថ្នាក់ស្តេចហើយមិត្តសម្លាញ់!";
            }
        }

        function listenToRoom() {
            onValue(ref(db, `rooms/${currentRoomId}`), async (snapshot) => {
                if (!snapshot.exists()) return;
                const data = snapshot.val();
                if (!data.players || Object.keys(data.players).length === 0) { await remove(ref(db, `rooms/${currentRoomId}`)); return; }

                board = data.board; turn = data.turn; lastMove = data.lastMove || null;
                
                let players = data.players || {};
                if (myRole === 'white') {
                    document.getElementById("opponentName").textContent = players.black || "រង់ចាំគូប្រកួត...";
                } else {
                    document.getElementById("opponentName").textContent = players.white || "រង់ចាំគូប្រកួត...";
                }
                document.getElementById("myHudName").textContent = rawDisplayName + ` (${myRole === 'white' ? 'ស' : 'ខ្មៅ'})`;

                if (data.chat && isVsAI) {
                    document.getElementById("bubbleMsg").textContent = data.chat;
                } else if (data.chat && !isVsAI) {
                    document.getElementById("bubbleMsg").textContent = data.chat;
                }

                if (!isVsAI && data.rtc) {
                    if (data.rtc.offer && myRole === 'black' && !peerConnection) {
                        await setupWebRTC();
                        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.rtc.offer));
                        let answer = await peerConnection.createAnswer();
                        await peerConnection.setLocalDescription(answer);
                        await update(ref(db, `rooms/${currentRoomId}/rtc`), { answer: { type: answer.type, sdp: answer.sdp } });
                    } else if (data.rtc.answer && myRole === 'white' && peerConnection && !peerConnection.remoteDescription) {
                        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.rtc.answer));
                    }
                    if (data.rtc.candidate) {
                        try {
                            if (peerConnection && peerConnection.remoteDescription) {
                                await peerConnection.addIceCandidate(new RTCIceCandidate(data.rtc.candidate));
                            }
                        } catch(err) {}
                    }
                }

                if (data.gameOver && !gameOver) {
                    gameOver = true;
                    if (myRole !== "observer") {
                        let didWin = (data.winnerRole === myRole);
                        showGameOverModal(didWin ? "🎉 អ្នកឈ្នះហ្គេមនេះហើយ (+15 ពិន្ទុ)!" : "😔 អ្នកបានចាញ់ហ្គេមនេះ (-10 ពិន្ទុ)!", didWin, false);
                    }
                } else { gameOver = data.gameOver; }

                updateStatusDisplay();
                selectedPiece = null; validMoves = [];
                renderBoard();
            });
        }

        window.toggleVoiceCall = async function() {
            if (!isCallActive) {
                try {
                    localStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
                    await setupWebRTC();
                    
                    if (myRole === 'white') {
                        let offer = await peerConnection.createOffer();
                        await peerConnection.setLocalDescription(offer);
                        await update(ref(db, `rooms/${currentRoomId}/rtc`), { offer: { type: offer.type, sdp: offer.sdp } });
                    }
                    isCallActive = true;
                    document.getElementById("callBtn").textContent = "📞 បិទសំឡេង";
                    document.getElementById("callStatus").textContent = "កំពុងតភ្ជាប់សំឡេង...";
                } catch(e) {
                    alert("មិនអាចបើកមីក្រូហ្វូនបានទេ៖ " + e.message);
                }
            } else {
                if (localStream) localStream.getTracks().forEach(t => t.stop());
                if (peerConnection) peerConnection.close();
                peerConnection = null;
                isCallActive = false;
                document.getElementById("callBtn").textContent = "📞 បើកសំឡេងនិយាយគ្នា";
                document.getElementById("callStatus").textContent = "បានបិទសំឡេង";
            }
        }

        async function setupWebRTC() {
            if (peerConnection) return;
            peerConnection = new RTCPeerConnection(servers);

            if (localStream) {
                localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));
            }

            peerConnection.ontrack = (event) => {
                let remoteAudio = document.getElementById("remoteAudio");
                remoteAudio.srcObject = event.streams[0];
                document.getElementById("callStatus").textContent = "កំពុងនិយាយគ្នា...";
            };

            peerConnection.onicecandidate = (event) => {
                if (event.candidate && currentRoomId) {
                    update(ref(db, `rooms/${currentRoomId}/rtc`), { candidate: event.candidate.toJSON() });
                }
            };
        }

        window.sendChatMsg = async function() {
            let txt = document.getElementById("chatInput").value.trim();
            if (!txt) return;
            document.getElementById("chatInput").value = "";
            
            if (isVsAI) {
                document.getElementById("bubbleMsg").dataset.aiSpoken = "true";
                document.getElementById("bubbleMsg").textContent = `${rawDisplayName}: ${txt}`;
                
                try {
                    let res = await fetch("/api/gemini-chat", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ message: txt })
                    });
                    let data = await res.json();
                    setTimeout(() => {
                        document.getElementById("bubbleMsg").textContent = "🤖 Gemini: " + data.reply;
                    }, 600);
                } catch(e) {
                    setTimeout(() => {
                        document.getElementById("bubbleMsg").textContent = "🤖 Gemini: ហាសហា! និយាយត្រូវចិត្តម៉ង លេងបន្តទៀតមក!";
                    }, 600);
                }
            } else if (currentRoomId) {
                update(ref(db, `rooms/${currentRoomId}`), { chat: `${rawDisplayName}: ${txt}` });
            }
        }

        window.renderBoard = function() {
            const boardEl = document.getElementById("board");
            if (!boardEl) return;
            boardEl.innerHTML = "";
            let isMyTurn = isVsAI ? (turn === "white") : (turn === myRole);
            let kingInCheckPos = isKingInCheck(board, isMyTurn) ? findKingPosition(board, isMyTurn) : null;

            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const sq = document.createElement("div");
                    sq.className = "square " + ((r + c) % 2 === 0 ? "light" : "dark");
                    
                    if (selectedPiece && selectedPiece.r === r && selectedPiece.c === c) sq.classList.add("selected");
                    if (validMoves.some(m => m.r === r && m.c === c)) sq.classList.add("highlight");
                    if (lastMove && ((lastMove.fromR === r && lastMove.fromC === c) || (lastMove.toR === r && lastMove.toC === c))) {
                        sq.classList.add("last-move");
                    }
                    if (kingInCheckPos && kingInCheckPos.r === r && kingInCheckPos.c === c) sq.classList.add("king-warning");

                    let cell = board[r][c];
                    if (cell.p !== "") {
                        let span = document.createElement("span");
                        span.textContent = cell.p;
                        span.className = isWhitePiece(cell.p) ? "white-piece" : "black-piece";
                        sq.appendChild(span);
                        if (cell.b) {
                            let badge = document.createElement("div");
                            badge.className = "boked-badge";
                            badge.textContent = "បក";
                            sq.appendChild(badge);
                        }
                    }
                    sq.onclick = () => handleSquareClick(r, c);
                    boardEl.appendChild(sq);
                }
            }
        }

        function handleSquareClick(r, c) {
            if (gameOver) return;
            if (isVsAI && turn !== "white") return;
            if (!isVsAI && turn !== myRole) return;

            let clickedCell = board[r][c];
            if (selectedPiece) {
                if (validMoves.some(m => m.r === r && m.c === c)) {
                    let targetPiece = clickedCell.p, movingCell = selectedPiece.cell;
                    let fromR = selectedPiece.r, fromC = selectedPiece.c;
                    let isOver = false, msg = "", winRole = "";

                    if (targetPiece !== "") playSound('capture'); else playSound('move');
                    if (targetPiece === "♚") { isOver = true; msg = "🏆 អបអរសាទរ! អ្នកឈ្នះការប្រកួតនេះ!"; winRole = "white"; }
                    else if (targetPiece === "♔") { isOver = true; msg = "🎉 ភាគី ខ្មៅ ឈ្នះ!"; winRole = "black"; }

                    let isBokedNow = movingCell.b;
                    if (movingCell.p === "♙" && r === 2) isBokedNow = true;
                    if (movingCell.p === "♟" && r === 5) isBokedNow = true;

                    board[r][c] = { p: movingCell.p, b: isBokedNow };
                    board[fromR][fromC] = { p: "", b: false };
                    lastMove = { fromR: fromR, fromC: fromC, toR: r, toC: c };

                    let nextTurn = turn === 'white' ? 'black' : 'white';

                    if (isVsAI) {
                        gameOver = isOver;
                        if (gameOver) { 
                            showGameOverModal(isTournament ? "🏆 អស្ចារ្យណាស់! អ្នកបានឈ្នះពានរង្វាន់ (+50 ពិន្ទុ)!" : "🎉 អ្នកឈ្នះគូប្រកួតយ៉ាងអស្ចារ្យ (+15 ពិន្ទុ)!", true, isTournament);
                            return; 
                        }
                        turn = nextTurn;
                        updateStatusDisplay();
                        renderBoard();
                        setTimeout(aiMakeMove, Math.floor(Math.random() * 800) + 1200);
                    } else {
                        update(ref(db, `rooms/${currentRoomId}`), {
                            board: board, turn: nextTurn, gameOver: isOver, winnerRole: winRole, lastMove: lastMove
                        }).catch(e => {});
                    }
                }
                selectedPiece = null; validMoves = [];
                renderBoard();
            } else if (clickedCell.p !== "") {
                if ((isVsAI && isWhitePiece(clickedCell.p)) || (!isVsAI && ((myRole === 'white' && isWhitePiece(clickedCell.p)) || (myRole === 'black' && isBlackPiece(clickedCell.p))))) {
                    selectedPiece = { r, c, cell: clickedCell };
                    validMoves = getValidMovesForBoard(r, c, clickedCell, board);
                    renderBoard();
                }
            }
        }

        window.leaveRoom = async function() {
            if (isCallActive) {
                if (localStream) localStream.getTracks().forEach(t => t.stop());
                if (peerConnection) peerConnection.close();
                peerConnection = null;
                isCallActive = false;
                document.getElementById("callBtn").textContent = "📞 បើកសំឡេងនិយាយគ្នា";
            }
            if (!isVsAI && currentRoomId) {
                remove(ref(db, `rooms/${currentRoomId}/players/${myRole}`)).catch(e => {});
            }
            isVsAI = false; isTournament = false;
            document.getElementById("gameOverModal").classList.add("hidden");
            document.getElementById("game-container").classList.add("hidden");
            document.getElementById("main-menu").classList.remove("hidden");
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_CONTENT

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

