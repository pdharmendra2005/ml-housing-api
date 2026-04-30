from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.model_loader import model

app = FastAPI()

# Allow local browser testing and common origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Define input schema
class InputData(BaseModel):
    features: list[float]

# Health check
@app.get("/")
def read_root():
    return {"message": "ML Model API is running"}

# Prediction endpoint
@app.post("/predict")
def predict(data: InputData):
    prediction = model.predict([data.features])
    return {"prediction": prediction.tolist()}