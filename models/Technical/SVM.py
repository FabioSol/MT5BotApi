from models.Technical.pipelines import y_pipeline,x_pipeline
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class SVM(BaseEstimator, ClassifierMixin):
    def __init__(self, C=1.0, kernel='rbf', gamma='scale',random_state=42069,**kwargs):
        self.C = C
        self.kernel = kernel
        self.gamma = gamma
        self.scaler = StandardScaler()
        self.randomstate=random_state
        self.model = SVC(C=self.C, kernel=self.kernel, gamma=self.gamma, random_state=random_state)

    def fit(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        return self

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def __str__(self):
        return f"C: {self.C} kernel: { self.kernel} gamma: {self.gamma} rs:{self.randomstate}"

if __name__ == '__main__':
    from data.reader import Reader
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix

    df = Reader.get_pd("EURUSD", "D1")
    X=x_pipeline(df)
    y=y_pipeline(df)
    model = SVM()
    model.fit(X,y)
    y_pred = model.predict(X)
    cm = confusion_matrix(y, y_pred)

    # Plot confusion matrix using seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', cbar=False)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()


