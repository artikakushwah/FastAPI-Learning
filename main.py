import json

from fastapi import FastAPI
from h11 import Data

app = FastAPI()

@app.get("/") # Get endpoint for the root URL
def greet():
    return {"Hello nd welcome to FastAPI!"}

@app.get('/Hello')
def hello():
    return{"This is a Hello endpoint!"}


def get_data():
    with open("students.json", "r") as file:
        return json.load(file)


@app.get("/students") # Get endpoint for the /students URL
def students():
    return get_data()