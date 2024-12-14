import numpy as np

class NaiveBayes:
    def __init__(self):
        self.prior = {}
        self.mean_std_dev = {}
        self.classes = []

    def fit(self, X, y):
        self.classes = np.unique(y)
        total_docs = len(y)

        for cls in self.classes:
            cls_docs = y[y == cls].shape[0]
            self.prior[cls] = cls_docs / total_docs

            cls_index = (y == cls)
            cls_mean = X[cls_index].mean(axis=0)
            cls_std_dev = X[cls_index].std(axis=0)
            cls_std_dev = np.where(cls_std_dev == 0, 1e-6, cls_std_dev)
            self.mean_std_dev[cls] = [cls_mean, cls_std_dev]

    def predict(self, X):
        predictions = []
        for doc in X:
            class_probs = {}
            for cls in self.classes:
                mean, std_dev = self.mean_std_dev[cls]
                log_prob = np.log(self.prior[cls])

                for i in range(len(doc)):
                    mu_ik = mean[i]
                    sigma_ik = std_dev[i]
                    log_coefficient = -np.log(sigma_ik * np.sqrt(2 * np.pi))
                    log_exponent = -((doc[i] - mu_ik) ** 2) / (2 * (sigma_ik ** 2))
                    log_gaussian_prob = log_coefficient + log_exponent
                    log_prob += log_gaussian_prob

                class_probs[cls] = log_prob

            predicted_class = max(class_probs, key=class_probs.get)
            predictions.append(predicted_class)
        return predictions
