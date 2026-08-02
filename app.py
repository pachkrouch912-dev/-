from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ហ្គេមអុកខ្មែរអនឡាញ</title>
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
            grid-template-columns: repeat(8, 60px);
            grid-template-rows: repeat(8, 60px);
            gap: 2px;
            justify-content: center;
            margin: 20px auto;
            border: 4px solid #5c3a21;
            background-color: #5c3a21;
            width: max-content;
        }
        .square {
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            cursor: pointer;
            user-select: none;
        }
        .light { background-color: #f0d9b5; }
        .dark { background-color: #b58863; }
        .selected { background-color: #7b61ff !important; }
        #status {
            font-size: 18px;
            font-weight: bold;
            margin-top: 15px;
            color: #333;
        }
    </style>
</head>
<body>

    <h1>♟️ ហ្គេមអុកខ្មែរ ♟️</h1>
    <div id="status">វេនអ្នកលេងពណ៌៖ ស</div>
    <div id="board"></div>

    <script>
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

        function renderBoard() {
            const boardElement = document.getElementById("board");
            boardElement.innerHTML = "";

            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const square = document.createElement("div");
                    square.classList.add("square");
                    square.classList.add((r + c) % 2 === 0 ? "light" : "dark");
                    square.dataset.row = r;
                    square.dataset.col = c;
                    
                    square.textContent = board[r][c];
                    square.addEventListener("click", () => handleSquareClick(r, c));
                    boardElement.appendChild(square);
                }
            }
        }

        function handleSquareClick(r, c) {
            const clickedPiece = board[r][c];

            if (selectedPiece) {
                board[selectedPiece.r][selectedPiece.c] = "";
                board[r][c] = selectedPiece.piece;
                selectedPiece = null;
                turn = turn === 'white' ? 'black' : 'white';
                document.getElementById("status").textContent = `វេនអ្នកលេងពណ៌៖ ${turn === 'white' ? 'ស' : 'ខ្មៅ'}`;
                renderBoard();
            } else if (clickedPiece !== "") {
                selectedPiece = { r, c, piece: clickedPiece };
                renderBoard();
                const squares = document.querySelectorAll(".square");
                squares[r * 8 + c].classList.add("selected");
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

