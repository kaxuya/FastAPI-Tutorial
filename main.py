from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()


def load_data():
    with open("patients.json") as f:
        data = json.load(f)

    return data


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
