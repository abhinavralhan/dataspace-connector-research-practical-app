import pickle
import logging
from .constants import *
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, accuracy_score


class DecisionTreeModel:
    def __init__(self):
        self.model_version = DEFAULT_MODEL
        self.hyperparameters = DEFAULT_HYPERPARAMETERS
        with open(f"{BASE_DIR}/model-{self.model_version}.pkl", "rb") as f:
            model = pickle.load(f)
        self.model = model
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.y_pred = None

    def train(self, data):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(data.drop(columns=['healthState']),
                                                                                data[['healthState']],
                                                                                test_size=0.3,
                                                                                random_state=1)
        clf = DecisionTreeClassifier(max_depth=int(self.hyperparameters['max_depth']),
                                     random_state=int(self.hyperparameters['random_state']),
                                     min_samples_split=int(self.hyperparameters['min_samples_split']))

        self.model = clf.fit(self.x_train, self.y_train)
        self.save_model()

    def predict(self, data):
        self.y_pred = self.model.predict(data)
        return self.y_pred

    def save_model(self):
        with open(f"model-{self.model_version}.pkl", "wb") as file:
            pickle.dump(self.model, file)

    def print_model_metrics(self):

        # calculate the confusion matrix
        conf_matrix = confusion_matrix(self.y_test, self.y_pred)
        logging.info('Confusion Matrix:', conf_matrix)

        # calculate the classification report
        class_report = classification_report(self.y_test, self.y_pred)
        logging.info('Classification Report:', class_report)

        # calculate roc auc score
        roc_auc = roc_auc_score(self.y_test, self.y_pred)
        logging.info('AUC-ROC:', roc_auc)

        # calculate model accuracy
        logging.info("Accuracy:", accuracy_score(self.y_test, self.y_pred))
