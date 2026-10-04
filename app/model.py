from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier


class IrisClassifier:
    def __init__(self) -> None:
        dataset = load_iris()
        self.labels = dataset.target_names
        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(dataset.data, dataset.target)

    def predict(self, features: list[float]) -> tuple[str, int, float]:
        class_id = int(self.model.predict([features])[0])
        confidence = float(self.model.predict_proba([features])[0][class_id])
        return self.labels[class_id], class_id, confidence
