import joblib

def load_model():
    model = joblib.load("models/housing_model.pkl")
    return model

model = load_model()