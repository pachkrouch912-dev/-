from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

rooms = {}

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ហ្គេមអុកខ្មែរអនឡាញ (Ok Chaktrong + Score)</title>
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
        #menu, #game-container { margin-top: 20px; }
        .box {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        input {
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin: 5px;
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
        
        #scoreboard {
            font-size: 16px;
            font-weight: bold;
            margin: 10px 0;
            color: #2c3e50;
            background: #eef2f7;
            display: inline-block;
            padding: 6px 20px;
            border-radius: 15px;
        }
        #status {
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
            color: #444;
            background: #fff;
            display: inline-block;
            padding: 8px 25px;
            border-radius: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        #board {
            display: grid;
            grid-template-columns: repeat(8, 60px);
            grid-template-rows: repeat(8, 60px);
            gap: 2px;
            justify-content: center;
            margin: 10px auto;
            border: 5px solid #5c3a21;
            background-color: #5c3a21;
            border-radius: 6px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            width: max-content;
        }
        .square {
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 34px;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            transition: background 0.2s;
        }
        .light { background-color: #f0d9b5; }
        .dark { background-color: #b58863; }
        .selected { background-color: #7b61ff !important; }
        .highlight { background-color: #85c1e9 !important; }

        .white-piece {
            color: #ffffff;
            text-shadow: 1px 1px 2px #000, 0 0 1em #000, 0 0 0.2em #000;
        }
        .black-piece {
            color: #111111;
            text-shadow: 1px 1px 2px #fff, 0 0 1em #fff, 0 0 0.2em #fff;
        }
        .hidden { display: none; }
        #restart-btn {
            background-color: #27ae60;
            margin-top: 10px;
            display: none;
        }
    </style>
</head>
<body>

    <h1>♟️ ហ្គេមអុកខ្មែរអនឡាញ (Ok Chaktrong) ♟️</h1>

    <div id="menu" class="box">
        <h3>ចូលបន្ទប់លេងហ្គេម</h3>
        <input type="text" id="roomInput" placeholder="បញ្ចូលលេខបន្ទប់ (ឧ. 123)"><br>
        <button onclick="joinRoom()">ចូលលេង</button>
    </div>

    <div id="game-container" class="hidden">
        <div id="scoreboard">ពិន្ទុ៖ ⚪ ស [ <span id="whiteScore">0</span> ] - [ <span id="blackScore">0</span> ] ⚫ ខ្មៅ</div><br>
        <div id="status">កំពុងរង់ចាំគូប្រកួត...</div>
        <div id="board"></div>
        <button id="restart-btn" onclick="requestRestart()">លេងសារថ្មី (Restart)</button>
    </div>

    <script>
        let ws = null;
        let myRole = null;
        let roomCode = null;

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

        function joinRoom() {
            roomCode = document.getElementById("roomInput").value.trim();
            if (!roomCode) {
                alert("សូមបញ្ចូលលេខបន្ទប់ជាមុនសិន!");
                return;
            }

            document.getElementById("menu").classList.add("hidden");
            document.getElementById("game-container").classList.remove("hidden");

            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws/${roomCode}`);

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                if (data.type === "init") {
                    myRole = data.role;
                    document.getElementById("status").textContent = `អ្នកគឺជាភាគី៖ ${myRole === 'white' ? 'ស (ខាងក្រោម)' : 'ខ្មៅ (ខាងលើ)'}`;
                } else if (data.type === "update" || data.type === "game_over") {
                    board = data.board;
                    turn = data.turn;
                    gameOver = data.gameOver;
                    document.getElementById("status").textContent = data.message;
                    
                    document.getElementById("whiteScore").textContent = data.whiteScore;
                    document.getElementById("blackScore").textContent = data.blackScore;

                    if (gameOver) {
                        document.getElementById("restart-btn").style.display = "inline-block";
                    } else {
                        document.getElementById("restart-btn").style.display = "none";
                    }

                    selectedPiece = null;
                    validMoves = [];
                    renderBoard();
                } else if (data.type === "error") {
                    alert(data.message);
                    location.reload();
                }
            };
        }

        function requestRestart() {
            ws.send(JSON.stringify({ type: "restart" }));
        }

        function isWhitePiece(piece) {
            return ["♖", "♘", "♗", "♕", "♔", "♙"].includes(piece);
        }

        function isBlackPiece(piece) {
            return ["♜", "♞", "♝", "♛", "♚", "♟"].includes(piece);
        }

        function getValidMoves(r, c, piece) {
            let moves = [];
            let isWhite = isWhitePiece(piece);

            if (piece === "♙") { 
                let nr = r - 1;
                if (nr >= 0 && board[nr][c] === "") moves.push({r: nr, c: c});
                if (r - 1 >= 0 && c - 1 >= 0 && isBlackPiece(board[r-1][c-1])) moves.push({r: r-1, c: c-1});
                if (r - 1 >= 0 && c + 1 < 8 && isBlackPiece(board[r-1][c+1])) moves.push({r: r-1, c: c+1});
            } else if (piece === "♟") { 
                let nr = r + 1;
                if (nr < 8 && board[nr][c] === "") moves.push({r: nr, c: c});
                if (r + 1 < 8 && c - 1 >= 0 && isWhitePiece(board[r+1][c-1])) moves.push({r: r+1, c: c-1});
                if (r + 1 < 8 && c + 1 < 8 && isWhitePiece(board[r+1][c+1])) moves.push({r: r+1, c: c+1});
            } else if (piece === "♔" || piece === "♚" || piece === "♕" || piece === "♛") {
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
            } else if (piece === "♖" || piece === "♜") {
                let directions = [[-1,0], [1,0], [0,-1], [0,1]];
                for (let d of directions) {
                    let step = 1;
                    while (true) {
                        let nr = r + d[0] * step, nc = c + d[1] * step;
                        if (nr < 0 || nr >= 8 || nc < 0 || nc >= 8) break;
                        let target = board[nr][nc];
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
            } else if (piece === "♘" || piece === "♞") {
                let knightMoves = [[-2,-1], [-2,1], [-1,-2], [-1,2], [1,-2], [1,2], [2,-1], [2,1]];
                for (let m of knightMoves) {
                    let nr = r + m[0], nc = c + m[1];
                    if (nr >= 0 && nr < 8 && nc >= 0 && nc < 8) {
                        let target = board[nr][nc];
                        if (target === "" || (isWhite && isBlackPiece(target)) || (!isWhite && isWhitePiece(target))) {
                            moves.push({r: nr, c: nc});
                        }
                    }
                }
            } else if (piece === "♗" || piece === "♝") {
                let elephantMoves = [
                    [-1,-1], [-1,1], [1,-1], [1,1],
                    isWhite ? [-1,0] : [1,0]
                ];
                for (let m of elephantMoves) {
                    let nr = r + m[0], nc = c + m[1];
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
            const boardElement = document.getElementById("board");
            boardElement.innerHTML = "";

            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const square = document.createElement("div");
                    square.classList.add("square");
                    square.classList.add((r + c) % 2 === 0 ? "light" : "dark");
                    
                    if (selectedPiece && selectedPiece.r === r && selectedPiece.c === c) {
                        square.classList.add("selected");
                    }

                    if (validMoves.some(m => m.r === r && m.c === c)) {
                        square.classList.add("highlight");
                    }

                    const piece = board[r][c];
                    if (piece !== "") {
                        const pieceSpan = document.createElement("span");
                        pieceSpan.textContent = piece;
                        if (isWhitePiece(piece)) {
                            pieceSpan.classList.add("white-piece");
                        } else {
                            pieceSpan.classList.add("black-piece");
                        }
                        square.appendChild(pieceSpan);
                    }

                    square.addEventListener("click", () => handleSquareClick(r, c));
                    boardElement.appendChild(square);
                }
            }
        }

        function handleSquareClick(r, c) {
            if (gameOver) return;
            if (turn !== myRole) {
                alert("មិនទាន់ដល់វេនរបស់អ្នកទេ!");
                return;
            }

            const clickedPiece = board[r][c];

            if (selectedPiece) {
                let isValid = validMoves.some(m => m.r === r && m.c === c);
                if (isValid) {
                    let targetPiece = board[r][c];
                    let movingPiece = selectedPiece.piece;
                    let isGameOver = false;
                    let winningColor = null;

                    if (targetPiece === "♚") {
                        isGameOver = true;
                        winningColor = "white";
                    } else if (targetPiece === "♔") {
                        isGameOver = true;
                        winningColor = "black";
                    }

                    if (movingPiece === "♙" && r === 2) movingPiece = "♕";
                    else if (movingPiece === "♟" && r === 5) movingPiece = "♛";

                    board[r][c] = movingPiece;
                    board[selectedPiece.r][selectedPiece.c] = "";

                    let nextTurn = turn === 'white' ? 'black' : 'white';

                    ws.send(JSON.stringify({
                        type: "move",
                        board: board,
                        turn: nextTurn,
                        gameOver: isGameOver,
                        winningColor: winningColor
                    }));
                }
                selectedPiece = null;
                validMoves = [];
                renderBoard();
            } else if (clickedPiece !== "") {
                if ((myRole === 'white' && isWhitePiece(clickedPiece)) || (myRole === 'black' && isBlackPiece(clickedPiece))) {
                    selectedPiece = { r, c, piece: clickedPiece };
                    validMoves = getValidMoves(r, c, clickedPiece);
                    renderBoard();
                }
            }
        }
    </script>
</body>
</html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, room: str, websocket: WebSocket):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def broadcast(self, room: str, message: dict):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_CONTENT

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    if room_id not in rooms:
        rooms[room_id] = {
            "board": json.loads(json.dumps([
                ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
                ["", "", "", "", "", "", "", ""],
                ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
                ["", "", "", "", "", "", "", ""],
                ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
            ])),
            "turn": "white",
            "gameOver": False,
            "message": "វេនអ្នកលេង៖ ស (ខាងក្រោម)",
            "whiteScore": 0,
            "blackScore": 0,
            "players": []
        }

    room = rooms[room_id]
    
    if len(room["players"]) >= 2:
        await websocket.accept()
        await websocket.send_text(json.dumps({"type": "error", "message": "បន្ទប់នេះមានអ្នកចូលពេញហើយ!"}))
        await websocket.close()
        return

    role = "white" if len(room["players"]) == 0 else "black"
    room["players"].append(websocket)

    await manager.connect(room_id, websocket)
    
    await websocket.send_text(json.dumps({
        "type": "init",
        "role": role
    }))
    
    await manager.broadcast(room_id, {
        "type": "update",
        "board": room["board"],
        "turn": room["turn"],
        "gameOver": room["gameOver"],
        "message": room["message"],
        "whiteScore": room["whiteScore"],
        "blackScore": room["blackScore"]
    })

    try:
        while True:
            data = await websocket.receive_text()
            packet = json.loads(data)
            
            if packet["type"] == "move":
                room["board"] = packet["board"]
                room["turn"] = packet["turn"]
                room["gameOver"] = packet["gameOver"]

                if packet["gameOver"]:
                    if packet["winningColor"] == "white":
                        room["whiteScore"] += 1
                        room["message"] = "🎉 ភាគី «ស» បានឈ្នះជុំនេះ!"
                    else:
                        room["blackScore"] += 1
                        room["message"] = "🎉 ភាគី «ខ្មៅ» បានឈ្នះជុំនេះ!"
                else:
                    room["message"] = f"វេនអ្នកលេង៖ {'ស' if room['turn'] == 'white' else 'ខ្មៅ'}"

                await manager.broadcast(room_id, {
                    "type": "update",
                    "board": room["board"],
                    "turn": room["turn"],
                    "gameOver": room["gameOver"],
                    "message": room["message"],
                    "whiteScore": room["whiteScore"],
                    "blackScore": room["blackScore"]
                })
            
            elif packet["type"] == "restart":
                # កំណត់ក្តារខៀនសារថ្មីពេលចង់លេងតទៀត
                room["board"] = json.loads(json.dumps([
                    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
                    ["", "", "", "", "", "", "", ""],
                    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
                    ["", "", "", "", "", "", "", ""],
                    ["", "", "", "", "", "", "", ""],
                    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
                    ["", "", "", "", "", "", "", ""],
                    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
                ]))
                room["turn"] = "white"
                room["gameOver"] = False
                room["message"] = "វេនអ្នកលេង៖ ស (ខាងក្រោម)"

                await manager.broadcast(room_id, {
                    "type": "update",
                    "board": room["board"],
                    "turn": room["turn"],
                    "gameOver": room["gameOver"],
                    "message": room["message"],
                    "whiteScore": room["whiteScore"],
                    "blackScore": room["blackScore"]
                })

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        if room_id in rooms and websocket in rooms[room_id]["players"]:
            rooms[room_id]["players"].remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

