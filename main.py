from fastapi import FastAPI
from endpoint1 import ep_1
from endpoint2 import ep_2
from endpoint3 import ep_3
from endpoint4 import ep_4
from endpoint5 import ep_5
from endpoint6 import ep_6
from endpoint7 import ep_7

app = FastAPI()
app.include_router(ep_1)
app.include_router(ep_2)
app.include_router(ep_3)
app.include_router(ep_4)
app.include_router(ep_5)
app.include_router(ep_6)
app.include_router(ep_7)



@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)