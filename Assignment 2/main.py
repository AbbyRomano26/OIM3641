from fastapi import FastAPI
from pydantic import BaseModel
from pycaret.classification import load_model, predict_model
import pandas as pd

app = FastAPI(title="Income Predictor")

model = load_model("best_pipeline")

class PersonData(BaseModel):
    age: int
    workclass: str
    fnlwgt: int
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict")
def predict(data: PersonData):
    input_df = pd.DataFrame([{
        "age": data.age,
        "workclass": data.workclass,
        "fnlwgt": data.fnlwgt,
        "education": data.education,
        "education_num": data.education_num,
        "marital_status": data.marital_status,
        "occupation": data.occupation,
        "relationship": data.relationship,
        "race": data.race,
        "sex": data.sex,
        "capital_gain": data.capital_gain,
        "capital_loss": data.capital_loss,
        "hours_per_week": data.hours_per_week,
        "native_country": data.native_country
    }])

    preds = predict_model(model, data=input_df)
    prediction = preds["prediction_label"].iloc[0]

    return {"prediction": str(prediction)}
