from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

class InputData(BaseModel):
    date: str
    latitude: float
    longitude: float

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

def get_prediction(pred):
    count = len(pred[0])
    sum = 0
    for list in pred[0]:
        sum += list[0]
    return sum / count

@app.post('/predict/')
async def predict(input_data: InputData):
    try:
        data = pd.DataFrame({ 'date': [input_data.date], 'latitude': [input_data.latitude], 'longitude': [input_data.longitude] })
        data['date'] = pd.to_datetime(data['date'])

        pred, _ = model.predict(data, quantiles = [0.1, 0.5, 0.9])
        
        return { "prediction": float(get_prediction(pred))}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)