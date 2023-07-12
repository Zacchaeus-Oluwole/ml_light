# Import required libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


data = pd.read_csv('hospital_lighting_dataset.csv')
data.reset_index(drop=True).head(10)

data = data[['light_level', 'occupancy', 'desired_light_level']]
data


# Split the dataset into input features and target variable
X = data[['light_level', 'occupancy']]
y = data['desired_light_level']


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model = LogisticRegression()
model = LinearRegression()
# model = RandomForestRegressor(n_estimators=2000)
model.fit(X_train,y_train)

from sklearn.metrics import accuracy_score, f1_score ,mean_squared_error,r2_score

prediction= model.predict(X_test)


# Serial communication for data transmission
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(5) # wait 5 sec
ser.reset_input_buffer()

def SendCommand(result):
    res = bytes(result, 'utf-8')
    ser.write(res)

def ReceiveCommand():
    number = ser.read()
    if number != b'':
        num = str(number, 'utf-8')
        return num
    

while True:

    recvdata = ReceiveCommand()
    print(recvdata.split(" "))

    l_l = recvdata.split(" ")[0]
    occ = recvdata.split(" ")[1]

    light_level = float(l_l)
    occupancy = int(occ)

    # Make predictions on new data [light_level, occupancy ]

    new_data = np.array([[occupancy, light_level ]])
    predictions = model.predict(new_data)

    # Control the lights based on the predictions
    if str(predictions) < str([0.635670678]):
        result = 0
        SendCommand(result)
        print("Light off")
    elif (str(predictions) >= str([0.635670678])) and str(predictions) < str([0.637836886]):
        result = 1
        SendCommand(result)
        print("Light level 1")
    elif (str(predictions) >= str([0.637836886])) and str(predictions) < str([0.640003094]):
        result = 2
        SendCommand(result)
        print("Light level 2")
    elif (str(predictions) >= str([0.640003094])) and str(predictions) < str([0.642169302]):
        result = 3
        SendCommand(result)
        print("Light level 3")
    elif (str(predictions) >= str([0.642169302])) and str(predictions) < str([0.64433551]):
        result = 4
        SendCommand(result)
        print("Light level 4")
    elif (str(predictions) >= str([0.64433551])) and str(predictions):
        result = 5
        SendCommand(result)
        print("Light level 5")
    else:
        result = 5
        SendCommand(result)
