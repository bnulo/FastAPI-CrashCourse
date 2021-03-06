from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "joe",
        "age": 12,
        "year": "year 12"
    }
}


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/")
def index():
    return {"name": "some name"}


# Path Parameter
@app.get("/get-student/{student-id}")
def get_student(student_id: int):
    return students[student_id]


@app.get("/more-complex-get-student/{student-id}")
def get_student(student_id: int = Path(
    None,  # default value
    description="The id of the student you want to view",  #
    gt=0,    # it must be greater than 0
    lt=5  # it must be less than 5
)
                ):
    return students[student_id]

#  gt Greater than
#  lt Less than
#  ge Greater than or equals to
#  le Less than or equals to


# Query Parameter
# key-value of search and Python:
# google.com/results?search=Python
@app.get("/get-by-name")
def get_student(name: str):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}


@app.get("/get-by-name")
def get_student_with_optional(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}


@app.get("/get-by-name")
def get_student_with_two_query_parameter(*, name: Optional[str] = None, age: int):
    # optional arguments have to  be last in function definition, so we use *

    for student_id in students:
        if students[student_id]["name"] == name and students[student_id]["age"] == age:
            return students[student_id]
    return {"Data": "Not Found"}


# Combining Path and Query Parameters
@app.get("/get-by-name/{student_id}")
def get_student_with_two_query_parameter(*, student_id: int, name: Optional[str] = None):

    if students[student_id]["name"] == name:
        return students[student_id]
    return {"Data": "Not Found"}


# Post
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists"}
    students[student_id] = student
    return students[student_id]


# Put
@app.post("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    if student.name is not None:
        students[student_id].name = student.name
    if student.age is not None:
        students[student_id].age = student.age
    if student.year is not None:
        students[student_id].year = student.year

    return students[student_id]


# Delete
@app.delete("/delete/{student_id}")
def delete(student_id: int):
    if student_id not in students:
        return {"Error": "student does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}
