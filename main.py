from fastapi import FastAPI as fp

app = fp()

@app.get("/great me")
def greating():
    return {"Message": "Hello World"}

