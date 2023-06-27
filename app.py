import asyncio
import uvicorn

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    headers = dict(request.headers)
    return headers


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"web socket response: {data}")


@app.get("/ws", response_class=HTMLResponse)
async def ws_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sse")
async def sse_endpoint():
    async def generate():
        count = 0
        while True:
            yield f"data: Message {count}\n"
            count += 1
            await asyncio.sleep(1)

    return StreamingResponse(generate(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
