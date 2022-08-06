import pandas as pd
import numpy as np

from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences


# loading dataframe
def detect_defacement():
    data = pd.read_csv('data.csv')

    # converting text column to string
    data['0'] = data['0'].astype(str)
    # choosing only required column
    X_train = data['0']

    model = load_model('my_model.h5')

    ## some config values
    embed_size = 100  # how big is each wordvector
    max_feature = 50000  # how many unique words to use (i.e num rows in embedding vector)
    max_len = 2000  # max number of words in a question to use

    from keras.preprocessing.text import Tokenizer
    tokenizer = Tokenizer(num_words=max_feature)

    tokenizer.fit_on_texts(X_train)

    x_train_features = np.array(tokenizer.texts_to_sequences(X_train))
    # x_test_features = np.array(tokenizer.texts_to_sequences(x_test))

    len(x_train_features[0])

    x_train_features = pad_sequences(x_train_features, maxlen=max_len)
    # x_test_features = pad_sequences(x_test_features,maxlen=max_len)

    x_train_features = pad_sequences(x_train_features)
    # x_test_features = pad_sequences(x_test_features,maxlen=max_len)

    y_predict = [1 if o > 0.5 else 0 for o in model.predict(x_train_features)]

    for i in range(len(y_predict)):
        if y_predict[i] == 0:
            return True
        else:
            return False


print(detect_defacement())
