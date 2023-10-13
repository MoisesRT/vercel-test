from fastapi import FastAPI

app = FastAPI()

from server.routes import router as NoteRouter


@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to my notes application, use the /docs route to proceed"
    }


app.include_router(NoteRouter, prefix="/note")
