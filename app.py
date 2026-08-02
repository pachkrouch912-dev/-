from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import random

app = FastAPI()

rooms = {}
# បន្ថែមទិន្នន័យសម្រាប់គ្រប់គ្រងកាក់របស់អ្នកលេង និងបញ្ជីឈ្មោះ
tournament = {
    "players": {}, # រក្សាទុក ឈ្មោះ: ចំនួនកាក់ (ឧ. {" Dara": 100 })
    "matches": [],
    "status": "waiting"
}

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ប្រព័ន្ធប្រកួតអុកខ្មែរ + កាក់ផ្ទាល់ខ្លួន</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            text-align: center;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        h1 { color: #8B0000; margin-bottom: 5px; }
        .box {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            margin-top: 20px;
            max-width: 500px;
            width: 100%;
        }
        input {
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin: 5px;
            width: 80%;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #8B0000;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover { background-color: #a80000; }
        .match-card {
            background: #eef2f7;
            padding: 10px;
            margin: 8px 0;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        #wallet {
            font-size: 18px;
            font-weight: bold;
            color: #d4af37;
            background: #fff;
            padding: 8px 20px;
            border-radius: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            display: inline-block;
            margin-bottom: 15px;
        }
        #game-container, #tournament-lobby { margin-top: 20px; }
        #board {
            display: grid;
            grid-template-columns: repeat(8, 50px);
            grid-template-rows: repeat(8, 50px);
            gap: 2px;
            justify-content: center;
            margin: 10px auto;
            border: 4px solid #5c3a21;
            background-color: #5c3a21;
            border-radius: 6px;
            width: max-content;
        }
        .square {
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
        }
        .light { background-color: #f0d9b5; }
        .dark { background-color: #b58863; }
        .selected { background-color: #7b61ff !important; }
        .highlight { background-color: #85c1e9 !important; }
        .white-piece { color: #fff; text-shadow: 1px 1px 2px #000; }
        .black-piece { color: #111; text-shadow: 1px 1px 2px #fff; }
        .hidden { display: none; }
    </style>
</head>
<body>

    <h1>♟️ ប្រកួតអុកខ្មែរ និងប្រព័ន្ធកាក់ ♟️</h1>

    <div id="register-box" class="box">
        <h3>ចុះឈ្មោះចូលរួមប្រកួត</h3>
        <input type="text" id="playerName" placeholder="បញ្ចូលឈ្មោះរបស់អ្នក"><br>
        <button onclick="registerPlayer()">ចូលលេង</button>
    </div>

    <div id="tournament-lobby" class="box hidden">
        <div id="wallet">💰 កាក់របស់អ្នក៖ <span id="coinBalance">0</span> 🪙</div>
        <h3>តារាងការប្រកួត (Tournament Lobby)</h3>
        <p id="lobby-status">កំពុងរង់ចាំអ្នកលេងផ្សេងទៀត...</p>
        <div id="match-list"></div>
        <button id="start-tour-btn" class="hidden" onclick="startTournament()">ចាប់ផ្ដើមការប្រកួត</button>
    </div>

    <div id="game-container" class="hidden">
        <h3 id="room-title">បន្ទប់ប្រកួត</h3>
        <div id="status">កំពុងរង់ចាំគូប្រកួត...</div>
        <div id="board"></div>
        <button onclick="leaveRoom()">ត្រឡប់ទៅតារាងប្រកួតវិញ</button>
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
        const lobbyWs = new WebSocket(`${protocol}//${window.location.host}/ws/lobby`);

        lobbyWs.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.type === "lobby_update") {
                updateLobbyUI(data.players, data.matches, data.status);
            }
        };

        function registerPlayer() {
            myName = document.getElementById("playerName").value.trim();
            if (!myName) {
                alert("សូមបញ្ចូលឈ្មោះរបស់អ្នកជាមុនសិន!");
                return;
            }
            document.getElementById("register-box").classList.add("hidden");
            document.getElementById("tournament-lobby").classList.remove("hidden");
            lobbyWs.send(JSON.stringify({ type: "register", name: myName }));
        }

        function updateLobbyUI(players, matches, status) {
            // អាប់ដេតចំនួនកាក់របស់អ្នកលេងផ្ទាល់ខ្លួន
            if (players[myName] !== undefined) {
                document.getElementById("coinBalance").textContent = players[myName];
            }

            const listDiv = document.getElementById("match-list");
            let playerNames = Object.keys(players);
            listDiv.innerHTML = `<h4>អ្នកលេងសរុប (${playerNames.length} នាក់)</h4>`;
            
            if (matches.length > 0) {
                listDiv.innerHTML += "<h4>គូប្រកួត៖</h4>";
                matches.forEach((m, index) => {
                    listDiv.innerHTML += `
                        <div class="match-card">
                            <span>គូទី ${index+1}: ${m.white} (⚪ស) vs ${m.black} (⚫ខ្មៅ) [${m.status}]</span>
                            ${(myName === m.white || myName === m.black) && m.status === 'ongoing' ? `<button onclick="joinMatch('${m.room}')">ចូលលេង</button>` : ''}
                        </div>
                    `;
                });
            }

            if (playerNames.length >= 2 && status === "waiting") {
                document.getElementById("start-tour-btn").classList.remove("hidden");
            }
        }

        function startTournament() {
            lobbyWs.send(JSON.stringify({ type: "start_tournament" }));
        }

        function joinMatch(roomCode) {
            currentRoom = roomCode;
            document.getElementById("tournament-lobby").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");
            document.getElementById("room-title").textContent = `បន្ទប់ប្រកួត៖ ${roomCode}`;

            ws = new WebSocket(`${protocol}//${window.location.host}/ws/room/${roomCode}?name=${encodeURIComponent(myName)}`);

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.type === "init") {
                    myRole = data.role;
                    document.getElementById("status").textContent = `អ្នកគឺជាភាគី៖ ${myRole === 'white' ? 'ស (ខាងក្រោម)' : 'ខ្មៅ (ខាងលើ)'}`;
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
            if(ws) ws.close();
            document.getElementById("game-container").classList.add("hidden");
            document.getElementById("tournament-lobby").classList.remove("hidden");
        }

        function isWhitePiece(p) { return ["♖", "♘", "♗", "♕", "♔", "♙"].includes(p); }
        function isBlackPiece(p) { return ["♜", "♞", "♝", "♛", "♚", "♟"].includes(p); }

        function getValidMoves(r, c, piece) {
            let moves = [];
            let isWhite = isWhitePiece(piece);
            if (piece === "♙") {
                if (r-1 >= 0 && board[r-1][c] === "") moves.push({r: r-1, c: c});
                if (r-1 >= 0 && c-1 >= 0 && isBlackPiece(board[r-1][c-1])) moves.push({r: r-1, c: c-1});
                if (r-1 >= 0 && c+1 < 8 && isBlackPiece(board[r-1][c+1])) moves.push({r: r-1, c: c+1});
            } else if (piece === "♟") {
                if (r+1 < 8 && board[r+1][c] === "") moves.push({r: r+1, c: c});
                if (r+1 < 8 && c-1 >= 0 && isWhitePiece(board[r+1][c-1])) moves.push({r: r+1, c: c-1});
                if (r+1 < 8 && c+1 < 8 && isWhitePiece(board[r+1][c+1])) moves.push({r: r+1, c: c+1});
            } else {
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

lobby_connections = []

async def broadcast_lobby():
    data = json.dumps({"type": "lobby_update", **tournament})
    for conn in lobby_connections:
        await conn.send_text(data)

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_CONTENT

@app.websocket("/ws/lobby")
async def lobby_ws(websocket: WebSocket):
    await websocket.accept()
    lobby_connections.append(websocket)
    await websocket.send_text(json.dumps({"type": "lobby_update", **tournament}))
    try:
        while True:
            data = await websocket.receive_text()
            packet = json.loads(data)
            if packet["type"] == "register":
                name = packet["name"]
                if name not in tournament["players"]:
                    tournament["players"][name] = 100  # 🎁 ផ្ដល់ជូនកាក់ស្វាគមន៍ចំនួន 100 កាក់ពេលចុះឈ្មោះដំបូង
                await broadcast_lobby()
            elif packet["type"] == "start_tournament":
                player_names = list(tournament["players"].keys())
                random.shuffle(player_names)
                tournament["matches"] = []
                for i in range(0, len(player_names) - 1, 2):
                    room_id = f"room_{i//2 + 1}"
                    tournament["matches"].append({
                        "room": room_id,
                        "white": player_names[i],
                        "black": player_names[i+1],
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
                await broadcast_lobby()
    except WebSocketDisconnect:
        lobby_connections.remove(websocket)

@app.websocket("/ws/room/{room_id}")
async def room_ws(websocket: WebSocket, room_id: str, name: str):
    await websocket.accept()
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

                # ប្រសិនបើចប់ហ្គេម ផ្ដល់រង្វាន់កាក់ដល់អ្នកឈ្នះ ៥០កាក់
                if packet["gameOver"]:
                    winner_role = "white" if "ស" in packet["message"] else "black"
                    winner_name = room["players"].get(winner_role, {}).get("name")
                    if winner_name and winner_name in tournament["players"]:
                        tournament["players"][winner_name] += 50
                    await broadcast_lobby()

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

