from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>អុកខ្មែរអនឡាញ & AI Bot</title>
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
            position: relative; z-index: 1; width: 100%; max-width: 420px; 
            height: 100%; display: flex; flex-direction: column; justify-content: space-between; 
            padding: 5px 0;
        }
        
        h1 { 
            color: #f1c40f; text-shadow: 0 0 10px rgba(241, 196, 15, 0.7);
            font-size: 18px; margin: 5px 0; letter-spacing: 1px;
        }

        .card {
            background: rgba(15, 25, 35, 0.9); backdrop-filter: blur(15px);
            padding: 12px; border-radius: 16px; display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.7), inset 0 0 10px rgba(255,255,255,0.05);
            width: 100%; border: 2px solid rgba(241, 196, 15, 0.3);
            flex-grow: 1; margin: 5px 0;
        }

        .user-profile {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(0,0,0,0.5); padding: 8px 15px; border-radius: 10px;
            margin-bottom: 6px; border: 1px solid rgba(241, 196, 15, 0.2);
            font-size: 13px; font-weight: bold; width: 100%;
        }
        .coin-badge { color: #f1c40f; display: flex; align-items: center; gap: 4px; }
        .stats-badge { color: #2ecc71; font-size: 11px; }

        input {
            padding: 9px; font-size: 14px; border: 2px solid #34495e; border-radius: 10px;
            margin: 4px 0; width: 100%; background: rgba(0, 0, 0, 0.5);
            color: #fff; text-align: center; outline: none; transition: 0.3s;
        }
        input:focus { border-color: #f1c40f; box-shadow: 0 0 8px rgba(241,196,15,0.4); }

        button {
            padding: 9px 14px; font-size: 13px; font-weight: bold;
            color: white; border: none; border-radius: 10px; cursor: pointer; 
            margin: 4px 0; width: 100%; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: 0.2s;
        }
        button:hover { transform: translateY(-2px); filter: brightness(1.1); }
        button:active { transform: translateY(1px); }

        .btn-green { background: linear-gradient(135deg, #2ecc71, #27ae60); box-shadow: 0 3px 10px rgba(46,204,113,0.4); }
        .btn-blue { background: linear-gradient(135deg, #3498db, #2980b9); box-shadow: 0 3px 10px rgba(52,152,219,0.4); }
        .btn-purple { background: linear-gradient(135deg, #9b59b6, #8e44ad); box-shadow: 0 3px 10px rgba(155,89,182,0.4); }
        .btn-red { background: linear-gradient(135deg, #e74c3c, #c0392b); box-shadow: 0 3px 10px rgba(231,76,60,0.4); }

        .deco-board-container {
            margin: 4px 0; width: 100%; display: flex; justify-content: center;
        }
        .deco-board {
            display: grid; grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr); gap: 1px;
            border: 2px solid #5a3d28; background-color: #5a3d28;
            border-radius: 8px; width: 180px; height: 180px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .deco-square {
            display: flex; align-items: center; justify-content: center;
            font-size: 14px; user-select: none; width: 100%; height: 100%;
        }
        .deco-light { background-color: #f0d9b5; color: #000; }
        .deco-dark { background-color: #b58863; color: #fff; }

        .leaderboard-box {
            margin-top: 4px; background: rgba(0, 0, 0, 0.4);
            border-radius: 10px; padding: 5px 8px; border: 1px solid rgba(241, 196, 15, 0.2);
            text-align: left; width: 100%; max-height: 80px; overflow-y: auto;
        }
        .leaderboard-title { color: #f1c40f; font-size: 11px; font-weight: bold; text-align: center; margin-bottom: 2px; }
        .lb-item { display: flex; justify-content: space-between; font-size: 11px; padding: 1px 3px; border-bottom: 1px solid rgba(255,255,255,0.05); }

        #board {
            display: grid; grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr); gap: 1px;
            justify-content: center; margin: 6px auto;
            border: 4px solid #5a3d28; background-color: #5a3d28;
            border-radius: 8px; width: 270px; height: 270px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        }
        .square {
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: bold; cursor: pointer; user-select: none;
            width: 100%; height: 100%; transition: background 0.2s; position: relative;
        }
        .light { background-color: #f0d9b5; color: #000; }
        .dark { background-color: #b58863; color: #fff; }
        .selected { background-color: #7b61ff !important; box-shadow: inset 0 0 8px #fff; }
        .highlight { background-color: #4cd137 !important; }
        .white-piece { color: #fff; text-shadow: 0 2px 3px #000; }
        .black-piece { color: #111; text-shadow: 0 2px 3px #fff; }
        
        .boked-badge {
            position: absolute; bottom: 1px; right: 1px; font-size: 8px;
            background: #e74c3c; color: #fff; padding: 1px 2px; border-radius: 3px;
            font-weight: bold;
        }

        /* Modal Popup សម្រាប់លទ្ធផលហ្គេម */
        .modal {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center;
            z-index: 10; backdrop-filter: blur(5px);
        }
        .modal-content {
            background: #1b2838; border: 2px solid #f1c40f; padding: 20px;
            border-radius: 16px; text-align: center; width: 85%; max-width: 320px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.9);
        }
        .modal-title { font-size: 20px; color: #f1c40f; margin-bottom: 10px; font-weight: bold; }
        .modal-text { font-size: 14px; margin-bottom: 15px; color: #ddd; }

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
        <h1>♟️ អុកខ្មែរអនឡាញ & AI ♟️</h1>

        <div id="login-box" class="card">
            <h3 style="color: #f1c40f; margin: 0 0 8px 0; font-size: 15px;">ចូលរួមលេងហ្គេម</h3>
            <input type="text" id="playerName" placeholder="បញ្ចូលឈ្មោះរបស់អ្នក">
            <button class="btn-green" onclick="loginUser()">ចូលគណនី</button>
        </div>

        <div id="main-menu" class="card hidden">
            <div class="user-profile">
                <div>
                    <span id="welcome-msg" style="color: #f1c40f; display: block;"></span>
                    <span class="stats-badge">ឈ្នះ: <span id="statWins">0</span> | ចាញ់: <span id="statLosses">0</span></span>
                </div>
                <span class="coin-badge">🪙 <span id="userCoins">0</span></span>
            </div>

            <div class="deco-board-container">
                <div class="deco-board" id="decoBoard"></div>
            </div>

            <button class="btn-purple" onclick="startVsAIGame()">🤖 លេងជាមួយ AI Bot (កម្រិតអស្ចារ្យ)</button>
            <button class="btn-green" onclick="quickJoinRoom()">⚡ ចូលលេងរហ័ស (Quick Match)</button>
            <button class="btn-blue" onclick="createPrivateRoom()">🏠 បង្កើតបន្ទប់ផ្ទាល់ខ្លួន</button>
            <input type="text" id="roomCodeInput" placeholder="បញ្ចូលកូដបន្ទប់ (ឧ. Room_1234)">
            <button class="btn-green" onclick="joinPrivateRoom()">🔗 ចូលតាមកូដបន្ទប់</button>

            <div class="leaderboard-box">
                <div class="leaderboard-title">🏆 តារាងជើងខ្លាំងប្រចាំសង្វៀន 🏆</div>
                <div id="leaderboardList">កំពុងទាញយក...</div>
            </div>
        </div>

        <div id="game-container" class="card hidden">
            <h3 id="room-title" style="color: #f1c40f; margin: 2px 0; font-size: 13px;">បន្ទប់ប្រកួត</h3>
            <div id="status" style="background: rgba(0,0,0,0.6); padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight:bold; margin-bottom: 4px; border: 1px solid rgba(255,255,255,0.2);">រង់ចាំគូប្រកួត...</div>
            <div id="board"></div>
            <button class="btn-red" style="width: 100%; margin-top: 4px;" onclick="leaveRoom()">ចាកចេញពីបន្ទប់</button>
        </div>
    </div>

    <!-- ផ្ទាំងលទ្ធផល និងប៊ូតុងលេងម្ដងទៀត -->
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
        import { getDatabase, ref, set, get, update, onValue, remove, onDisconnect } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";

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
        const db = getDatabase(app);

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

        let myName = "";
        let rawDisplayName = "";
        let myCoins = 0;
        let myWins = 0;
        let myLosses = 0;
        let currentRoomId = "";
        let myRole = ""; 
        let board = JSON.parse(JSON.stringify(initialBoard));
        let turn = "white";
        let gameOver = false;
        let selectedPiece = null;
        let validMoves = [];
        let isVsAI = false;

        function renderDecoBoard() {
            const decoEl = document.getElementById("decoBoard");
            if (!decoEl) return;
            decoEl.innerHTML = "";
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const sq = document.createElement("div");
                    sq.className = "deco-square " + ((r + c) % 2 === 0 ? "deco-light" : "deco-dark");
                    let cell = initialBoard[r][c];
                    if (cell.p !== "") {
                        sq.textContent = cell.p;
                        sq.style.color = ["♖", "♘", "♗", "♕", "♔", "♙"].includes(cell.p) ? "#fff" : "#111";
                    }
                    decoEl.appendChild(sq);
                }
            }
        }
        renderDecoBoard();

        function loadLeaderboard() {
            const usersRef = ref(db, 'users');
            onValue(usersRef, (snapshot) => {
                const lbEl = document.getElementById("leaderboardList");
                if (!lbEl) return;
                if (!snapshot.exists()) {
                    lbEl.innerHTML = "<div style='text-align:center; color:#888;'>មិនទាន់មានទិន្នន័យ</div>";
                    return;
                }
                let usersData = snapshot.val();
                let usersArray = [];
                for (let u in usersData) {
                    usersArray.push({
                        name: usersData[u].name || u,
                        coins: usersData[u].coins || 0
                    });
                }
                usersArray.sort((a, b) => b.coins - a.coins);

                lbEl.innerHTML = "";
                usersArray.slice(0, 3).forEach((user, index) => {
                    let rankIcon = index === 0 ? "🥇" : (index === 1 ? "🥈" : "🥉");
                    let item = document.createElement("div");
                    item.className = "lb-item";
                    item.innerHTML = `<span>${rankIcon} ${user.name}</span> <span style="color:#f1c40f;">🪙 ${user.coins}</span>`;
                    lbEl.appendChild(item);
                });
            });
        }

        window.loginUser = async function() {
            rawDisplayName = document.getElementById("playerName").value.trim();
            if (!rawDisplayName) { alert("សូមបញ្ចូលឈ្មោះរបស់អ្នក!"); return; }
            myName = rawDisplayName.replace(/[.#$\/\[\]]/g, "_");

            const userRef = ref(db, `users/${myName}`);
            const userSnap = await get(userRef);

            if (userSnap.exists()) {
                myCoins = userSnap.val().coins || 1000;
                myWins = userSnap.val().wins || 0;
                myLosses = userSnap.val().losses || 0;
            } else {
                myCoins = 1000; 
                myWins = 0;
                myLosses = 0;
                await set(userRef, { name: rawDisplayName, coins: myCoins, wins: myWins, losses: myLosses });
            }

            updateUIStats();
            document.getElementById("login-box").classList.add("hidden");
            document.getElementById("main-menu").classList.remove("hidden");
            document.getElementById("welcome-msg").textContent = `${rawDisplayName}`;

            loadLeaderboard();
        }

        function updateUIStats() {
            document.getElementById("userCoins").textContent = myCoins;
            document.getElementById("statWins").textContent = myWins;
            document.getElementById("statLosses").textContent = myLosses;
        }

        async function recordGameResult(didWin) {
            if (didWin) {
                myWins += 1;
                myCoins += 100;
            } else {
                myLosses += 1;
                myCoins = Math.max(0, myCoins - 100);
            }
            updateUIStats();
            await update(ref(db, `users/${myName}`), { coins: myCoins, wins: myWins, losses: myLosses });
        }

        // ================= AI BOT LOGIC =================
        window.startVsAIGame = function() {
            isVsAI = true;
            myRole = "white";
            board = JSON.parse(JSON.stringify(initialBoard));
            turn = "white";
            gameOver = false;
            selectedPiece = null;
            validMoves = [];

            document.getElementById("gameOverModal").classList.add("hidden");
            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = `ប្រកួតទល់នឹង AI Bot (កម្រិតអស្ចារ្យ)`;
            document.getElementById("status").textContent = `វេន៖ ស (អ្នក)`;
            renderBoard();
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
                        for (let m of moves) {
                            allMoves.push({fromR: r, fromC: c, toR: m.r, toC: m.c});
                        }
                    }
                }
            }
            return allMoves;
        }

        function getValidMovesForBoard(r, c, cell, currentBoard) {
            let moves = [];
            let piece = cell.p;
            let isWhite = isWhitePiece(piece);

            if (piece === "♔" || piece === "♚") {
                let directions = [[-1,0], [1,0], [0,-1], [0,1], [-1,-1], [-1,1], [1,-1], [1,1]];
                for (let d of directions) {
                    let nr = r + d[0], nc = c + d[1];
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
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) {
                            moves.push({r: nr, c: nc});
                        }
                    }
                }
            } else if (piece === "♗" || piece === "♝") {
                let directions = isWhite ? [[-1,0], [-1,-1], [-1,1], [1,-1], [1,1]] : [[1,0], [-1,-1], [-1,1], [1,-1], [1,1]];
                for (let d of directions) {
                    let nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = currentBoard[nr][nc].p;
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) {
                            moves.push({r: nr, c: nc});
                        }
                    }
                }
            } else if (piece === "♘" || piece === "♞") {
                let jmps = [[-2,-1], [-2,1], [-1,-2], [-1,2], [1,-2], [1,2], [2,-1], [2,1]];
                for (let d of jmps) {
                    let nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = currentBoard[nr][nc].p;
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) {
                            moves.push({r: nr, c: nc});
                        }
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
                        if (target === "") {
                            moves.push({r: nr, c: nc});
                        } else {
                            if ((isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) {
                                moves.push({r: nr, c: nc});
                            }
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
                            if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) {
                                moves.push({r: nr, c: nc});
                            }
                        }
                    }
                } else {
                    let fwd = isWhite ? -1 : 1;
                    let nr = r + fwd, nc = c;
                    if (nr >= 0 && nr < 8 && currentBoard[nr][nc].p === "") {
                        moves.push({r: nr, c: nc});
                    }
                    let leftCol = c - 1;
                    let rightCol = c + 1;
                    if (nr >= 0 && nr < 8) {
                        if (leftCol >= 0) {
                            let targetLeft = currentBoard[nr][leftCol].p;
                            if (targetLeft !== "" && ((isWhite && isBlackPiece(targetLeft)) || (!isWhite && isWhitePiece(targetLeft)))) {
                                moves.push({r: nr, c: leftCol});
                            }
                        }
                        if (rightCol < 8) {
                            let targetRight = currentBoard[nr][rightCol].p;
                            if (targetRight !== "" && ((isWhite && isBlackPiece(targetRight)) || (!isWhite && isWhitePiece(targetRight)))) {
                                moves.push({r: nr, c: rightCol});
                            }
                        }
                    }
                }
            }
            return moves;
        }

        function evaluateBoard(currentBoard) {
            let score = 0;
            const values = { "♟": 10, "♙": -10, "♞": 30, "♘": -30, "♝": 30, "♗": -30, "♜": 50, "♖": -50, "♛": 90, "♕": -90, "♚": 1000, "♔": -1000 };
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    let p = currentBoard[r][c].p;
                    if (values[p] !== undefined) {
                        score += values[p];
                        if (currentBoard[r][c].b) {
                            score += (p === "♟" ? 20 : -20);
                        }
                    }
                }
            }
            return score;
        }

        function minimax(currentBoard, depth, alpha, beta, isMaximizing) {
            if (depth === 0) return evaluateBoard(currentBoard);

            let allMoves = getAllValidMovesForColor(currentBoard, !isMaximizing);
            if (allMoves.length === 0) return evaluateBoard(currentBoard);

            if (isMaximizing) {
                let maxEval = -Infinity;
                for (let m of allMoves) {
                    let tempBoard = JSON.parse(JSON.stringify(currentBoard));
                    let movingCell = tempBoard[m.fromR][m.fromC];
                    let target = tempBoard[m.toR][m.toC].p;
                    if (target === "♔") return 10000;

                    let isBokedNow = movingCell.b;
                    if (movingCell.p === "♟" && m.toR === 7) isBokedNow = true;

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
                    let target = tempBoard[m.toR][m.toC].p;
                    if (target === "♚") return -10000;

                    let isBokedNow = movingCell.b;
                    if (movingCell.p === "♙" && m.toR === 0) isBokedNow = true;

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

            let bestEval = -Infinity;
            let bestMove = allMoves[0];

            for (let m of allMoves) {
                let tempBoard = JSON.parse(JSON.stringify(board));
                let movingCell = tempBoard[m.fromR][m.fromC];
                let target = tempBoard[m.toR][m.toC].p;
                if (target === "♔") {
                    bestMove = m;
                    break;
                }

                let isBokedNow = movingCell.b;
                if (movingCell.p === "♟" && m.toR === 7) isBokedNow = true;

                tempBoard[m.toR][m.toC] = { p: movingCell.p, b: isBokedNow };
                tempBoard[m.fromR][m.fromC] = { p: "", b: false };

                let evalScore = minimax(tempBoard, 2, -Infinity, Infinity, false);
                if (evalScore > bestEval) {
                    bestEval = evalScore;
                    bestMove = m;
                }
            }

            let movingCell = board[bestMove.fromR][bestMove.fromC];
            let targetPiece = board[bestMove.toR][bestMove.toC].p;
            
            let isBokedNow = movingCell.b;
            if (movingCell.p === "♟" && bestMove.toR === 7) isBokedNow = true;

            board[bestMove.toR][bestMove.toC] = { p: movingCell.p, b: isBokedNow };
            board[bestMove.fromR][bestMove.fromC] = { p: "", b: false };

            if (targetPiece === "♔") {
                gameOver = true;
                showGameOverModal("😔 អ្នកបានចាញ់ AI Bot!", false);
            } else {
                turn = "white";
                document.getElementById("status").textContent = `វេន៖ ស (អ្នក)`;
            }
            renderBoard();
        }

        function showGameOverModal(message, didWin) {
            document.getElementById("modalTitle").textContent = didWin ? "🎉 អបអរសាទរ!" : "😢 ចាញ់បាត់ហើយ!";
            document.getElementById("modalText").textContent = message;
            document.getElementById("gameOverModal").classList.remove("hidden");
            recordGameResult(didWin);
        }

        window.playAgain = function() {
            if (isVsAI) {
                startVsAIGame();
            } else {
                quickJoinRoom();
            }
        }

        window.closeModalAndMenu = function() {
            document.getElementById("gameOverModal").classList.add("hidden");
            window.leaveRoom();
        }

        // ================= STANDARD MULTIPLAYER =================
        window.quickJoinRoom = async function() {
            isVsAI = false;
            document.getElementById("gameOverModal").classList.add("hidden");
            try {
                const roomsRef = ref(db, 'rooms');
                const snapshot = await get(roomsRef);
                let targetRoom = null;
                if (snapshot.exists()) {
                    const rooms = snapshot.val();
                    for (let rId in rooms) {
                        let rData = rooms[rId];
                        let players = rData.players || {};
                        if (Object.keys(players).length < 2 && !rData.gameOver) {
                            targetRoom = rId;
                            break;
                        }
                    }
                }
                if (!targetRoom) {
                    targetRoom = "Room_" + Math.floor(Math.random() * 9000 + 1000);
                    await set(ref(db, `rooms/${targetRoom}`), {
                        board: initialBoard, turn: "white", gameOver: false, message: "រង់ចាំគូប្រកួត...", players: {}
                    });
                }
                await joinRoomProcess(targetRoom);
            } catch (error) { console.error(error); }
        }

        window.createPrivateRoom = async function() {
            isVsAI = false;
            try {
                const targetRoom = "Room_" + Math.floor(Math.random() * 9000 + 1000);
                await set(ref(db, `rooms/${targetRoom}`), {
                    board: initialBoard, turn: "white", gameOver: false, message: "រង់ចាំគូប្រកួត...", players: {}
                });
                await joinRoomProcess(targetRoom);
                alert(`កូដបន្ទប់របស់អ្នក៖ ${targetRoom}`);
            } catch (error) { console.error(error); }
        }

        window.joinPrivateRoom = async function() {
            isVsAI = false;
            const rCode = document.getElementById("roomCodeInput").value.trim();
            if (!rCode) { alert("សូមបញ្ចូលកូដបន្ទប់សិន!"); return; }
            const roomRef = ref(db, `rooms/${rCode}`);
            const snapshot = await get(roomRef);
            if (!snapshot.exists()) { alert("រកមិនឃើញបន្ទប់នេះទេ!"); return; }
            await joinRoomProcess(rCode);
        }

        async function joinRoomProcess(roomId) {
            currentRoomId = roomId;
            const playerRef = ref(db, `rooms/${currentRoomId}/players`);
            const pSnap = await get(playerRef);
            let players = pSnap.exists() ? pSnap.val() : {};

            if (!players.white) { myRole = "white"; players.white = myName; }
            else if (!players.black) { myRole = "black"; players.black = myName; }
            else { myRole = "observer"; }

            await update(ref(db, `rooms/${currentRoomId}`), { players: players });

            if (myRole === 'white') onDisconnect(ref(db, `rooms/${currentRoomId}/players/white`)).remove();
            else if (myRole === 'black') onDisconnect(ref(db, `rooms/${currentRoomId}/players/black`)).remove();

            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = `បន្ទប់៖ ${currentRoomId} (${myRole === 'white' ? 'ស' : 'ខ្មៅ'})`;

            listenToRoom();
            renderBoard();
        }

        function listenToRoom() {
            const roomRef = ref(db, `rooms/${currentRoomId}`);
            onValue(roomRef, async (snapshot) => {
                if (!snapshot.exists()) return;
                const data = snapshot.val();
                if (!data.players || Object.keys(data.players).length === 0) { await remove(roomRef); return; }

                board = data.board;
                turn = data.turn;
                
                if (data.gameOver && !gameOver) {
                    gameOver = true;
                    if (myRole !== "observer") {
                        let didWin = (data.winnerRole === myRole);
                        showGameOverModal(didWin ? "🎉 អ្នកឈ្នះហ្គេមនេះហើយ (+100 កាក់)!" : "😔 អ្នកបានចាញ់ហ្គេមនេះ (-100 កាក់)!", didWin);
                    }
                } else { gameOver = data.gameOver; }
                
                let pCount = data.players ? Object.keys(data.players).length : 0;
                if (pCount < 2) {
                    document.getElementById("status").textContent = `កំពុងរង់ចាំគូប្រកួត...`;
                } else {
                    document.getElementById("status").textContent = data.message || `វេន៖ ${turn === 'white' ? 'ស' : 'ខ្មៅ'}`;
                }
                selectedPiece = null;
                validMoves = [];
                renderBoard();
            });
        }

        window.getValidMoves = function(r, c, cell) {
            return getValidMovesForBoard(r, c, cell, board);
        }

        window.renderBoard = function() {
            const boardEl = document.getElementById("board");
            if (!boardEl) return;
            boardEl.innerHTML = "";
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const sq = document.createElement("div");
                    sq.className = "square " + ((r + c) % 2 === 0 ? "light" : "dark");
                    if (selectedPiece && selectedPiece.r === r && selectedPiece.c === c) sq.classList.add("selected");
                    if (validMoves.some(m => m.r === r && m.c === c)) sq.classList.add("highlight");
                    
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
            
            if (isVsAI) {
                if (turn !== "white") return;
            } else {
                if (turn !== myRole) return;
            }

            let clickedCell = board[r][c];

            if (selectedPiece) {
                if (validMoves.some(m => m.r === r && m.c === c)) {
                    let targetPiece = clickedCell.p;
                    let movingCell = selectedPiece.cell;
                    let isOver = false;
                    let msg = "";
                    let winRole = "";

                    if (targetPiece === "♚") { isOver = true; msg = "🎉 ភាគី ស ឈ្នះ!"; winRole = "white"; }
                    else if (targetPiece === "♔") { isOver = true; msg = "🎉 ភាគី ខ្មៅ ឈ្នះ!"; winRole = "black"; }

                    let isBokedNow = movingCell.b;
                    if (movingCell.p === "♙" && r === 0) isBokedNow = true;
                    if (movingCell.p === "♟" && r === 7) isBokedNow = true;

                    board[r][c] = { p: movingCell.p, b: isBokedNow };
                    board[selectedPiece.r][selectedPiece.c] = { p: "", b: false };

                    let nextTurn = turn === 'white' ? 'black' : 'white';

                    if (isVsAI) {
                        gameOver = isOver;
                        if (gameOver) {
                            showGameOverModal("🎉 អ្នកឈ្នះ AI Bot យ៉ាងអស្ចារ្យ!", true);
                            return;
                        }
                        turn = nextTurn;
                        document.getElementById("status").textContent = `AI កំពុងគិត...`;
                        renderBoard();
                        setTimeout(aiMakeMove, 400);
                    } else {
                        update(ref(db, `rooms/${currentRoomId}`), {
                            board: board, turn: nextTurn, gameOver: isOver, winnerRole: winRole,
                            message: msg || `វេន៖ ${nextTurn === 'white' ? 'ស' : 'ខ្មៅ'}`
                        });
                    }
                }
                selectedPiece = null;
                validMoves = [];
                renderBoard();
            } else if (clickedCell.p !== "") {
                if (isVsAI) {
                    if (isWhitePiece(clickedCell.p)) {
                        selectedPiece = { r, c, cell: clickedCell };
                        validMoves = getValidMoves(r, c, clickedCell);
                        renderBoard();
                    }
                } else {
                    if ((myRole === 'white' && isWhitePiece(clickedCell.p)) || (myRole === 'black' && isBlackPiece(clickedCell.p))) {
                        selectedPiece = { r, c, cell: clickedCell };
                        validMoves = getValidMoves(r, c, clickedCell);
                        renderBoard();
                    }
                }
            }
        }

        window.leaveRoom = async function() {
            if (!isVsAI && currentRoomId) {
                const pRef = ref(db, `rooms/${currentRoomId}/players/${myRole}`);
                await remove(pRef);
                const roomSnap = await get(ref(db, `rooms/${currentRoomId}/players`));
                if (!roomSnap.exists() || Object.keys(roomSnap.val() || {}).length === 0) {
                    await remove(ref(db, `rooms/${currentRoomId}`));
                }
            }
            isVsAI = false;
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

