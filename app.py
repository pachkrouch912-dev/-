from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str
    opponent_name: str = "Gemini ជើងខ្លាំង"

@app.post("/api/gemini-chat")
async def gemini_chat(req: ChatRequest):
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return {"reply": "ហាសហា! ខ្ញុំត្រៀមខ្លួនរួចជាស្រេចហើយ ចាំមើលរឿងអស្ចារ្យលើក្ដារអុកនេះ!"}
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"អ្នកគឺជាគូប្រកួតអុកខ្មែរដ៏កំប្លែង ឌឺដងបន្តិច ប៉ុន្តែរួសរាយ និងស្រស់ស្រាយ។ អ្នកលេងបាននិយាយមកកាន់អ្នកថា: '{req.message}'។ សូមតបមកវិញជាភាសាខ្មែរខ្លីៗ ប្រកបដោយភាពកំប្លែង ស្វាហាប់ និងរស់រវើកក្នុងនាមជាគូប្រកួតអុក。"
        response = model.generate_content(prompt)
        return {"reply": response.text.strip()}
    except Exception as e:
        return {"reply": "អូ៎ អ៊ីនធឺណិតរាងទាក់បន្តិចហើយ ប៉ុន្តែទឹកមុខខ្ញុំនៅតែញញឹមហៅគូប្រកួតលេងដដែល!"}

@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "ok"}

@app.get("/manifest.json")
async def get_manifest():
    return JSONResponse({
        "name": "អុកខ្មែរអនឡាញ - WebRTC & Gemini",
        "short_name": "អុកខ្មែរ",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a0f18",
        "theme_color": "#1b2838",
        "description": "ហ្គេមអុកខ្មែរអនឡាញ ជាមួយ WebRTC Voice Call និង Gemini AI",
        "id": "OukkhmerWebRTC",
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
    self.addEventListener('install', (event) => { self.skipWaiting(); });
    self.addEventListener('activate', (event) => { return self.clients.claim(); });
    self.addEventListener('fetch', (event) => {
        event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
    });
    """
    return PlainTextResponse(sw_code, media_type="application/javascript")

@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join("www", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>រកមិនឃើញឯកសារ index.html ទេ! សូមបង្កើតវាក្នុងថត www</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

