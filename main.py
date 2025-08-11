from fastapi import FastAPI

app = FastAPI(title="api2")

@app.get("/")
def root():
    return {"message": "hello api2"}

@app.get("/ping")
def ping():
    return {"pong": True}

@app.get("/healthz")
def health():
    return {"ok": True}
