from fastapi import FastAPI

app = FastAPI()

@app.get("/") # Get endpoint for the root URL
def greet():
    return {"Hello nd welcome to FastAPI!"}

@app.get('/Hello')
def hello():
    return{"This is a Hello endpoint!"}
