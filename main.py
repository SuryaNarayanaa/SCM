from fastapi import FastAPI
from endpoint7 import ep_7

app = FastAPI()
app.include_router(ep_7)


@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)