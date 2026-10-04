from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.model import IrisClassifier


class IrisFeatures(BaseModel):
    sepal_length: float = Field(gt=0, le=10)
    sepal_width: float = Field(gt=0, le=10)
    petal_length: float = Field(gt=0, le=10)
    petal_width: float = Field(gt=0, le=10)


class Prediction(BaseModel):
    prediction: str
    class_id: int
    confidence: float


app = FastAPI(title="Iris Classification API", version="1.0.0")
classifier = IrisClassifier()


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "iris-classifier", "docs": "/docs"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=Prediction)
def predict(features: IrisFeatures) -> Prediction:
    label, class_id, confidence = classifier.predict(list(features.model_dump().values()))
    return Prediction(prediction=label, class_id=class_id, confidence=round(confidence, 4))
