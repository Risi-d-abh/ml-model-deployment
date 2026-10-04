import pytest
from pydantic import ValidationError

from app.main import IrisFeatures, health, predict, root


sample = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
}


def test_root_returns_service_details() -> None:
    response = root()

    assert response["service"] == "iris-classifier"


def test_health_endpoint_is_available() -> None:
    response = health()

    assert response == {"status": "ok"}


def test_prediction_returns_a_known_iris_class() -> None:
    response = predict(IrisFeatures(**sample))

    assert response.prediction in {"setosa", "versicolor", "virginica"}


def test_prediction_response_has_expected_fields() -> None:
    response = predict(IrisFeatures(**sample))
    body = response.model_dump()

    assert set(body) == {"prediction", "class_id", "confidence"}
    assert body["class_id"] in {0, 1, 2}
    assert 0 <= body["confidence"] <= 1


def test_missing_feature_is_rejected() -> None:
    invalid_sample = {key: value for key, value in sample.items() if key != "petal_width"}

    with pytest.raises(ValidationError):
        IrisFeatures(**invalid_sample)


def test_non_positive_measurement_is_rejected() -> None:
    invalid_sample = {**sample, "sepal_length": 0}

    with pytest.raises(ValidationError):
        IrisFeatures(**invalid_sample)
