from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ហ្គេមអុកខ្មែរ (Ok Chaktrong Standard)</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            text-align: center;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #8B0000;
            margin-bottom: 5px;
        }
        #status {
            font-size: 18px;
            font-weight: bold;
            margin: 15px 0;
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
            font-size: 32px;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            transition: background 0.2s;
        }
        .light { background-color: #f0d9b5; }
        .dark { background-color: #b58863; }
        .selected { background-color: #7b61ff !important; }
        .highlight { background-color: #85c1e9 !important; }
    </style>
</head>
<body>

    <h1>♟️ ហ្គេមអុកខ្មែរ (Ok Chaktrong) ♟️</h1>
    <div id="status">វេនអ្នកលេង៖ ស (ខាងក្រោម)</div>
    <div id="board"></div>

    <script>
        // ការរៀបចំក្តារខៀនដំបូងតាមស្តង់ដារអុកខ្មែរ
        const initialBoard = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"], // ជួរ 0: គ្រាប់ធំខ្មៅ
            ["", "", "", "", "", "", "", ""],         // ជួរ 1: ទទេ
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"], // ជួរ 2: ត្រីខ្មៅ
            ["", "", "", "", "", "", "", ""],         // ជួរ 3: ទទេ
            ["", "", "", "", "", "", "", ""],         // ជួរ 4: ទទេ
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"], // ជួរ 5: ត្រីស
            ["", "", "", "", "", "", "", ""],         // ជួរ 6: ទទេ
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]  // ជួរ 7: គ្រាប់ធំស
        ];

        let board = JSON.parse(JSON.stringify(initialBoard));
        let selectedPiece = null;
        let turn = 'white'; 
        let validMoves = [];

        function isWhitePiece(piece) {
            return ["♖", "♘", "♗", "♕", "♔", "♙"].includes(piece);
        }

        function isBlackPiece(piece) {
            return ["♜", "♞", "♝", "♛", "♚", "♟"].includes(piece);
        }

        function getValidMoves(r, c, piece) {
            let moves = [];
            let isWhite = isWhitePiece(piece);

            // ១. ច្បាប់គ្រាប់ត្រី (ដើរទៅមុខ ១ អូ និងស៊ីទាស់ខ្វែង ១ អូ)
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
            }

            // ២. រាជ និង នាង (ដើរ ១ អូគ្រប់ទិសទាំង ៨)
            else if (piece === "♔" || piece === "♚" || piece === "♕" || piece === "♛") {
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

            // ៣. គូទ (ដើរបណ្តោយបញ្ឈរ និងផ្តេក ចម្ងាយគ្មានកំណត់)
            else if (piece === "♖" || piece === "♜") {
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
            }

            // ៤. សេះ (ដើរលោតរូបអក្សរ L)
            else if (piece === "♘" || piece === "♞") {
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
            }

            // ៥. គោ (ដើរទម្រេត ១ អូគ្រប់ទិស ឬទៅមុខ ១ អូ)
            else if (piece === "♗" || piece === "♝") {
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

                    square.textContent = board[r][c];
                    square.addEventListener("click", () => handleSquareClick(r, c));
                    boardElement.appendChild(square);
                }
            }
        }

        function handleSquareClick(r, c) {
            const clickedPiece = board[r][c];

            if (selectedPiece) {
                let isValid = validMoves.some(m => m.r === r && m.c === c);
                if (isValid) {
                    let movingPiece = selectedPiece.piece;

                    // ច្បាប់ស្តង់ដារអុកខ្មែរ៖ 
                    // - ត្រីស (♙) ដើរដល់ជួរទី 3 ពីលើ (Index 2) ប្រែក្លាយជานាង (♕)
                    // - ត្រីខ្មៅ (♟) ដើរដល់ជួរទី 6 ពីលើ (Index 5) ប្រែក្លាយជានាង (♛)
                    if (movingPiece === "♙" && r === 2) {
                        movingPiece = "♕";
                    } else if (movingPiece === "♟" && r === 5) {
                        movingPiece = "♛";
                    }

                    board[r][c] = movingPiece;
                    board[selectedPiece.r][selectedPiece.c] = "";

                    turn = turn === 'white' ? 'black' : 'white';
                    document.getElementById("status").textContent = `វេនអ្នកលេង៖ ${turn === 'white' ? 'ស (ខាងក្រោម)' : 'ខ្មៅ (ខាងលើ)'}`;
                }
                selectedPiece = null;
                validMoves = [];
                renderBoard();
            } else if (clickedPiece !== "") {
                if ((turn === 'white' && isWhitePiece(clickedPiece)) || (turn === 'black' && isBlackPiece(clickedPiece))) {
                    selectedPiece = { r, c, piece: clickedPiece };
                    validMoves = getValidMoves(r, c, clickedPiece);
                    renderBoard();
                }
            }
        }

        renderBoard();
    </script>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_CONTENT

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

