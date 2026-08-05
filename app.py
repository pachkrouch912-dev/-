from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

app = FastAPI()

@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "ok"}

@app.get("/manifest.json")
async def get_manifest():
    return JSONResponse({
        "name": "អុកខ្មែរអនឡាញ - តារាងចំណាត់ថ្នាក់ជើងខ្លាំង",
        "short_name": "អុកខ្មែរ",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a0f18",
        "theme_color": "#1b2838",
        "description": "ហ្គេមអុកខ្មែរអនឡាញ និងប្រកួតដណ្ដើមពិន្ទុចំណាត់ថ្នាក់",
        "id": "OukkhmerRanking",
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
    <title>អុកខ្មែរអនឡាញ - តារាងចំណាត់ថ្នាក់</title>
    
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
            color: #f1c40f; text-shadow: 0 0 10px rgba(241, 196, 15, 0.7);
            font-size: 19px; margin: 4px 0; letter-spacing: 1px;
        }

        .card {
            background: rgba(15, 25, 35, 0.92); backdrop-filter: blur(15px);
            padding: 12px; border-radius: 20px; display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.7), inset 0 0 15px rgba(255,255,255,0.05);
            width: 100%; border: 2px solid rgba(241, 196, 15, 0.3);
            flex-grow: 1; margin: 4px 0;
        }

        .user-profile {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(0,0,0,0.6); padding: 8px 12px; border-radius: 12px;
            margin-bottom: 6px; border: 1px solid rgba(241, 196, 15, 0.2);
            font-size: 13px; font-weight: bold; width: 100%;
        }
        .points-badge { color: #f1c40f; display: flex; align-items: center; gap: 4px; }
        .stats-badge { color: #2ecc71; font-size: 11px; }

        input {
            padding: 10px; font-size: 14px; border: 2px solid #34495e; border-radius: 12px;
            margin: 4px 0; width: 100%; background: rgba(0, 0, 0, 0.6);
            color: #fff; text-align: center; outline: none; transition: 0.3s;
        }
        input:focus { border-color: #f1c40f; box-shadow: 0 0 10px rgba(241,196,15,0.5); }

        button {
            padding: 10px 16px; font-size: 14px; font-weight: 800; text-transform: uppercase;
            color: white; border: none; border-radius: 30px; cursor: pointer; 
            margin: 5px 0; width: 100%; letter-spacing: 0.5px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.4), inset 0 2px 3px rgba(255,255,255,0.4), inset 0 -3px 4px rgba(0,0,0,0.4);
            transition: all 0.2s ease; position: relative; overflow: hidden;
        }
        button:hover { transform: translateY(-2px); filter: brightness(1.15); box-shadow: 0 7px 20px rgba(0,0,0,0.6), inset 0 2px 3px rgba(255,255,255,0.6), inset 0 -3px 4px rgba(0,0,0,0.4); }
        button:active { transform: translateY(2px); box-shadow: 0 2px 8px rgba(0,0,0,0.4), inset 0 2px 2px rgba(0,0,0,0.3); }

        .btn-green { background: linear-gradient(to bottom, #2ecc71, #27ae60); border: 1px solid #1e8449; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
        .btn-blue { background: linear-gradient(to bottom, #3498db, #2980b9); border: 1px solid #1f618d; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
        .btn-red { background: linear-gradient(to bottom, #e74c3c, #c0392b); border: 1px solid #922b21; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
        .btn-gold { background: linear-gradient(to bottom, #f1c40f, #d4ac0d); border: 1px solid #b7950b; color: #111; text-shadow: none; }

        .deco-board-container {
            margin: 4px 0; width: 100%; display: flex; justify-content: center;
            pointer-events: none;
        }
        .deco-board {
            display: grid; grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr); gap: 1px;
            border: 2px solid #34495e; background-color: #34495e;
            border-radius: 8px; width: 130px; height: 130px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .deco-square {
            display: flex; align-items: center; justify-content: center;
            font-size: 11px; user-select: none; width: 100%; height: 100%; position: relative;
        }
        .deco-light { background-color: #95a5a6; color: #2c3e50; }
        .deco-dark { background-color: #34495e; color: #ecf0f1; }
        .deco-boked {
            position: absolute; bottom: 0px; right: 0px; font-size: 4px;
            background: #e74c3c; color: #fff; padding: 0px 1px; border-radius: 2px;
            font-weight: bold;
        }

        .leaderboard-box {
            margin-top: 4px; background: rgba(0, 0, 0, 0.4);
            border-radius: 10px; padding: 6px 8px; border: 1px solid rgba(241, 196, 15, 0.2);
            text-align: left; width: 100%; max-height: 85px; overflow-y: auto;
        }
        .leaderboard-title { color: #f1c40f; font-size: 11px; font-weight: bold; text-align: center; margin-bottom: 2px; }
        .lb-item { display: flex; justify-content: space-between; font-size: 11px; padding: 1px 3px; border-bottom: 1px solid rgba(255,255,255,0.05); }

        #board {
            display: grid; grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr); gap: 1px;
            justify-content: center; margin: 6px auto;
            border: 4px solid #2c3e50; background-color: #2c3e50;
            border-radius: 10px; width: 85vw; height: 85vw; max-width: 350px; max-height: 350px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.7);
        }
        .square {
            display: flex; align-items: center; justify-content: center;
            font-size: 26px; font-weight: bold; cursor: pointer; user-select: none;
            width: 100%; height: 100%; transition: background 0.2s; position: relative;
        }
        .light { background-color: #95a5a6; color: #111; }
        .dark { background-color: #34495e; color: #fff; }
        .selected { background-color: #7b61ff !important; box-shadow: inset 0 0 10px #fff; }
        .highlight { background-color: #2ecc71 !important; }
        
        .last-move {
            background-color: rgba(241, 196, 15, 0.45) !important;
            box-shadow: inset 0 0 8px rgba(241, 196, 15, 0.8);
        }

        .white-piece { color: #ffffff; text-shadow: 0 2px 4px #000; }
        .black-piece { color: #111111; text-shadow: 0 2px 4px #fff; }
        
        .king-warning {
            background-color: #e74c3c !important;
            animation: pulseWarning 0.8s infinite alternate;
            box-shadow: 0 0 15px #e74c3c;
        }
        @keyframes pulseWarning {
            0% { transform: scale(1); filter: brightness(1); }
            100% { transform: scale(1.05); filter: brightness(1.3); }
        }

        .boked-badge {
            position: absolute; bottom: 2px; right: 2px; font-size: 8px;
            background: #e74c3c; color: #fff; padding: 1px 3px; border-radius: 3px;
            font-weight: bold;
        }

        .modal {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); display: flex; justify-content: center; align-items: center;
            z-index: 10; backdrop-filter: blur(5px);
        }
        .modal-content {
            background: #1b2838; border: 2px solid #f1c40f; padding: 20px;
            border-radius: 20px; text-align: center; width: 90%; max-width: 320px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.9);
        }
        .modal-title { font-size: 20px; color: #f1c40f; margin-bottom: 10px; font-weight: bold; }
        .modal-text { font-size: 14px; margin-bottom: 15px; color: #ddd; }

        .hidden { display: none !important; }
        .toggle-text { font-size: 12px; color: #3498db; cursor: pointer; margin-top: 8px; text-decoration: underline; }
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
        <h1>♟️ អុកខ្មែរដណ្ដើមពិន្ទុជើងខ្លាំង ♟️</h1>

        <div id="login-box" class="card hidden">
            <h3 id="auth-title" style="color: #f1c40f; margin: 0 0 10px 0; font-size: 15px;">ចូលគណនីរបស់អ្នក</h3>
            <input type="text" id="usernameInput" placeholder="ឈ្មោះអ្នកលេង (សម្រាប់ចុះឈ្មោះ)" class="hidden">
            <input type="email" id="emailInput" placeholder="អ៊ីមែល (Email)">
            <input type="password" id="passwordInput" placeholder="ពាក្យសម្ងាត់ (Password)">
            
            <button id="authBtn" class="btn-green" onclick="handleAuth()">ចូលគណនី</button>
            <div class="toggle-text" id="toggleAuthMode" onclick="toggleAuthMode()">មិនទាន់មានគណនី? ចុះឈ្មោះថ្មី</div>
        </div>

        <div id="main-menu" class="card hidden">
            <div class="user-profile">
                <div>
                    <span id="welcome-msg" style="color: #f1c40f; display: block;"></span>
                    <span class="stats-badge">ឈ្នះ: <span id="statWins">0</span> | ចាញ់: <span id="statLosses">0</span></span>
                </div>
                <span class="points-badge">⭐ ពិន្ទុ៖ <span id="userPoints">0</span></span>
            </div>

            <div class="deco-board-container">
                <div class="deco-board" id="decoBoard"></div>
            </div>

            <button class="btn-gold" onclick="startTournamentRoom()">🏆 ប្រកួតដណ្ដើមពាន (ជម្រុះយកពិន្ទុខ្ពស់)</button>
            <button class="btn-green" onclick="quickJoinRoom()">⚡ ចូលលេងរហ័ស (ជាមួយ AI)</button>
            <button class="btn-blue" onclick="createPrivateRoom()">🏠 បង្កើតបន្ទប់ផ្ទាល់ខ្លួន</button>
            <input type="text" id="roomCodeInput" placeholder="បញ្ចូលកូដបន្ទប់ (ឧ. Room_1234)">
            <button class="btn-green" onclick="joinPrivateRoom()">🔗 ចូលតាមកូដបន្ទប់</button>
            <button class="btn-red" style="margin-top: 4px; padding: 6px;" onclick="logoutUser()">ចាកចេញពីគណនី</button>

            <div class="leaderboard-box">
                <div class="leaderboard-title">🏆 តារាងចំណាត់ថ្នាក់ពូកែលេងជាងគេ 🏆</div>
                <div id="leaderboardList">កំពុងទាញយក...</div>
            </div>
        </div>

        <div id="game-container" class="card hidden">
            <h3 id="room-title" style="color: #f1c40f; margin: 2px 0; font-size: 13px;">បន្ទប់ប្រកួត</h3>
            <div id="status" style="background: rgba(0,0,0,0.6); padding: 5px 10px; border-radius: 10px; font-size: 12px; font-weight:bold; margin-bottom: 5px; border: 1px solid rgba(255,255,255,0.2);">រង់ចាំគូប្រកួត...</div>
            <div id="board"></div>
            <button class="btn-red" style="width: 100%; margin-top: 5px;" onclick="leaveRoom()">ចាកចេញពីបន្ទប់</button>
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

        window.handleAuth = async function() {
            initAudio();
            const email = document.getElementById("emailInput").value.trim();
            const password = document.getElementById("passwordInput").value.trim();
            const username = document.getElementById("usernameInput").value.trim();

            if (!email || !password) {
                alert("សូមបំពេញអ៊ីមែល និងពាក្យសម្ងាត់ឱ្យបានត្រឹមត្រូវ!");
                return;
            }
            if (isRegisterMode && !username) {
                alert("សូមបញ្ចូលឈ្មោះអ្នកលេងរបស់អ្នក!");
                return;
            }

            try {
                if (isRegisterMode) {
                    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
                    const user = userCredential.user;
                    await set(ref(db, `users/${user.uid}`), { name: username, points: 100, wins: 0, losses: 0 });
                } else {
                    await signInWithEmailAndPassword(auth, email, password);
                }
            } catch (error) {
                alert("មានបញ្ហា៖ " + error.message);
            }
        }

        window.logoutUser = function() {
            signOut(auth);
        }

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
                osc.type = 'sine';
                osc.frequency.setValueAtTime(400, now);
                osc.frequency.exponentialRampToValueAtTime(600, now + 0.1);
                gainNode.gain.setValueAtTime(0.2, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
                osc.start(now); osc.stop(now + 0.1);
            } else if (type === 'capture') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(250, now);
                osc.frequency.exponentialRampToValueAtTime(100, now + 0.15);
                gainNode.gain.setValueAtTime(0.3, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
                osc.start(now); osc.stop(now + 0.15);
            } else if (type === 'warning') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(600, now);
                osc.frequency.setValueAtTime(900, now + 0.12);
                gainNode.gain.setValueAtTime(0.3, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
                osc.start(now); osc.stop(now + 0.35);
            } else if (type === 'win') {
                osc.type = 'square';
                osc.frequency.setValueAtTime(300, now);
                osc.frequency.setValueAtTime(450, now + 0.1);
                gainNode.gain.setValueAtTime(0.25, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
                osc.start(now); osc.stop(now + 0.35);
            } else if (type === 'lose') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(300, now);
                osc.frequency.exponentialRampToValueAtTime(120, now + 0.3);
                gainNode.gain.setValueAtTime(0.25, now);
                gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
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
                document.getElementById("leaderboardList").innerHTML = "<div style='text-align:center; color:#888;'>ផ្អាកតារាងចំណាត់ថ្នាក់បណ្តោះអាសន្ន</div>";
            });
        }
        loadLeaderboard();

        onAuthStateChanged(auth, async (user) => {
            if (user) {
                myUid = user.uid;
                const userRef = ref(db, `users/${myUid}`);
                const snapshot = await get(userRef);

                if (snapshot.exists()) {
                    let data = snapshot.val();
                    rawDisplayName = data.name || "អ្នកលេង";
                    myPoints = data.points ?? 100;
                    myWins = data.wins ?? 0;
                    myLosses = data.losses ?? 0;
                } else {
                    rawDisplayName = user.email.split('@')[0];
                    myPoints = 100; myWins = 0; myLosses = 0;
                    await set(userRef, { name: rawDisplayName, points: myPoints, wins: myWins, losses: myLosses });
                }
                myName = rawDisplayName.replace(/[.#$\/\[\]]/g, "_");

                updateUIStats();
                document.getElementById("login-box").classList.add("hidden");
                document.getElementById("main-menu").classList.remove("hidden");
                document.getElementById("welcome-msg").textContent = `${rawDisplayName}`;
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
            if (tournamentWin) {
                myWins += 1; 
                myPoints += 50; 
                playSound('win');
            } else if (didWin) { 
                myWins += 1; 
                myPoints += 15; 
                playSound('win'); 
            } else { 
                myLosses += 1; 
                myPoints = Math.max(0, myPoints - 10); 
                playSound('lose'); 
            }
            updateUIStats();
            if (myUid) {
                await update(ref(db, `users/${myUid}`), { name: rawDisplayName, points: myPoints, wins: myWins, losses: myLosses }).catch(e => console.log(e));
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
                // ដើរ១ប្រឡោះជុំវិញខ្លួនធម្មតា
                let directions = [[-1,0], [1,0], [0,-1], [0,1], [-1,-1], [-1,1], [1,-1], [1,1]];
                for (let d of directions) {
                    let nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = currentBoard[nr][nc].p;
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) moves.push({r: nr, c: nc});
                    }
                }
                // ក្បួនពិសេសស្ដេចខ្មែរ៖ លោតខ្វែង១ប្រឡោះ (ស្រដៀងគ្រាប់គោ) បន្ថែមប្រសិនបើមិនទាន់ជាប់អ៊ុក
                let jumpingDirections = [[-2, -2], [-2, 2], [2, -2], [2, 2]];
                for (let jd of jumpingDirections) {
                    let nr = r + jd[0], nc = c + jd[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = currentBoard[nr][nc].p;
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) {
                            moves.push({r: nr, c: nc});
                        }
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
                let statusMsg = `វេន៖ ស (អ្នក)`;
                if (isKingInCheck(board, true)) {
                    playSound('warning');
                    statusMsg = `⚠️ ប្រយ័ត្ន! ព្រះរាជា (ស្តេច) របស់អ្នកកំពុងរងគ្រោះថ្នាក់!`;
                }
                document.getElementById("status").textContent = statusMsg;
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
            if (isTournament) {
                startTournamentRoom();
            } else {
                quickJoinRoom();
            }
        }

        window.closeModalAndMenu = function() {
            document.getElementById("gameOverModal").classList.add("hidden");
            window.leaveRoom();
        }

        window.startTournamentRoom = function() {
            initAudio(); 
            isVsAI = true;
            isTournament = true;
            board = JSON.parse(JSON.stringify(initialBoard));
            turn = "white";
            gameOver = false;
            selectedPiece = null;
            validMoves = [];
            lastMove = null;

            document.getElementById("gameOverModal").classList.add("hidden");
            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = `🏆 វគ្គប្រកួតដណ្ដើមពិន្ទុជើងខ្លាំង`;
            document.getElementById("status").textContent = `វេន៖ ស (អ្នក) - ប្រយ័ត្ន! គូប្រកួតខ្លាំងណាស់!`;
            renderBoard();
        }

        window.quickJoinRoom = function() {
            initAudio(); 
            isVsAI = true;
            isTournament = false;
            board = JSON.parse(JSON.stringify(initialBoard));
            turn = "white";
            gameOver = false;
            selectedPiece = null;
            validMoves = [];
            lastMove = null;

            document.getElementById("gameOverModal").classList.add("hidden");
            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = `ប្រកួតរហ័ស (ជាមួយ AI)`;
            document.getElementById("status").textContent = `វេន៖ ស (អ្នក)`;
            renderBoard();
        }

        window.createPrivateRoom = async function() {
            initAudio(); isVsAI = false; isTournament = false;
            try {
                const targetRoom = "Room_" + Math.floor(Math.random() * 9000 + 1000);
                await set(ref(db, `rooms/${targetRoom}`), { board: initialBoard, turn: "white", gameOver: false, message: "រង់ចាំគូប្រកួត...", players: {} });
                await joinRoomProcess(targetRoom);
                alert(`កូដបន្ទប់របស់អ្នក៖ ${targetRoom}`);
            } catch (error) { 
                alert("មានបញ្ហាក្នុងការបង្កើតបន្ទប់!"); 
            }
        }

        window.joinPrivateRoom = async function() {
            initAudio(); isVsAI = false; isTournament = false;
            const rCode = document.getElementById("roomCodeInput").value.trim();
            if (!rCode) { alert("សូមបញ្ចូលកូដបន្ទប់សិន!"); return; }
            try {
                if (!(await get(ref(db, `rooms/${rCode}`))).exists()) { alert("រកមិនឃើញបន្ទប់នេះទេ!"); return; }
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
                else if (!players.black) { myRole = "black"; players.black = myName; }
                else { myRole = "observer"; }

                await update(ref(db, `rooms/${currentRoomId}`), { players: players });
                if (myRole === 'white') onDisconnect(ref(db, `rooms/${currentRoomId}/players/white`)).remove();
                else if (myRole === 'black') onDisconnect(ref(db, `rooms/${currentRoomId}/players/black`)).remove();
            } catch(e) {
                myRole = "white";
            }

            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = `បន្ទប់ប្រកួត (${myRole === 'white' ? 'ស' : 'ខ្មៅ'})`;
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
                        showGameOverModal(didWin ? "🎉 អ្នកឈ្នះហ្គេមនេះហើយ (+15 ពិន្ទុ)!" : "😔 អ្នកបានចាញ់ហ្គេមនេះ (-10 ពិន្ទុ)!", didWin, false);
                    }
                } else { gameOver = data.gameOver; }

                let pCount = Object.keys(data.players || {}).length;
                if (pCount < 2 && !isVsAI) {
                    document.getElementById("status").textContent = `កំពុងរង់ចាំគូប្រកួត...`;
                } else {
                    let defaultMsg = data.message || `វេន៖ ${turn === 'white' ? 'ស' : 'ខ្មៅ'}`;
                    if (myRole !== "observer" && myRole === turn && isKingInCheck(board, myRole === 'white')) {
                        playSound('warning');
                        defaultMsg = `⚠️ ប្រយ័ត្ន! ព្រះរាជា (ស្តេច) របស់អ្នកកំពុងរងគ្រោះថ្នាក់!`;
                    }
                    if(!isVsAI) document.getElementById("status").textContent = defaultMsg;
                }
                selectedPiece = null; validMoves = [];
                renderBoard();
            }, (error) => {
                console.log("Room listener error");
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
                    let nextStatusMsg = `វេន៖ ${nextTurn === 'white' ? 'ស' : 'ខ្មៅ'}`;

                    if (!isOver && isKingInCheck(board, nextTurn === 'white')) {
                        playSound('warning');
                        nextStatusMsg = `⚠️ ប្រយ័ត្ន! ព្រះរាជា (ស្តេច) របស់អ្នកកំពុងរងគ្រោះថ្នាក់!`;
                    }

                    if (isVsAI) {
                        gameOver = isOver;
                        if (gameOver) { 
                            if (isTournament) {
                                showGameOverModal("🏆 អស្ចារ្យណាស់! អ្នកបានឈ្នះការប្រកួតពានរង្វាន់ (+50 ពិន្ទុ)!", true, true);
                            } else {
                                showGameOverModal("🎉 អ្នកឈ្នះគូប្រកួតយ៉ាងអស្ចារ្យ (+15 ពិន្ទុ)!", true, false);
                            }
                            return; 
                        }
                        turn = nextTurn;
                        document.getElementById("status").textContent = `គូប្រកួតកំពុងគិត...`;
                        renderBoard();
                        
                        let randomDelay = Math.floor(Math.random() * 1000) + 1500;
                        setTimeout(aiMakeMove, randomDelay);
                    } else {
                        update(ref(db, `rooms/${currentRoomId}`), {
                            board: board, turn: nextTurn, gameOver: isOver, winnerRole: winRole, message: msg || nextStatusMsg, lastMove: lastMove
                        }).catch(e => console.log(e));
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
            if (!isVsAI && currentRoomId) {
                remove(ref(db, `rooms/${currentRoomId}/players/${myRole}`)).catch(e => {});
            }
            isVsAI = false;
            isTournament = false;
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

