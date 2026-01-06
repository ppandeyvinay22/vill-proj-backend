from fastapi import FastAPI

app = FastAPI(title="Village Food API")

@app.get("/")
def health():
    return {"status": "ok"}

