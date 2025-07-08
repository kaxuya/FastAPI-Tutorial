from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API"}


# this is the health check endpoint (indicates that api is live and working)
@app.get("/health")
def health_check():
    return {"status": "ok", "version": MODEL_VERSION, "model_loaded": model is not None}


@app.post("/predict")
def predict_premium(data: UserInput):
    user_input = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation,
    }

    prediction = predict_output(user_input)

    return JSONResponse(status_code=200, content={"predicted_category": prediction})
