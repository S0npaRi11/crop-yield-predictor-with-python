import pickle

# constants
PATH = './models/'


def predict(data, model):
    # loaded_model = pickle.load(open(PATH + model + '.sav', 'rb'))
    loaded_model = pickle.load(open('./stacking_model.sav', 'rb'))
    # print(loaded_model)

    return loaded_model.predict(data)[0]
