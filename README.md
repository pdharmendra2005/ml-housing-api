# ML Demo Deployment

This project contains a FastAPI service that loads a trained regression model from `models/housing_model.pkl` and exposes a prediction endpoint at `/predict`.

## Local development

1. Activate your virtual environment:

```powershell
& .\myvenv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the API:

```powershell
uvicorn app.main:app --reload
```

4. Check the service:

- Health: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

## Prediction example

Use the browser console or a script to POST JSON to `/predict`:

```js
fetch("http://127.0.0.1:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    features: [88244.61487, 6.548375433, 8.765481292, 3.36, 25791.99499]
  })
})
  .then(r => r.json())
  .then(data => console.log(data));
```

## Docker

Build and run the container:

```powershell
docker build -t ml-housing-api .
docker run -p 8000:80 ml-housing-api
```

## CI Pipeline

A GitHub Actions workflow is included to install dependencies and run tests on push or pull request.
