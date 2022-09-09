import pandas as pd
import requests
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
import tushare as ts
import datetime as dt
td = dt.datetime.today().strftime("%Y/%m/%d")
wd_t=dt.datetime.today().weekday()
td1 = td.replace('/', '')

pro = ts.pro_api('17b3b989ac007724a18a682f9982aeacc42c1ec972c2349eb4ed5ab5')
df= pro.daily(ts_code='000068.SZ', start_date='20180101', end_date=td1)
df1 = df.reset_index()['close']
#Let us plot the Close value graph using pyplot

plt.plot(df['close'])
plt.show()

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))
df1=scaler.fit_transform(numpy.array(df1).reshape(-1,1))

training_size=int(len(df1)*0.65)
test_size=len(df1)-training_size
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]

def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
        return numpy.array(dataX), numpy.array(dataY)
time_step = 100
X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)

X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

print(X_train)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')

train_predict=model.predict(X_train)
test_predict=model.predict(X_test)
train_predict=scaler.inverse_transform(train_predict)
test_predict=scaler.inverse_transform(test_predict)

import math
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(y_train,train_predict))

x_input=test_data[341:].reshape(1,-1)
x_input.shape