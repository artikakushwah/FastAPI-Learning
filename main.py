from fastapi import FastAPI, HTTPException, Path
import json

from fastapi.params import Query

app = FastAPI()


@app.get("/")
def greet():
    return {"message": "Hello and welcome to FastAPI!"}


@app.get("/Hello")
def hello():
    return {"message": "This is a Hello endpoint!"}


# Helper function
def load_data():
    with open("students.json", "r") as file:
        return json.load(file)


@app.get("/students")
def students():
    return load_data()

#path parameter
@app.get("/students/{students_id}")
def get_id(
    students_id: str = Path(
        ...,
        description="The ID of the student to retrieve"
    )
):
    data = load_data()

    if students_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return data[students_id]

#query parameter
@app.get('/filter')
def filter_student(
    course : str = Query(None, description="show only students in this course", examples=["Python"])):
    
    data = load_data()

    if course is None:
        return data

    filtered = {}
    for student_id , info in data.items():
        if info["course"].lower() == course.lower():
            filtered[student_id] = info

    return filtered

SORT_FIELDS = ["marks", "age", "name"]
SORT_ORDER  = ["asc", "desc"]

@app.get('/sort')
def sort_students(
    sort_by : str = Query(None, description="Sort by marks, name, age",
    examples=["marks"]),
    order : str = Query("asc", description="asc or desc", examples=["asc", "desc"])
):
    #If the given sort_by input dosn't belongs to any (marks, age, name) we will raise an error.
    if sort_by not in SORT_FIELDS:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid sort_by '{sort_by}, Choose from {SORT_FIELDS}"
        )
    #If the given order input dosn't belongs to any (asc, desc) we will raise an error.
    if order not in SORT_ORDER:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid order '{order}. Choose from {SORT_ORDER}"
        )


    data = load_data()

    #step-1 Turn the dictionary into a list, putting the ID inside each student
    student = []
    for student_id , info in data.items():
        info['id'] = student_id
        student.append(info)

    #Step-2 Sort the list by the choosen field
    reverse = (order=="desc")
    sorted_students = sorted(student, key=lambda s: s[sort_by],reverse=reverse)

    return sorted_students