import os

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression


def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    csv_path = os.path.join(root_dir, "USA_Housing.csv")
    model_dir = os.path.join(root_dir, "models")
    model_path = os.path.join(model_dir, "housing_model.pkl")

    df = pd.read_csv(csv_path)
    feature_columns = [
        "Avg. Area Income",
        "Avg. Area House Age",
        "Avg. Area Number of Rooms",
        "Avg. Area Number of Bedrooms",
        "Area Population",
    ]

    X = df[feature_columns]
    y = df["Price"]

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, model_path, compress=3)
    print(f"Saved retrained model to {model_path}")


if __name__ == "__main__":
    main()
