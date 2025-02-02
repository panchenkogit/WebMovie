import pickle


def load_model():
    with open("ml_model/svd_model.pkl", "rb") as f:
        return pickle.load(f)