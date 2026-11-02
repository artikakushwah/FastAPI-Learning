from http.client import HTTPException, Path
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

#Helper funtion 
def load_data():
    with open("students.json", "r") as file:
        return json.load(file)


@app.get("/students") # Get endpoint for the /students URL
def students():
    return load_data()

#students_id is a path parameter that will be passed in the URL
@app.get("/students/{students_id}") # Get endpoint for the /students/{student_id} URL
def get_id(students_id: str=Path(..., description="The ID of the student to retrieve")):
    data = load_data()
    if students_id not in data:
            raise HTTPException(status_code=404, detail="Student not found")
    return data[students_id]