
from sklearn import preprocessing, svm
import pandas as pd
import numpy as np
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout
from sklearn.preprocessing import MultiLabelBinarizer ,LabelEncoder
import sklearn.datasets as skds
from pathlib import Path
from scipy.io import  arff
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.model_selection import  train_test_split
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping
import keras
from time import time
        
class TimingCallback(keras.callbacks.Callback):
  def __init__(self):
    self.logs=[]
  def on_epoch_begin(self, epoch, logs={}):
    self.starttime=time()
  def on_epoch_end(self, epoch, logs={}):
    self.logs.append(time()-self.starttime)
    
    
seed = 7
np.random.seed(seed)

data = arff.loadarff('POSIT.arff')
dt = pd.DataFrame(data[0])

dt_label_class = dt['classification'].astype(float)
#dt.iloc[:,0].astype(float)

dt_features = dt.iloc[:,1:28].apply(np.ceil)
#print(dt['CLASS'])
train_x,test_x ,train_y,test_y =  train_test_split(dt_features ,dt_label_class, test_size= 0.3 , random_state= 1, stratify= dt_label_class) #

scaler = StandardScaler()

scaler.fit(train_x)
X_train = scaler.transform(train_x)
X_test = scaler.transform(test_x)

num_labels = 3
vocab_size = 27
# define baseline model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(512, input_shape=(vocab_size,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    model.add(Dense(512))   
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    model.add(Dense(num_labels))
    model.add(Activation('softmax'))
    model.summary()
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


# Fit the model
estimator = KerasClassifier(build_fn=baseline_model, nb_epoch=10, batch_size=10, verbose=0)


#kfold = KFold(n_splits=5, shuffle=True, random_state=seed)

#results = cross_val_score(estimator, X_train, train_y, cv=kfold)
#print("\nOverall Validation accuracy: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))

# build the neural network from all the training set
#history = estimator.fit(X_train, train_y)
cb = TimingCallback()
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=50)

history = estimator.fit(X_train, train_y,validation_split=0.33,epochs=10,verbose=0,callbacks=[cb, es])

predictions = estimator.predict(X_test)
print("Training Time For each Epoch")
print(cb.logs)
print("=======================================================================")
# list all data in history


plt.plot(history.history['acc'])
plt.plot(cb.logs)
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('time')
plt.legend(['accuracy', 'time'], loc='upper left')
plt.show()



# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# build the confusion matrix after classifing the test data


print("Overall Accuracy", accuracy_score(test_y, predictions) * 100)
print(classification_report(test_y,predictions))

cm = confusion_matrix(test_y, predictions)
print("\nThe confusion matrix when apply the test set on the trained nerual network:\n", cm)