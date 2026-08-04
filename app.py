from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

app = FastAPI()

@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "ok"}

@app.get("/manifest.json")
async def get_manifest():
    return JSONResponse({
        "name": "អុកខ្មែរអនឡាញ - Smart AI & Quick Play",
        "short_name": "អុកខ្មែរ AI",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a0f18",
        "theme_color": "#1b2838",
        "description": "ហ្គេមអុកខ្មែរអនឡាញ ជាមួយប្រព័ន្ធ Quick Play, AI ជំនួយ និងជំនួយការ AI Coach",
        "id": "OukkhmerSmartAI",
        "icons": [
            {
                "src": "https://dummyimage.com/192x192/1b2838/ffffff.png&text=OukAI",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "https://dummyimage.com/512x512/1b2838/ffffff.png&text=OukAI",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

@app.get("/sw.js")
async def get_sw():
    sw_code = """
    self.addEventListener('install', (event) => {
        self.skipWaiting();
    });
    self.addEventListener('activate', (event) => {
        return self.clients.claim();
    });
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
    <title>អុកខ្មែរអនឡាញ - Smart AI & Quick Play</title>
    
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#1b2838">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: radial-gradient(circle at center, #1b2838, #0a0f18);
            text-align: center; margin: 0; padding: 10px; color: #fff; 
            height: 100vh; height: 100dvh; overflow: hidden; 
            display: flex; flex-direction: column; justify-content: center; align-items: center;
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
            position: relative; z-index: 1; width: 100%; max-width: 480px; 
            height: 100%; display: flex; flex-direction: column; justify-content: space-between; 
            padding: 5px;
        }
        
        h1 { 
            color: #f1c40f; text-shadow: 0 0 15px rgba(241, 196, 15, 0.6);
            font-size: 19px; margin: 4px 0; letter-spacing: 1px;
        }

        .card {
            background: rgba(18, 28, 40, 0.85); backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 12px; border-radius: 24px; display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6), inset 0 1px 2px rgba(255,255,255,0.1);
            width: 100%; border: 1px solid rgba(241, 196, 15, 0.25);
            flex-grow: 1; margin: 4px 0;
        }

        .user-profile {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(0,0,0,0.5); padding: 8px 12px; border-radius: 16px;
            margin-bottom: 6px; border: 1px solid rgba(241, 196, 15, 0.15);
            font-size: 13px; font-weight: bold; width: 100%;
        }
        .points-badge { color: #f1c40f; display: flex; align-items: center; gap: 5px; font-size: 13px; }
        .stats-badge { color: #2ecc71; font-size: 11px; margin-top: 2px; display: block; }

        input {
            padding: 10px 14px; font-size: 14px; border: 1px solid rgba(255,255,255,0.15); border-radius: 14px;
            margin: 4px 0; width: 100%; background: rgba(0, 0, 0, 0.4);
            color: #fff; text-align: center; outline: none; transition: all 0.3s ease;
        }
        input:focus { border-color: #f1c40f; box-shadow: 0 0 12px rgba(241,196,15,0.4); background: rgba(0,0,0,0.6); }

        button {
            padding: 11px 16px; font-size: 13px; font-weight: 700;
            color: white; border: none; border-radius: 16px; cursor: pointer; 
            margin: 4px 0; width: 100%; letter-spacing: 0.3px;
            display: flex; align-items: center; justify-content: center; gap: 8px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden;
        }
        button::after {
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: 0.5s;
        }
        button:hover::after { left: 100%; }
        button:hover { transform: translateY(-3px); box-shadow: 0 12px 25px rgba(0,0,0,0.4); filter: brightness(1.1); }
        button:active { transform: translateY(1px); box-shadow: 0 4px 10px rgba(0,0,0,0.3); }

        .btn-green { background: linear-gradient(135deg, #2ecc71, #27ae60); border: 1px solid rgba(46,204,113,0.4); }
        .btn-blue { background: linear-gradient(135deg, #3498db, #2980b9); border: 1px solid rgba(52,152,219,0.4); }
        .btn-red { background: linear-gradient(135deg, #e74c3c, #c0392b); border: 1px solid rgba(231,76,60,0.4); }
        .btn-gold { background: linear-gradient(135deg, #f1c40f, #d4ac0d); border: 1px solid rgba(241,196,15,0.4); color: #111; font-weight: 800; }
        .btn-purple { background: linear-gradient(135deg, #9b59b6, #8e44ad); border: 1px solid rgba(155,89,182,0.4); }
        .btn-google { background: linear-gradient(135deg, #ea4335, #c5221f); border: 1px solid rgba(234,67,53,0.4); }

        .deco-board-container {
            margin: 2px 0; width: 100%; display: flex; justify-content: center; pointer-events: none;
        }
        .deco-board {
            display: grid; grid-template-columns: repeat(8, 1fr); grid-template-rows: repeat(8, 1fr); gap: 1px;
            border: 2px solid rgba(255,255,255,0.1); background-color: #34495e; border-radius: 12px; width: 100px; height: 100px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.4);
        }
        .deco-square { display: flex; align-items: center; justify-content: center; font-size: 9px; user-select: none; position: relative; }
        .deco-light { background-color: #95a5a6; color: #2c3e50; }
        .deco-dark { background-color: #34495e; color: #ecf0f1; }
        .deco-boked { position: absolute; bottom: 0px; right: 0px; font-size: 3px; background: #e74c3c; color: #fff; padding: 0px 1px; border-radius: 2px; font-weight: bold; }

        .leaderboard-box {
            margin-top: 4px; background: rgba(0, 0, 0, 0.35); border-radius: 14px; padding: 6px 8px; 
            border: 1px solid rgba(241, 196, 15, 0.15); text-align: left; width: 100%; max-height: 80px; overflow-y: auto;
        }
        .leaderboard-title { color: #f1c40f; font-size: 10px; font-weight: bold; text-align: center; margin-bottom: 3px; }
        .lb-item { display: flex; justify-content: space-between; font-size: 10px; padding: 1px 3px; border-bottom: 1px solid rgba(255,255,255,0.04); }

        #board {
            display: grid; grid-template-columns: repeat(8, 1fr); grid-template-rows: repeat(8, 1fr); gap: 1px;
            justify-content: center; margin: 4px auto; border: 4px solid #2c3e50; background-color: #2c3e50;
            border-radius: 12px; width: 78vw; height: 78vw; max-width: 310px; max-height: 310px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.7);
        }
        .square {
            display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; 
            cursor: pointer; user-select: none; width: 100%; height: 100%; transition: background 0.2s; position: relative;
        }
        .light { background-color: #95a5a6; color: #111; }
        .dark { background-color: #34495e; color: #fff; }
        .selected { background-color: #7b61ff !important; box-shadow: inset 0 0 10px #fff; }
        .highlight { background-color: #2ecc71 !important; }
        .last-move { background-color: rgba(241, 196, 15, 0.45) !important; box-shadow: inset 0 0 8px rgba(241, 196, 15, 0.8); }

        .white-piece { color: #ffffff; text-shadow: 0 2px 4px #000; }
        .black-piece { color: #111111; text-shadow: 0 2px 4px #fff; }
        
        .king-warning {
            background-color: #e74c3c !important; animation: pulseWarning 0.8s infinite alternate; box-shadow: 0 0 15px #e74c3c;
        }
        @keyframes pulseWarning {
            0% { transform: scale(1); filter: brightness(1); }
            100% { transform: scale(1.05); filter: brightness(1.3); }
        }

        .boked-badge {
            position: absolute; bottom: 2px; right: 2px; font-size: 7px;
            background: #e74c3c; color: #fff; padding: 1px 2px; border-radius: 3px; font-weight: bold;
        }

        /* AI Coach Dialogue & Box */
        .ai-coach-box {
            background: rgba(155, 89, 182, 0.15); border: 1px solid rgba(155, 89, 182, 0.4);
            border-radius: 12px; padding: 6px 10px; margin: 4px 0; font-size: 11px; text-align: left;
            display: flex; align-items: center; gap: 8px; width: 100%;
        }

        .modal {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); display: flex; justify-content: center; align-items: center;
            z-index: 10; backdrop-filter: blur(8px);
        }
        .modal-content {
            background: #1b2838; border: 1px solid rgba(241,196,15,0.4); padding: 20px;
            border-radius: 24px; text-align: center; width: 90%; max-width: 310px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.9);
        }
        .modal-title { font-size: 18px; color: #f1c40f; margin-bottom: 8px; font-weight: bold; }
        .modal-text { font-size: 13px; margin-bottom: 14px; color: #ddd; }

        .hidden { display: none !important; }
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
        <h1>♟️ អុកខ្មែរ Smart AI & Quick Play ♟️</h1>

        <div id="login-box" class="card hidden">
            <h3 style="color: #f1c40f; margin: 0 0 12px 0; font-size: 15px;">សូមចូលរួមលេងហ្គេម</h3>
            <button class="btn-google" onclick="loginWithGoogle()">
                <span>🌐</span> ចូលគណនីជាមួយ Google
            </button>
        </div>

        <div id="main-menu" class="card hidden">
            <div class="user-profile">
                <div>
                    <span id="welcome-msg" style="color: #f1c40f; display: block; font-size: 13px;"></span>
                    <span class="stats-badge">ឈ្នះ: <span id="statWins">0</span> | ចាញ់: <span id="statLosses">0</span></span>
                </div>
                <span class="points-badge">⭐ <span id="userPoints">0</span> ពិន្ទុ</span>
            </div>

            <div class="deco-board-container">
                <div class="deco-board" id="decoBoard"></div>
            </div>

            <button class="btn-gold" onclick="startQuickPlay()">⚡ ស្វែងរកគូប្រកួត (Quick Play)</button>
            <button class="btn-blue" onclick="createPrivateRoom()">🏠 បង្កើតបន្ទប់ផ្ទាល់ខ្លួន</button>
            <input type="text" id="roomCodeInput" placeholder="បញ្ចូលកូដបន្ទប់ (ឧ. Room_1234)">
            <button class="btn-green" onclick="joinPrivateRoom()">🔗 ចូលតាមកូដបន្ទប់</button>

            <div class="leaderboard-box">
                <div class="leaderboard-title">🏆 តារាងចំណាត់ថ្នាក់ពូកែលេងជាងគេ 🏆</div>
                <div id="leaderboardList">កំពុងទាញយក...</div>
            </div>
        </div>

        <div id="game-container" class="card hidden">
            <h3 id="room-title" style="color: #f1c40f; margin: 2px 0; font-size: 12px;">បន្ទប់ប្រកួត</h3>
            <div id="status" style="background: rgba(0,0,0,0.5); padding: 5px 8px; border-radius: 10px; font-size: 11px; font-weight:bold; margin-bottom: 4px; border: 1px solid rgba(255,255,255,0.15);">រង់ចាំគូប្រកួត...</div>
            
            <div id="aiCoachBox" class="ai-coach-box hidden">
                <span>🤖</span>
                <div>
                    <strong style="color: #9b59b6; display: block;">AI គ្រូបង្វឹកណែនាំ៖</strong>
                    <span id="aiCoachText">ចុចប៊ូតុងខាងក្រោមដើម្បីសុំយោបល់ក្បាច់ដើរ!</span>
                </div>
            </div>

            <div id="board"></div>

            <div style="display: flex; gap: 4px; width: 100%;">
                <button id="aiHintBtn" class="btn-purple hidden" style="flex: 1; margin: 4px 0;" onclick="getAIHint()">💡 សុំយោបល់ AI</button>
                <button class="btn-red" style="flex: 1; margin: 4px 0;" onclick="leaveRoom()">🚪 ចាកចេញ</button>
            </div>
        </div>
    </div>

    <div id="gameOverModal" class="modal hidden">
        <div class="modal-content">
            <div class="modal-title" id="modalTitle">លទ្ធផលហ្គេម</div>
            <div class="modal-text" id="modalText">តើអ្នកចង់លេងម្ដងទៀតទេ?</div>
            <button class="btn-green" onclick="closeModalAndMenu()">🏠 ត្រឡប់ទៅមីនុយដើម</button>
        </div>
    </div>

    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
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
        const googleProvider = new GoogleAuthProvider();

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

        function speakAI(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                let utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'km-KH';
                utterance.rate = 1.0;
                window.speechSynthesis.speak(utterance);
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
        let turn = "white", gameOver = false, selectedPiece = null, validMoves = [];
        let lastMove = null, isPlayingAI = false;

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
                if (!snapshot.exists()) {
                    lbEl.innerHTML = "<div style='text-align:center; color:#888;'>មិនទាន់មានទិន្នន័យ</div>";
                    return;
                }
                let usersData = snapshot.val();
                let usersArray = [];
                for (let u in usersData) {
                    usersArray.push({ name: usersData[u].name || "អ្នកលេង", points: usersData[u].points || 0 });
                }
                usersArray.sort((a, b) => b.points - a.points);
                lbEl.innerHTML = "";
                usersArray.slice(0, 5).forEach((user, index) => {
                    let rankIcon = index === 0 ? "🥇" : (index === 1 ? "🥈" : (index === 2 ? "🥉" : `🏅 #${index+1}`));
                    let item = document.createElement("div");
                    item.className = "lb-item";
                    item.innerHTML = `<span>${rankIcon} ${user.name}</span> <span style="color:#f1c40f;">⭐ ${user.points} ពិន្ទុ</span>`;
                    lbEl.appendChild(item);
                });
            }, (error) => {
                document.getElementById("leaderboardList").innerHTML = "<div style='text-align:center; color:#888;'>ផ្អាកតារាងចំណាត់ថ្នាក់</div>";
            });
        }
        loadLeaderboard();

        onAuthStateChanged(auth, async (user) => {
            if (user) {
                myUid = user.uid;
                rawDisplayName = user.displayName || "Google User";
                myName = rawDisplayName.replace(/[.#$\/\[\]]/g, "_");

                const userRef = ref(db, `users/${myUid}`);
                const snapshot = await get(userRef);

                if (snapshot.exists()) {
                    let data = snapshot.val();
                    myPoints = data.points ?? 100;
                    myWins = data.wins ?? 0;
                    myLosses = data.losses ?? 0;
                } else {
                    myPoints = 100; myWins = 0; myLosses = 0;
                    await set(userRef, { name: rawDisplayName, points: myPoints, wins: myWins, losses: myLosses });
                }

                updateUIStats();
                document.getElementById("login-box").classList.add("hidden");
                document.getElementById("main-menu").classList.remove("hidden");
                document.getElementById("welcome-msg").textContent = `${rawDisplayName}`;
            } else {
                document.getElementById("login-box").classList.remove("hidden");
                document.getElementById("main-menu").classList.add("hidden");
            }
        });

        window.loginWithGoogle = async function() {
            initAudio();
            try {
                await signInWithPopup(auth, googleProvider);
            } catch (error) {
                alert("ការចូលគណនី Google មានបញ្ហា៖ " + error.message);
            }
        }

        function updateUIStats() {
            document.getElementById("userPoints").textContent = myPoints;
            document.getElementById("statWins").textContent = myWins;
            document.getElementById("statLosses").textContent = myLosses;
        }

        async function recordGameResult(didWin) {
            if (didWin) { 
                myWins += 1; myPoints += 15; playSound('win'); 
                if(isPlayingAI) speakAI("អបអរសាទរ! អ្នកបានយកឈ្នះ AI យ៉ាងអស្ចារ្យ។");
            } else { 
                myLosses += 1; myPoints = Math.max(0, myPoints - 10); playSound('lose'); 
                if(isPlayingAI) speakAI("គួរឱ្យស្តាយ! អ្នកបានចាញ់ AI ព្យាយាមម្តងទៀតណា។");
            }
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

        function showGameOverModal(message, didWin) {
            document.getElementById("modalTitle").textContent = didWin ? "🎉 អបអរសាទរ!" : "😢 ចាញ់បាត់ហើយ!";
            document.getElementById("modalText").textContent = message;
            document.getElementById("gameOverModal").classList.remove("hidden");
            recordGameResult(didWin);
        }

        window.closeModalAndMenu = function() {
            document.getElementById("gameOverModal").classList.add("hidden");
            window.leaveRoom();
        }

        // --- SMART QUICK PLAY LOGIC ---
        window.startQuickPlay = async function() {
            initAudio();
            try {
                const roomsSnap = await get(ref(db, 'rooms'));
                let availableRoom = null;
                if (roomsSnap.exists()) {
                    let rooms = roomsSnap.val();
                    for (let rId in rooms) {
                        let room = rooms[rId];
                        if (!room.gameOver && room.players) {
                            let pCount = Object.keys(room.players).length;
                            if (pCount === 1 && !room.isAI) {
                                availableRoom = rId;
                                break;
                            }
                        }
                    }
                }

                if (availableRoom) {
                    isPlayingAI = false;
                    await joinRoomProcess(availableRoom);
                } else {
                    // No human available, match with AI!
                    isPlayingAI = true;
                    const aiRoomId = "AI_Room_" + Math.floor(Math.random() * 9000 + 1000);
                    await set(ref(db, `rooms/${aiRoomId}`), {
                        board: initialBoard, turn: "white", gameOver: false,
                        message: "ប្រកួតជាមួយ AI ឆ្លាតវៃ!", players: { white: myName }, isAI: true
                    });
                    await joinRoomProcess(aiRoomId);
                    speakAI("សួស្តី! ខ្ញុំជាគ្រូបង្វឹក និងជាគូប្រកួត AI របស់អ្នក។ សូមចាប់ផ្តើមដើរមក!");
                }
            } catch(e) {
                alert("មានបញ្ហាក្នុងការស្វែងរកគូប្រកួត!");
            }
        }

        window.createPrivateRoom = async function() {
            initAudio();
            try {
                isPlayingAI = false;
                const targetRoom = "Room_" + Math.floor(Math.random() * 9000 + 1000);
                await set(ref(db, `rooms/${targetRoom}`), { board: initialBoard, turn: "white", gameOver: false, message: "រង់ចាំគូប្រកួត...", players: {}, isAI: false });
                await joinRoomProcess(targetRoom);
                alert(`កូដបន្ទប់របស់អ្នក៖ ${targetRoom}`);
            } catch (error) { 
                alert("មានបញ្ហាក្នុងការបង្កើតបន្ទប់!"); 
            }
        }

        window.joinPrivateRoom = async function() {
            initAudio();
            const rCode = document.getElementById("roomCodeInput").value.trim();
            if (!rCode) { alert("សូមបញ្ចូលកូដបន្ទប់សិន!"); return; }
            try {
                const rSnap = await get(ref(db, `rooms/${rCode}`));
                if (!rSnap.exists()) { alert("រកមិនឃើញបន្ទប់នេះទេ!"); return; }
                isPlayingAI = rSnap.val().isAI || false;
                await joinRoomProcess(rCode);
            } catch(e) {
                alert("មានបញ្ហាក្នុងការចូលបន្ទប់!");
            }
        }

        async function joinRoomProcess(roomId) {
            currentRoomId = roomId;
            try {
                const pSnap = await get(ref(db, `rooms/${currentRoomId}/players`));
                let players = pSnap.exists() ? pSnap.val() : {};
                if (!players.white) { myRole = "white"; players.white = myName; }
                else if (!players.black && !isPlayingAI) { myRole = "black"; players.black = myName; }
                else if (isPlayingAI) { myRole = "white"; }
                else { myRole = "observer"; }

                await update(ref(db, `rooms/${currentRoomId}`), { players: players });
                if (myRole === 'white' && !isPlayingAI) onDisconnect(ref(db, `rooms/${currentRoomId}/players/white`)).remove();
                else if (myRole === 'black' && !isPlayingAI) onDisconnect(ref(db, `rooms/${currentRoomId}/players/black`)).remove();
            } catch(e) {
                myRole = "white";
            }

            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = isPlayingAI ? `ប្រកួតជាមួយ AI ជំនួយ` : `បន្ទប់ប្រកួត (${myRole === 'white' ? 'ស' : 'ខ្មៅ'})`;
            
            if(isPlayingAI) {
                document.getElementById("aiCoachBox").classList.remove("hidden");
                document.getElementById("aiHintBtn").classList.remove("hidden");
            } else {
                document.getElementById("aiCoachBox").classList.add("hidden");
                document.getElementById("aiHintBtn").classList.add("hidden");
            }

            listenToRoom();
            renderBoard();
        }

        function listenToRoom() {
            onValue(ref(db, `rooms/${currentRoomId}`), async (snapshot) => {
                if (!snapshot.exists()) return;
                const data = snapshot.val();
                if (!data.players || Object.keys(data.players).length === 0) { await remove(ref(db, `rooms/${currentRoomId}`)); return; }

                board = data.board; turn = data.turn;
                lastMove = data.lastMove || null;

                if (data.gameOver && !gameOver) {
                    gameOver = true;
                    if (myRole !== "observer") {
                        let didWin = (data.winnerRole === myRole);
                        showGameOverModal(didWin ? "🎉 អ្នកឈ្នះហ្គេមនេះហើយ (+15 ពិន្ទុ)!" : "😔 អ្នកបានចាញ់ហ្គេមនេះ (-10 ពិន្ទុ)!", didWin);
                    }
                } else { gameOver = data.gameOver; }

                let pCount = Object.keys(data.players || {}).length;
                if (pCount < 2 && !isPlayingAI) {
                    document.getElementById("status").textContent = `កំពុងរង់ចាំគូប្រកួត...`;
                } else {
                    let defaultMsg = data.message || `វេន៖ ${turn === 'white' ? 'ស' : 'ខ្មៅ'}`;
                    if (myRole !== "observer" && myRole === turn && isKingInCheck(board, myRole === 'white')) {
                        playSound('warning');
                        defaultMsg = `⚠️ ប្រយ័ត្ន! ព្រះរាជា (ស្តេច) របស់អ្នកកំពុងរងគ្រោះថ្នាក់!`;
                    }
                    document.getElementById("status").textContent = defaultMsg;
                }
                selectedPiece = null; validMoves = [];
                renderBoard();

                // Trigger AI Turn if playing AI and it's black's turn
                if (isPlayingAI && turn === 'black' && !gameOver) {
                    setTimeout(() => makeAIMove(), 800);
                }
            }, (error) => {});
        }

        // --- ADVANCED AI COACH & HINT SYSTEM ---
        window.getAIHint = function() {
            initAudio();
            let allMyMoves = getAllValidMovesForColor(board, myRole === 'white');
            if (allMyMoves.length === 0) return;
            
            // Pick a smart strategic move or random valid move
            let bestMove = allMyMoves[Math.floor(Math.random() * allMyMoves.length)];
            let pieceSymbol = board[bestMove.fromR][bestMove.fromC].p;
            let hintText = `យោបល់៖ សូមរំកិលគ្រាប់ [${pieceSymbol}] របស់អ្នកទៅកាន់ទីតាំងជួរទី ${bestMove.toR + 1} ខ្ទង់ទី ${bestMove.toC + 1} គឺជាការប្រសើរ!`;
            
            document.getElementById("aiCoachText").textContent = hintText;
            speakAI("ខ្ញុំបានរកឃើញក្បាច់ដើរល្អសម្រាប់អ្នកហើយ៖ " + hintText);

            // Highlight hint temporarily on board
            validMoves = [{r: bestMove.toR, c: bestMove.toC}];
            selectedPiece = { r: bestMove.fromR, c: bestMove.fromC, cell: board[bestMove.fromR][bestMove.fromC] };
            renderBoard();
        }

        async function makeAIMove() {
            if (gameOver) return;
            let aiMoves = getAllValidMovesForColor(board, false);
            if (aiMoves.length === 0) return;

            // Simple AI Strategy: Prioritize captures or random valid move
            let move = aiMoves[Math.floor(Math.random() * aiMoves.length)];
            let targetPiece = board[move.toR][move.toC].p;
            let movingCell = board[move.fromR][move.fromC];

            if (targetPiece !== "") playSound('capture'); else playSound('move');
            let isOver = false, msg = "", winRole = "";

            if (targetPiece === "♔") { isOver = true; msg = "🎉 AI ឈ្នះការប្រកួតនេះ!"; winRole = "black"; }

            let isBokedNow = movingCell.b;
            if (movingCell.p === "♟" && move.toR === 5) isBokedNow = true;

            board[move.toR][move.toC] = { p: movingCell.p, b: isBokedNow };
            board[move.fromR][move.fromC] = { p: "", b: false };
            lastMove = { fromR: move.fromR, fromC: move.fromC, toR: move.toR, toC: move.toC };

            let nextTurn = 'white';
            let nextStatusMsg = `វេន៖ ស (អ្នក)`;

            if (!isOver && isKingInCheck(board, true)) {
                playSound('warning');
                nextStatusMsg = `⚠️ ប្រយ័ត្ន! ព្រះរាជា (ស្តេច) របស់អ្នកកំពុងរងគ្រោះថ្នាក់!`;
                document.getElementById("aiCoachText").textContent = "ប្រយ័ត្ន! ព្រះរាជារបស់អ្នកកំពុងត្រូវគេគំរាមកំហែងហើយ!";
                speakAI("ប្រយ័ត្ន! ព្រះរាជារបស់អ្នកកំពុងរងគ្រោះថ្នាក់។");
            }

            await update(ref(db, `rooms/${currentRoomId}`), {
                board: board, turn: nextTurn, gameOver: isOver, winnerRole: winRole, message: msg || nextStatusMsg, lastMove: lastMove
            });
        }

        window.renderBoard = function() {
            const boardEl = document.getElementById("board");
            if (!boardEl) return;
            boardEl.innerHTML = "";
            let kingInCheckPos = isKingInCheck(board, turn === 'white') ? findKingPosition(board, turn === 'white') : null;

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
            if (turn !== myRole) return;
            if (isPlayingAI && turn === 'black') return;

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
                    let nextStatusMsg = isPlayingAI ? "AI កំពុងគិត..." : `វេន៖ ${nextTurn === 'white' ? 'ស' : 'ខ្មៅ'}`;

                    if (!isOver && isKingInCheck(board, nextTurn === 'white')) {
                        playSound('warning');
                        nextStatusMsg = `⚠️ ប្រយ័ត្ន! ព្រះរាជា (ស្តេច) របស់អ្នកកំពុងរងគ្រោះថ្នាក់!`;
                    }

                    update(ref(db, `rooms/${currentRoomId}`), {
                        board: board, turn: nextTurn, gameOver: isOver, winnerRole: winRole, message: msg || nextStatusMsg, lastMove: lastMove
                    }).catch(e => {});
                }
                selectedPiece = null; validMoves = [];
                renderBoard();
            } else if (clickedCell.p !== "") {
                if ((myRole === 'white' && isWhitePiece(clickedCell.p)) || (myRole === 'black' && isBlackPiece(clickedCell.p))) {
                    selectedPiece = { r, c, cell: clickedCell };
                    validMoves = getValidMovesForBoard(r, c, clickedCell, board);
                    renderBoard();
                }
            }
        }

        window.leaveRoom = async function() {
            if (currentRoomId && !isPlayingAI) {
                remove(ref(db, `rooms/${currentRoomId}/players/${myRole}`)).catch(e => {});
            } else if (currentRoomId && isPlayingAI) {
                remove(ref(db, `rooms/${currentRoomId}`)).catch(e => {});
            }
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

