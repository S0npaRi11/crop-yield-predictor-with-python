import pickle

# constants
PATH = './models/'


def predict(data, model):
    loaded_model = pickle.load(open(PATH + model + '.sav', 'rb'))

    return loaded_model.predict(data)[0]
