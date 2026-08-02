from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ហ្គេមអុកខ្មែរពេញលេញ</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #b30000;
        }
        #board {
            display: grid;
            grid-template-columns: repeat(8, 55px);
            grid-template-rows: repeat(8, 55px);
            gap: 2px;
            justify-content: center;
            margin: 20px auto;
            border: 4px solid #5c3a21;
            background-color: #5c3a21;
            width: max-content;
        }
        .square {
            width: 55px;
            height: 55px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
        }
        .light { background-color: #f0d9b5; }
        .dark { background-color: #b58863; }
        .selected { background-color: #7b61ff !important; }
        .highlight { background-color: #a9dfbf !important; }
        #status {
            font-size: 18px;
            font-weight: bold;
            margin-top: 15px;
            color: #333;
        }
    </style>
</head>
<body>

    <h1>♟️ ហ្គេមអុកខ្មែរ (តាមលក្ខខណ្ឌពេញលេញ) ♟️</h1>
    <div id="status">វេនអ្នកលេង៖ ស (ខាងក្រោម)</div>
    <div id="board"></div>

    <script>
        // ការរៀបចំទីតាំងដំបូងត្រឹមត្រូវតាមក្បួនអុកខ្មែរ៖
        // ជួរទី 0 និង 1 គឺគ្រាប់ខ្មៅ (ខាងលើ)
        // ជួរទី 2 គឺត្រីខ្មៅ
        // ជួរទី 5 គឺត្រីស
        // ជួរទី 6 និង 7 គឺគ្រាប់ស (ខាងក្រោម)
        const initialBoard = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"], // 0: គ្រាប់ធំខ្មៅ
            ["", "", "", "", "", "", "", ""],         // 1: ទទេ
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"], // 2: ត្រីខ្មៅ
            ["", "", "", "", "", "", "", ""],         // 3: ទទេ
            ["", "", "", "", "", "", "", ""],         // 4: ទទេ
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"], // 5: ត្រីស
            ["", "", "", "", "", "", "", ""],         // 6: ទទេ
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]  // 7: គ្រាប់ធំស
        ];

        let board = JSON.parse(JSON.stringify(initialBoard));
        let selectedPiece = null;
        let turn = 'white'; // 'white' or 'black'
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

            // ១. ច្បាប់គ្រាប់ត្រី (♙ ស ដើរឡើងលើ, ♟ ខ្មៅ ដើរចុះក្រោម)
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

            // ២. ច្បាប់គ្រាប់រាជ និង នាង - ដើរបាន ១ អូគ្រប់ទិស
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

            // ៣. ច្បាប់គ្រាប់គូទ - ដើរបណ្តោយបញ្ឈរ និងផ្ដេកឆ្ងាយ
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

            // ៤. ច្បាប់គ្រាប់សេះ - ដើរអក្សរ L
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

            // ៥. ច្បាប់គ្រាប់គោ - ដើរទម្រេត ១ អូគ្រប់ទិស ឬទៅមុខ ១ អូ
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
                    board[r][c] = selectedPiece.piece;
                    board[selectedPiece.r][selectedPiece.c] = "";

                    // ក្បួនប្រែក្លាយគ្រាប់ត្រីទៅជានាងពេលដល់ជួរទី 3 (ពីលើរាប់ចុះ សម្រាប់ត្រីស) និងជួរទី 4 (សម្រាប់ត្រីខ្មៅ)
                    if (selectedPiece.piece === "♙" && r === 2) board[r][c] = "♕"; 
                    if (selectedPiece.piece === "♟" && r === 5) board[r][c] = "♛"; 

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
