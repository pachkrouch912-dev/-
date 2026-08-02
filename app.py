from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>អុកខ្មែរអនឡាញ - 8-Ball Pool Style</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: radial-gradient(circle at center, #1b2838, #0a0f18);
            text-align: center; margin: 0; padding: 20px; color: #fff; min-height: 100vh;
            overflow-x: hidden; position: relative;
        }

        .bg-chess {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            overflow: hidden; z-index: 0; pointer-events: none; opacity: 0.15;
        }
        .floating-piece {
            position: absolute; font-size: 40px; animation: floatUp 8s infinite linear;
        }
        @keyframes floatUp {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            50% { opacity: 1; }
            100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
        }

        .container { position: relative; z-index: 1; max-width: 480px; margin: 0 auto; }
        
        h1 { 
            color: #f1c40f; text-shadow: 0 0 15px rgba(241, 196, 15, 0.7);
            font-size: 24px; margin-bottom: 10px; letter-spacing: 1px;
        }

        .card {
            background: rgba(15, 25, 35, 0.85); backdrop-filter: blur(15px);
            padding: 20px; border-radius: 20px; display: inline-block;
            box-shadow: 0 15px 35px rgba(0,0,0,0.7), inset 0 0 15px rgba(255,255,255,0.05);
            margin-top: 15px; width: 100%; box-sizing: border-box;
            border: 2px solid rgba(241, 196, 15, 0.3);
            animation: fadeIn 0.5s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .user-profile {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(0,0,0,0.5); padding: 10px 20px; border-radius: 12px;
            margin-bottom: 15px; border: 1px solid rgba(241, 196, 15, 0.2);
            font-size: 15px; font-weight: bold;
        }
        .coin-badge { color: #f1c40f; display: flex; align-items: center; gap: 5px; }

        input {
            padding: 14px; font-size: 16px; border: 2px solid #34495e; border-radius: 12px;
            margin: 10px 0; width: 85%; background: rgba(0, 0, 0, 0.5);
            color: #fff; text-align: center; outline: none; transition: 0.3s;
        }
        input:focus { border-color: #f1c40f; box-shadow: 0 0 10px rgba(241,196,15,0.4); }

        button {
            padding: 14px 24px; font-size: 16px; font-weight: bold;
            color: white; border: none; border-radius: 12px; cursor: pointer; 
            margin: 10px auto; width: 92%; display: block;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3); transition: 0.2s;
        }
        button:hover { transform: translateY(-3px); filter: brightness(1.1); }
        button:active { transform: translateY(1px); }

        .btn-green { background: linear-gradient(135deg, #2ecc71, #27ae60); box-shadow: 0 4px 15px rgba(46,204,113,0.4); }
        .btn-blue { background: linear-gradient(135deg, #3498db, #2980b9); box-shadow: 0 4px 15px rgba(52,152,219,0.4); }
        .btn-red { background: linear-gradient(135deg, #e74c3c, #c0392b); box-shadow: 0 4px 15px rgba(231,76,60,0.4); }

        /* តារាងជើងខ្លាំង (Leaderboard) */
        .leaderboard-box {
            margin-top: 15px; background: rgba(0, 0, 0, 0.4);
            border-radius: 12px; padding: 12px; border: 1px solid rgba(241, 196, 15, 0.2);
            text-align: left; max-height: 160px; overflow-y: auto;
        }
        .leaderboard-title { color: #f1c40f; font-size: 14px; font-weight: bold; text-align: center; margin-bottom: 8px; }
        .lb-item { display: flex; justify-content: space-between; font-size: 13px; padding: 4px 8px; border-bottom: 1px solid rgba(255,255,255,0.05); }

        .deco-board-container {
            margin-top: 15px; display: flex; flex-direction: column; align-items: center;
        }
        .deco-board {
            display: grid; grid-template-columns: repeat(8, 22px);
            grid-template-rows: repeat(8, 22px); gap: 1px;
            border: 2px solid #8e44ad; background-color: #8e44ad;
            border-radius: 6px; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        }
        .deco-square {
            width: 22px; height: 22px; display: flex;
            align-items: center; justify-content: center;
            font-size: 14px; user-select: none;
        }
        .deco-light { background-color: #f5cba7; color: #000; }
        .deco-dark { background-color: #d35400; color: #fff; }

        #board {
            display: grid; grid-template-columns: repeat(8, 42px);
            grid-template-rows: repeat(8, 42px); gap: 2px;
            justify-content: center; margin: 15px auto;
            border: 5px solid #8e44ad; background-color: #8e44ad;
            border-radius: 10px; width: max-content;
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        }
        .square {
            width: 42px; height: 42px; display: flex;
            align-items: center; justify-content: center;
            font-size: 26px; font-weight: bold; cursor: pointer; user-select: none;
            transition: background 0.2s;
        }
        .light { background-color: #f5cba7; color: #000; }
        .dark { background-color: #d35400; color: #fff; }
        .selected { background-color: #9b59b6 !important; box-shadow: inset 0 0 10px #fff; }
        .highlight { background-color: #2ecc71 !important; }
        .white-piece { color: #fff; text-shadow: 0 2px 4px #000; }
        .black-piece { color: #111; text-shadow: 0 2px 4px #fff; }
        .hidden { display: none; }
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
        <h1>♟️ អុកខ្មែរអនឡាញ (8-Ball Pool Style) ♟️</h1>

        <!-- ផ្នែកចូលឈ្មោះ (ទំព័រទី១) -->
        <div id="login-box" class="card">
            <h3 style="color: #f1c40f; margin-top: 0;">ចូលរួមលេងហ្គេម</h3>
            <input type="text" id="playerName" placeholder="បញ្ចូលឈ្មោះរបស់អ្នក"><br>
            <button class="btn-green" onclick="loginUser()">ចូលគណនី</button>
        </div>

        <!-- ម៉ឺនុយដើម (ទំព័រទី២) -->
        <div id="main-menu" class="card hidden">
            <div class="user-profile">
                <span id="welcome-msg" style="color: #f1c40f;"></span>
                <span class="coin-badge">🪙 <span id="userCoins">0</span> កាក់</span>
            </div>
            <button class="btn-green" onclick="quickJoinRoom()">⚡ ចូលលេងរហ័ស (Quick Match)</button>
            <button class="btn-blue" onclick="createPrivateRoom()">🏠 បង្កើតបន្ទប់ផ្ទាល់ខ្លួន</button>
            <input type="text" id="roomCodeInput" placeholder="បញ្ចូលកូដបន្ទប់ (ឧ. Room_1234)"><br>
            <button class="btn-green" onclick="joinPrivateRoom()">🔗 ចូលតាមកូដបន្ទប់</button>

            <!-- តារាងបង្ហាញជើងខ្លាំង -->
            <div class="leaderboard-box">
                <div class="leaderboard-title">🏆 តារាងជើងខ្លាំងប្រចាំសង្វៀន 🏆</div>
                <div id="leaderboardList">កំពុងទាញយក...</div>
            </div>

            <!-- ក្ដារអុកលំអរនៅលើម៉ឺនុយដើម -->
            <div class="deco-board-container">
                <div class="deco-board" id="decoBoard"></div>
            </div>
        </div>

        <!-- កន្លែងលេងអុក -->
        <div id="game-container" class="hidden">
            <h3 id="room-title" style="color: #f1c40f; margin: 5px 0;">បន្ទប់ប្រកួត</h3>
            <div id="status" style="background: rgba(0,0,0,0.6); padding: 8px 18px; border-radius: 20px; display:inline-block; font-weight:bold; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.2);">រង់ចាំគូប្រកួត...</div>
            <div id="board"></div>
            <button class="btn-red" style="width: 220px; margin-top: 15px;" onclick="leaveRoom()">ចាកចេញពីបន្ទប់</button>
        </div>
    </div>

    <!-- Firebase SDKs -->
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
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
            ["", "", "", "", "", "", "", ""],
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
            ["", "", "", "", "", "", "", ""],
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
        ];

        let myName = "";
        let rawDisplayName = "";
        let myCoins = 0;
        let currentRoomId = "";
        let myRole = ""; 
        let board = JSON.parse(JSON.stringify(initialBoard));
        let turn = "white";
        let gameOver = false;
        let selectedPiece = null;
        let validMoves = [];

        function renderDecoBoard() {
            const decoEl = document.getElementById("decoBoard");
            decoEl.innerHTML = "";
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const sq = document.createElement("div");
                    sq.className = "deco-square " + ((r + c) % 2 === 0 ? "deco-light" : "deco-dark");
                    let p = initialBoard[r][c];
                    if (p !== "") {
                        sq.textContent = p;
                        sq.style.color = ["♖", "♘", "♗", "♕", "♔", "♙"].includes(p) ? "#fff" : "#111";
                    }
                    decoEl.appendChild(sq);
                }
            }
        }
        renderDecoBoard();

        // មុខងារទាញយកតារាងជើងខ្លាំង (Leaderboard)
        function loadLeaderboard() {
            const usersRef = ref(db, 'users');
            onValue(usersRef, (snapshot) => {
                const lbEl = document.getElementById("leaderboardList");
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
                // រៀបលំដាប់ពីអ្នកមានកាក់ច្រើនជាងគេទៅតិច
                usersArray.sort((a, b) => b.coins - a.coins);

                lbEl.innerHTML = "";
                usersArray.slice(0, 5).forEach((user, index) => {
                    let rankIcon = index === 0 ? "🥇" : (index === 1 ? "🥈" : (index === 2 ? "🥉" : `${index + 1}.`));
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
            } else {
                myCoins = 1000; 
                await set(userRef, { name: rawDisplayName, coins: myCoins });
            }

            document.getElementById("login-box").classList.add("hidden");
            document.getElementById("main-menu").classList.remove("hidden");
            document.getElementById("welcome-msg").textContent = `${rawDisplayName}`;
            document.getElementById("userCoins").textContent = myCoins;

            loadLeaderboard();
        }

        window.quickJoinRoom = async function() {
            const roomsRef = ref(db, 'rooms');
            const snapshot = await get(roomsRef);
            let targetRoom = null;

            if (snapshot.exists()) {
                const rooms = snapshot.val();
                for (let rId in rooms) {
                    let rData = rooms[rId];
                    let players = rData.players || {};
                    let playerCount = Object.keys(players).length;
                    if (playerCount < 2 && !rData.gameOver) {
                        targetRoom = rId;
                        break;
                    }
                }
            }

            if (!targetRoom) {
                targetRoom = "Room_" + Math.floor(Math.random() * 9000 + 1000);
                await set(ref(db, `rooms/${targetRoom}`), {
                    board: initialBoard,
                    turn: "white",
                    gameOver: false,
                    message: "រង់ចាំគូប្រកួត...",
                    players: {}
                });
            }

            await joinRoomProcess(targetRoom);
        }

        window.createPrivateRoom = async function() {
            const targetRoom = "Room_" + Math.floor(Math.random() * 9000 + 1000);
            await set(ref(db, `rooms/${targetRoom}`), {
                board: initialBoard,
                turn: "white",
                gameOver: false,
                message: "រង់ចាំគូប្រកួត...",
                players: {}
            });
            await joinRoomProcess(targetRoom);
            alert(`បានបង្កើតបន្ទប់ដោយជោគជ័យ!\nកូដបន្ទប់របស់អ្នកគឺ៖ ${targetRoom}\nសូមផ្ញើកូដនេះទៅកាន់មិត្តភក្តិរបស់អ្នកដើម្បីចូលលេង។`);
        }

        window.joinPrivateRoom = async function() {
            const rCode = document.getElementById("roomCodeInput").value.trim();
            if (!rCode) { alert("សូមបញ្ចូលកូដបន្ទប់សិន!"); return; }
            
            const roomRef = ref(db, `rooms/${rCode}`);
            const snapshot = await get(roomRef);
            if (!snapshot.exists()) {
                alert("រកមិនឃើញបន្ទប់នេះទេ!");
                return;
            }
            await joinRoomProcess(rCode);
        }

        async function joinRoomProcess(roomId) {
            currentRoomId = roomId;
            const playerRef = ref(db, `rooms/${currentRoomId}/players`);
            const pSnap = await get(playerRef);
            let players = pSnap.exists() ? pSnap.val() : {};

            if (!players.white) {
                myRole = "white";
                players.white = myName;
            } else if (!players.black) {
                myRole = "black";
                players.black = myName;
            } else {
                myRole = "observer";
            }

            await update(ref(db, `rooms/${currentRoomId}`), { players: players });

            if (myRole === 'white') {
                onDisconnect(ref(db, `rooms/${currentRoomId}/players/white`)).remove();
            } else if (myRole === 'black') {
                onDisconnect(ref(db, `rooms/${currentRoomId}/players/black`)).remove();
            }

            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = `បន្ទប់៖ ${currentRoomId} (${myRole === 'white' ? 'ស' : (myRole === 'black' ? 'ខ្មៅ' : 'អ្នកទស្សនា')})`;

            listenToRoom();
            renderBoard();
        }

        function listenToRoom() {
            const roomRef = ref(db, `rooms/${currentRoomId}`);
            onValue(roomRef, async (snapshot) => {
                if (!snapshot.exists()) return;
                const data = snapshot.val();
                
                if (!data.players || Object.keys(data.players).length === 0) {
                    await remove(roomRef);
                    return;
                }

                board = data.board;
                turn = data.turn;
                
                if (data.gameOver && !gameOver) {
                    gameOver = true;
                    if (myRole !== "observer") {
                        if (data.winnerRole === myRole) {
                            myCoins += 100; // ឈ្នះបាន +100 កាក់
                            alert("🎉 សូមអបអរសាទរ! អ្នកឈ្នះការប្រកួត (+100 កាក់)!");
                        } else {
                            myCoins = Math.max(0, myCoins - 100); // ចាញ់កាត់ -100 កាក់
                            alert("😔 អ្នកបានចាញ់ការប្រកួត (-100 កាក់)!");
                        }
                        await update(ref(db, `users/${myName}`), { coins: myCoins });
                        document.getElementById("userCoins").textContent = myCoins;
                    }
                } else {
                    gameOver = data.gameOver;
                }
                
                let pCount = data.players ? Object.keys(data.players).length : 0;
                if (pCount < 2) {
                    document.getElementById("status").textContent = `បន្ទប់៖ ${currentRoomId} - កំពុងរង់ចាំគូប្រកួត...`;
                } else {
                    document.getElementById("status").textContent = data.message || `វេនអ្នកលេង៖ ${turn === 'white' ? 'ស' : 'ខ្មៅ'}`;
                }
                selectedPiece = null;
                validMoves = [];
                renderBoard();
            });
        }

        function isWhitePiece(p) { return ["♖", "♘", "♗", "♕", "♔", "♙"].includes(p); }
        function isBlackPiece(p) { return ["♜", "♞", "♝", "♛", "♚", "♟"].includes(p); }

        function getValidMoves(r, c, piece) {
            let moves = [];
            let isWhite = isWhitePiece(piece);
            let directions = [[-1,0], [1,0], [0,-1], [0,1], [-1,-1], [-1,1], [1,-1], [1,1]];
            for (let d of directions) {
                let nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                    let target = board[nr][nc];
                    if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) {
                        moves.push({r: nr, c: nc});
                    }
                }
            }
            return moves;
        }

        window.renderBoard = function() {
            const boardEl = document.getElementById("board");
            boardEl.innerHTML = "";
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const sq = document.createElement("div");
                    sq.className = "square " + ((r + c) % 2 === 0 ? "light" : "dark");
                    if (selectedPiece && selectedPiece.r === r && selectedPiece.c === c) sq.classList.add("selected");
                    if (validMoves.some(m => m.r === r && m.c === c)) sq.classList.add("highlight");
                    
                    let p = board[r][c];
                    if (p !== "") {
                        let span = document.createElement("span");
                        span.textContent = p;
                        span.className = isWhitePiece(p) ? "white-piece" : "black-piece";
                        sq.appendChild(span);
                    }
                    sq.onclick = () => handleSquareClick(r, c);
                    boardEl.appendChild(sq);
                }
            }
        }

        function handleSquareClick(r, c) {
            if (gameOver || turn !== myRole) return;
            let clicked = board[r][c];
            if (selectedPiece) {
                if (validMoves.some(m => m.r === r && m.c === c)) {
                    let target = board[r][c];
                    let moving = selectedPiece.piece;
                    let isOver = false;
                    let msg = "";
                    let winRole = "";

                    if (target === "♚") { 
                        isOver = true; 
                        msg = "🎉 ភាគី ស ឈ្នះការប្រកួត!"; 
                        winRole = "white";
                    } else if (target === "♔") { 
                        isOver = true; 
                        msg = "🎉 ភាគី ខ្មៅ ឈ្នះការប្រកួត!"; 
                        winRole = "black";
                    }

                    board[r][c] = moving;
                    board[selectedPiece.r][selectedPiece.c] = "";
                    let nextTurn = turn === 'white' ? 'black' : 'white';

                    update(ref(db, `rooms/${currentRoomId}`), {
                        board: board,
                        turn: nextTurn,
                        gameOver: isOver,
                        winnerRole: winRole,
                        message: msg || `វេនអ្នកលេង៖ ${nextTurn === 'white' ? 'ស' : 'ខ្មៅ'}`
                    });
                }
                selectedPiece = null;
                validMoves = [];
                renderBoard();
            } else if (clicked !== "") {
                if ((myRole === 'white' && isWhitePiece(clicked)) || (myRole === 'black' && isBlackPiece(clicked))) {
                    selectedPiece = { r, c, piece: clicked };
                    validMoves = getValidMoves(r, c, clicked);
                    renderBoard();
                }
            }
        }

        window.leaveRoom = async function() {
            if (currentRoomId) {
                const pRef = ref(db, `rooms/${currentRoomId}/players/${myRole}`);
                await remove(pRef);
                
                const roomSnap = await get(ref(db, `rooms/${currentRoomId}/players`));
                if (!roomSnap.exists() || Object.keys(roomSnap.val() || {}).length === 0) {
                    await remove(ref(db, `rooms/${currentRoomId}`));
                }
            }
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

