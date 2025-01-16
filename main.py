from fastapi import FastAPI
import numpy as np
from pydantic import BaseModel
import cloudpickle
import pandas as pd

app = FastAPI()

class InputData(BaseModel):
    date: str
    latitude: float
    longitude: float

with open('model.pkl', 'rb') as file:
    model = cloudpickle.load(file)

def get_prediction(pred):
    count = len(pred[0])
    sum = 0
    for list in pred[0]:
        sum += list[0]
    return sum / count

@app.post('/predict')
async def predict(input_data: InputData):
    data = pd.DataFrame({ 'date': [input_data.date], 'latitude': [input_data.latitude], 'longitude': [input_data.longitude] })
    data['date'] = pd.to_datetime(data['date'])

    pred, _ = model.predict(data)

    return { "prediction": float(get_prediction(pred))}