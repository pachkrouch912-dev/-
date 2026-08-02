from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import random

app = FastAPI()

rooms = {}
# ប្រព័ន្ធគ្រប់គ្រងអ្នកលេង កាក់ និងទួរនេម៉ង់
players_db = {} # {"ឈ្មោះ": {"coins": 100, "ws": websocket}}
tournament = {
    "players": [],
    "rounds": [], # រក្សាទុកវគ្គនីមួយៗនៃការប្រកួត (ចន្លោះពី 4 ទៅ 5 វគ្គ)
    "current_round": 0,
    "status": "waiting"
}

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ហ្គេមអុកខ្មែរអនឡាញ - 8 Ball Pool Style</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            text-align: center;
            margin: 0;
            padding: 20px;
            color: #fff;
        }
        h1 { color: #f1c40f; margin-bottom: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 15px;
            display: inline-block;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            margin-top: 20px;
            max-width: 450px;
            width: 100%;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        input {
            padding: 12px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            margin: 10px 0;
            width: 85%;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            text-align: center;
        }
        button {
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            background-color: #e67e22;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin: 8px;
            transition: 0.2s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            width: 90%;
        }
        button:hover { background-color: #d35400; transform: translateY(-2px); }
        .btn-green { background-color: #27ae60; }
        .btn-green:hover { background-color: #219653; }
        .btn-blue { background-color: #2980b9; }
        .btn-blue:hover { background-color: #1f618d; }
        
        #wallet {
            font-size: 20px;
            font-weight: bold;
            color: #f1c40f;
            background: rgba(0, 0, 0, 0.3);
            padding: 10px 20px;
            border-radius: 30px;
            display: inline-block;
            margin-bottom: 15px;
            border: 1px solid #f1c40f;
        }
        .match-card {
            background: rgba(0, 0, 0, 0.2);
            padding: 10px;
            margin: 8px 0;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
        }
        #board {
            display: grid;
            grid-template-columns: repeat(8, 48px);
            grid-template-rows: repeat(8, 48px);
            gap: 2px;
            justify-content: center;
            margin: 10px auto;
            border: 4px solid #5c3a21;
            background-color: #5c3a21;
            border-radius: 6px;
            width: max-content;
        }
        .square {
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
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

    <h1>♟️ អុកខ្មែរអនឡាញ (Ok Chaktrong) ♟️</h1>

    <!-- វគ្គចូលឈ្មោះ និងបង្ហាញកាក់ -->
    <div id="login-box" class="card">
        <h3>ចូលរួមលេងហ្គេម</h3>
        <input type="text" id="playerName" placeholder="បញ្ចូលឈ្មោះរបស់អ្នក"><br>
        <button class="btn-green" onclick="loginUser()">ចូលគណនី</button>
    </div>

    <!-- ម៉ឺនុយដើររចនាបថ 8 Ball Pool -->
    <div id="main-menu" class="card hidden">
        <div id="wallet">💰 កាក់របស់អ្នក៖ <span id="coinBalance">100</span> 🪙</div><br>
        <button class="btn-blue" onclick="showDirectPlay()">🎮 លេង ១ទល់១ (1v1 Room)</button>
        <button onclick="showTournament()">🏆 ប្រកួតជម្រុះ (4-5 Rounds)</button>
    </div>

    <!-- ប្រអប់លេង ១ទល់១ (1v1 Direct Play) -->
    <div id="direct-play-box" class="card hidden">
        <h3>លេង ១ទល់១ ជាមួយមិត្តភក្តិ</h3>
        <input type="text" id="roomInput" placeholder="បញ្ចូលលេខបន្ទប់ (ឧ. 101)"><br>
        <button class="btn-green" onclick="joinRoom('1v1')">ចូលបន្ទប់លេង</button>
        <button onclick="backToMenu()">ថយក្រោយ</button>
    </div>

    <!-- ប្រអប់តារាងប្រកួតជម្រុះ (Tournament Lobby) -->
    <div id="tournament-lobby" class="card hidden">
        <h3>🏆 វគ្គប្រកួតជម្រុះ (Tournament)</h3>
        <p id="tour-status">ស្វែងរកអ្នកលេងគ្រប់គ្រាន់ដើម្បីចាប់ផ្តើម...</p>
        <div id="match-list"></div>
        <button id="start-tour-btn" class="hidden btn-green" onclick="startTournament()">ចាប់ផ្តើមប្រកួតជម្រុះ</button>
        <button onclick="backToMenu()">ថយក្រោយ</button>
    </div>

    <!-- កន្លែងលេងហ្គេមអុក -->
    <div id="game-container" class="hidden">
        <h3 id="room-title">បន្ទប់ប្រកួត</h3>
        <div id="status" style="background: rgba(0,0,0,0.4); padding: 5px 15px; border-radius: 15px; display:inline-block; font-weight:bold;">រង់ចាំគូប្រកួត...</div>
        <div id="board"></div>
        <button class="btn-green" onclick="leaveRoom()">ចាកចេញពីបន្ទប់</button>
    </div>

    <script>
        let ws = null;
        let myName = null;
        let myRole = null;
        let currentRoom = null;

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
        let board = JSON.parse(JSON.stringify(initialBoard));
        let selectedPiece = null;
        let turn = 'white';
        let validMoves = [];
        let gameOver = false;

        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        let globalWs = null;

        function loginUser() {
            myName = document.getElementById("playerName").value.trim();
            if (!myName) {
                alert("សូមបញ្ចូលឈ្មោះរបស់អ្នក!");
                return;
            }
            document.getElementById("login-box").classList.add("hidden");
            document.getElementById("main-menu").classList.remove("hidden");

            globalWs = new WebSocket(`${protocol}//${window.location.host}/ws/global?name=${encodeURIComponent(myName)}`);
            globalWs.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.type === "wallet_update") {
                    document.getElementById("coinBalance").textContent = data.coins;
                } else if (data.type === "tour_update") {
                    updateTournamentUI(data);
                }
            };
        }

        function showDirectPlay() {
            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("direct-play-box").classList.remove("hidden");
        }

        function showTournament() {
            document.getElementById("main-menu").classList.add("hidden");
            document.getElementById("tournament-lobby").classList.remove("hidden");
            globalWs.send(JSON.stringify({ type: "join_tournament" }));
        }

        function backToMenu() {
            document.getElementById("direct-play-box").classList.add("hidden");
            document.getElementById("tournament-lobby").classList.add("hidden");
            document.getElementById("main-menu").classList.remove("hidden");
        }

        function joinRoom(mode) {
            let roomCode = mode === '1v1' ? document.getElementById("roomInput").value.trim() : currentRoom;
            if (!roomCode) {
                alert("សូមបញ្ចូលលេខបន្ទប់!");
                return;
            }
            currentRoom = roomCode;
            document.getElementById("direct-play-box").classList.add("hidden");
            document.getElementById("tournament-lobby").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = `បន្ទប់៖ ${roomCode}`;

            ws = new WebSocket(`${protocol}//${window.location.host}/ws/room/${roomCode}?name=${encodeURIComponent(myName)}`);

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.type === "init") {
                    myRole = data.role;
                    document.getElementById("status").textContent = `ភាគី៖ ${myRole === 'white' ? 'ស (ខាងក្រោម)' : 'ខ្មៅ (ខាងលើ)'}`;
                } else if (data.type === "update") {
                    board = data.board;
                    turn = data.turn;
                    gameOver = data.gameOver;
                    document.getElementById("status").textContent = data.message;
                    selectedPiece = null;
                    validMoves = [];
                    renderBoard();
                }
            };
        }

        function leaveRoom() {
            if (ws) ws.close();
            document.getElementById("game-container").classList.add("hidden");
            document.getElementById("main-menu").classList.remove("hidden");
        }

        function updateTournamentUI(data) {
            const listDiv = document.getElementById("match-list");
            listDiv.innerHTML = `<h4>ចំនួនអ្នកចូលរួម៖ ${data.players.length} នាក់ (វគ្គទី ${data.current_round} / 5)</h4>`;
            
            if (data.matches.length > 0) {
                data.matches.forEach((m, idx) => {
                    listDiv.innerHTML += `
                        <div class="match-card">
                            <span>គូទី ${idx+1}: ${m.white} vs ${m.black}</span>
                            ${(myName === m.white || myName === m.black) && m.status === 'ongoing' ? `<button onclick="currentRoom='${m.room}'; joinRoom('tour')">ចូលលេង</button>` : `<span>${m.status}</span>`}
                        </div>
                    `;
                });
            }
            if (data.players.length >= 2 && data.status === "waiting") {
                document.getElementById("start-tour-btn").classList.remove("hidden");
            }
        }

        function startTournament() {
            globalWs.send(JSON.stringify({ type: "start_tournament" }));
        }

        //  logic ដើរគ្រាប់អុក
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

        function renderBoard() {
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

                    if (target === "♚") { isOver = true; msg = "🎉 ស ឈ្នះការប្រកួត (+50 កាក់)!"; }
                    else if (target === "♔") { isOver = true; msg = "🎉 ខ្មៅ ឈ្នះការប្រកួត (+50 កាក់)!"; }

                    board[r][c] = moving;
                    board[selectedPiece.r][selectedPiece.c] = "";
                    let nextTurn = turn === 'white' ? 'black' : 'white';

                    ws.send(JSON.stringify({ type: "move", board, turn: nextTurn, gameOver: isOver, message: msg }));
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
    </script>
</body>
</html>
"""

global_connections = []

async def broadcast_global():
    for name, data in players_db.items():
        try:
            await data["ws"].send_text(json.dumps({"type": "wallet_update", "coins": data["coins"]}))
        except:
            pass

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_CONTENT

@app.websocket("/ws/global")
async def global_ws(websocket: WebSocket, name: str):
    await websocket.accept()
    if name not in players_db:
        players_db[name] = {"coins": 100, "ws": websocket} # 🎁 ផ្ដល់ជូនកាក់ស្វាគមន៍ ១០០ ពេលចូលដំបូង
    else:
        players_db[name]["ws"] = websocket

    global_connections.append(websocket)
    await websocket.send_text(json.dumps({"type": "wallet_update", "coins": players_db[name]["coins"]}))
    
    try:
        while True:
            data = await websocket.receive_text()
            packet = json.loads(data)
            if packet["type"] == "join_tournament":
                if name not in tournament["players"]:
                    tournament["players"].append(name)
                # ส่งข้อมูลทัวร์นาเมนต์ให้ทุกคนเห็น
                tour_payload = json.dumps({"type": "tour_update", **tournament})
                for conn in global_connections:
                    await conn.send_text(tour_payload)
            elif packet["type"] == "start_tournament":
                player_list = tournament["players"]
                random.shuffle(player_list)
                tournament["matches"] = []
                tournament["current_round"] += 1
                for i in range(0, len(player_list) - 1, 2):
                    room_id = f"tour_r{tournament['current_round']}_m{i//2 + 1}"
                    tournament["matches"].append({
                        "room": room_id,
                        "white": player_list[i],
                        "black": player_list[i+1],
                        "status": "ongoing"
                    })
                    rooms[room_id] = {
                        "board": json.loads(json.dumps(initial_board)),
                        "turn": "white",
                        "gameOver": False,
                        "message": "វេនអ្នកលេង៖ ស",
                        "players": {}
                    }
                tournament["status"] = "ongoing"
                tour_payload = json.dumps({"type": "tour_update", **tournament})
                for conn in global_connections:
                    await conn.send_text(tour_payload)
    except WebSocketDisconnect:
        global_connections.remove(websocket)

@app.websocket("/ws/room/{room_id}")
async def room_ws(websocket: WebSocket, room_id: str, name: str):
    await websocket.accept()
    if room_id not in rooms:
        rooms[room_id] = {
            "board": json.loads(json.dumps(initial_board)),
            "turn": "white",
            "gameOver": False,
            "message": "វេនអ្នកលេង៖ ស",
            "players": {}
        }
    
    room = rooms[room_id]
    role = "white" if len(room["players"]) == 0 else "black"
    room["players"][role] = {"ws": websocket, "name": name}

    await websocket.send_text(json.dumps({"type": "init", "role": role}))
    
    try:
        while True:
            data = await websocket.receive_text()
            packet = json.loads(data)
            if packet["type"] == "move":
                room["board"] = packet["board"]
                room["turn"] = packet["turn"]
                room["gameOver"] = packet["gameOver"]
                room["message"] = packet["message"]

                if packet["gameOver"]:
                    winner_role = "white" if "ស" in packet["message"] else "black"
                    winner_name = room["players"].get(winner_role, {}).get("name")
                    if winner_name and winner_name in players_db:
                        players_db[winner_name]["coins"] += 50 # 💰 ឈ្នះបាន 50 កាក់បន្ថែម
                        await broadcast_global()

                for p in room["players"].values():
                    await p["ws"].send_text(json.dumps({
                        "type": "update",
                        "board": room["board"],
                        "turn": room["turn"],
                        "gameOver": room["gameOver"],
                        "message": room["message"]
                    }))
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

