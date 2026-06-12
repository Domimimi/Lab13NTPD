from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(data: dict):
    # Prosta atrapa (mock) odpowiedzi modelu ML
    return {
        "status": "success",
        "version":"2.0",
        "prediction": "mock_result",
        "input_data": data
    }