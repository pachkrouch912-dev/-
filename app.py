from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>អុកខ្មែរអនឡាញ - Firebase Realtime</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            text-align: center; margin: 0; padding: 20px; color: #fff; min-height: 100vh;
        }
        h1 { color: #f1c40f; text-shadow: 0 0 10px rgba(241, 196, 15, 0.5); }
        .card {
            background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(12px);
            padding: 25px; border-radius: 16px; display: inline-block;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-top: 15px;
            max-width: 480px; width: 100%; border: 1px solid rgba(255, 255, 255, 0.15);
        }
        input {
            padding: 12px; font-size: 16px; border: none; border-radius: 8px;
            margin: 10px 0; width: 85%; background: rgba(255, 255, 255, 0.9);
            color: #333; text-align: center; outline: none;
        }
        button {
            padding: 12px 24px; font-size: 16px; font-weight: bold;
            background-color: #e67e22; color: white; border: none;
            border-radius: 8px; cursor: pointer; margin: 8px; width: 90%;
            box-shadow: 0 4px 15px rgba(230, 126, 34, 0.4);
        }
        button:hover { background-color: #d35400; transform: translateY(-2px); }
        .btn-green { background-color: #27ae60; }
        
        #board {
            display: grid; grid-template-columns: repeat(8, 40px);
            grid-template-rows: repeat(8, 40px); gap: 2px;
            justify-content: center; margin: 15px auto;
            border: 4px solid #5c3a21; background-color: #5c3a21;
            border-radius: 6px; width: max-content;
        }
        .square {
            width: 40px; height: 40px; display: flex;
            align-items: center; justify-content: center;
            font-size: 24px; font-weight: bold; cursor: pointer; user-select: none;
        }
        .light { background-color: #f0d9b5; color: #000; }
        .dark { background-color: #b58863; color: #000; }
        .selected { background-color: #7b61ff !important; }
        .highlight { background-color: #85c1e9 !important; }
        .white-piece { color: #fff; text-shadow: 1px 1px 2px #000; }
        .black-piece { color: #111; text-shadow: 1px 1px 2px #fff; }
        .hidden { display: none; }
    </style>
</head>
<body>

    <h1>♟️ អុកខ្មែរអនឡាញ (Firebase Realtime) ♟️</h1>

    <!-- ផ្នែកចូលឈ្មោះ -->
    <div id="login-box" class="card">
        <h3>ចូលរួមលេងហ្គេម</h3>
        <input type="text" id="playerName" placeholder="បញ្ចូលឈ្មោះរបស់អ្នក"><br>
        <button class="btn-green" onclick="loginUser()">ចូលគណនី</button>
    </div>

    <!-- ម៉ឺនុយដើម -->
    <div id="main-menu" class="card hidden">
        <h3 id="welcome-msg"></h3>
        <button class="btn-green" onclick="quickJoinRoom()">⚡ ចូលលេងរហ័ស (Quick Match)</button>
    </div>

    <!-- កន្លែងលេងអុក -->
    <div id="game-container" class="hidden">
        <h3 id="room-title">បន្ទប់ប្រកួត</h3>
        <div id="status" style="background: rgba(0,0,0,0.4); padding: 5px 15px; border-radius: 15px; display:inline-block; font-weight:bold; margin-bottom: 10px;">រង់ចាំគូប្រកួត...</div>
        <div id="board"></div>
        <button class="btn-green" style="width: 200px; margin-top: 15px;" onclick="leaveRoom()">ចាកចេញពីបន្ទប់</button>
    </div>

    <!-- Firebase SDKs -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getDatabase, ref, set, get, update, onValue } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";

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
        let currentRoomId = "";
        let myRole = ""; 
        let board = JSON.parse(JSON.stringify(initialBoard));
        let turn = "white";
        let gameOver = false;
        let selectedPiece = null;
        let validMoves = [];
        let roomListener = null;

        window.loginUser = function() {
            myName = document.getElementById("playerName").value.trim();
            if (!myName) { alert("សូមបញ្ចូលឈ្មោះរបស់អ្នក!"); return; }
            document.getElementById("login-box").classList.add("hidden");
            document.getElementById("main-menu").classList.remove("hidden");
            document.getElementById("welcome-msg").textContent = `សួស្តី, ${myName}`;
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

            currentRoomId = targetRoom;
            
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

            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = `បន្ទប់៖ ${currentRoomId} (${myRole === 'white' ? 'ស' : 'ខ្មៅ'})`;

            listenToRoom();
            renderBoard();
        }

        function listenToRoom() {
            const roomRef = ref(db, `rooms/${currentRoomId}`);
            roomListener = onValue(roomRef, (snapshot) => {
                if (!snapshot.exists()) return;
                const data = snapshot.val();
                board = data.board;
                turn = data.turn;
                gameOver = data.gameOver;
                
                let pCount = data.players ? Object.keys(data.players).length : 0;
                if (pCount < 2) {
                    document.getElementById("status").textContent = "កំពុងរង់ចាំគូប្រកួតចូលលេង...";
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

                    if (target === "♚") { isOver = true; msg = "🎉 ភាគី ស ឈ្នះការប្រកួត!"; }
                    else if (target === "♔") { isOver = true; msg = "🎉 ភាគី ខ្មៅ ឈ្នះការប្រកួត!"; }

                    board[r][c] = moving;
                    board[selectedPiece.r][selectedPiece.c] = "";
                    let nextTurn = turn === 'white' ? 'black' : 'white';

                    update(ref(db, `rooms/${currentRoomId}`), {
                        board: board,
                        turn: nextTurn,
                        gameOver: isOver,
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

        window.leaveRoom = function() {
            document.getElementById("game-container").classList.add("hidden");
            document.getElementById("main-menu").classList.remove("hidden");
            location.reload();
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

