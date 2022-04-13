from fastapi import FastAPI
from predict import HousePriceModel

app = FastAPI()

@app.get("/")
def root():
    return {"status": "online"}

@app.post("/predict")
def predict(inputs: dict):
    model = HousePriceModel()
    pred = model.predict(inputs)[0]
    return pred
