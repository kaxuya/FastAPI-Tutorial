from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[
        str, Field(..., description="Name of the patient", examples=["Ananya Verma"])
    ]
    city: Annotated[
        str, Field(..., description="City of the patient", examples=["Guwahati"])
    ]
    age: Annotated[
        int, Field(..., gt=0, lt=120, description="Age of the patient", examples=[28])
    ]
    gender: Annotated[
        Literal["male", "female", "others"],
        Field(..., description="Gender of the patient", examples=["female"]),
    ]
    height: Annotated[
        float,
        Field(
            ..., gt=0, description="Height of the patient in meters", examples=[1.75]
        ),
    ]
    weight: Annotated[
        float,
        Field(..., gt=0, description="Weight of the patient in kg", examples=[85]),
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height * self.height), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


def load_data():
    with open("patients.json") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/view")
def view():
    data = load_data()
    return data


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ..., description="ID of the patient in the database", example="P001"
    )  # these ... dots means this field is compulsory
):
    # load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="sort by height, weight of bmi"),
    order: str = Query("asc", description="sort in asc or desc order"),
):
    valid_fields = {"height", "weight", "bmi"}
    orders = {"asc", "desc"}

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid field select from {valid_fields}"
        )

    if order not in orders:
        raise HTTPException(
            status_code=400, detail=f"Invalid order select from {orders}"
        )

    data = load_data()
    sort_desc = True if order == "desc" else False

    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=sort_desc)

    return sorted_data

@app.post('/create') # this post request will get automatically the json data recieved in the request body
def create_patient(patient: Patient):
    # load existing data
    data = load_data()

    # check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # add the patient to the database
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})