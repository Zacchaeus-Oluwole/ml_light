# Import required libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = pd.read_csv('hospital_lighting_dataset.csv')
data.reset_index(drop=True).head(10)

data = data[['light_level', 'occupancy', 'desired_light_level']]

# Split the dataset into input features and target variable
X = data[['light_level', 'occupancy']]
y = data['desired_light_level']


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train,y_train)

from sklearn.metrics import accuracy_score, f1_score , mean_squared_error, r2_score

prediction= model.predict(X_test)

# Serial communication for data transmission
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)
ser.reset_input_buffer()

def SendCommand(result):
    # Send the result back as an integer
    ser.write(str(result).encode())
    ser.write(b'\n')  # Add a newline character to indicate the end of the message

def ReceiveCommand():
    data = ""
    while data == "":
        try:
            data = ser.readline().decode().strip()
            # print("Got this :", data)
        except:
            print("Error getting response from arduino, wasted much time \n")

    return data

def rev(num):
    v = 1.0 - num
    return v

def output(occupancy, lp, result):
    l = "Occupancy Detected: " + str(occupancy) + " Light Intensity: "+ str(lp)+ "% LED1: " + str(result) + "V LED2: 5V"
    print(l)
    with open('result.txt', 'a') as fp:
        fp.write("%s\n" % l)
    
l_l = 0
while True:

    recvdata = ReceiveCommand()

    l_l = recvdata.split(",")[0]
    
    if len(l_l) > 4:
        l_l = recvdata[0:4]
        occ = recvdata[-1]
    else:
        try:
            occ = recvdata.split(",")[1]
        except:
            occ = "0"

    if len(l_l) < 1:
        light_level = float(0)
    else:
        try:
            light_level = float(l_l)
        except:
            light_level = float(0)

    if len(occ) < 1:
        occupancy = 0
    else:
        try:
            occupancy = int(occ)
        except:
            occupancy = 0

    # Make predictions on new data [light_level, occupancy ]

    new_data = np.array([[occupancy, rev(light_level) ]])
    predictions = model.predict(new_data)

    # Control the lights based on the predictions
    if str(predictions) < str([0.635670678]):
        result = 0
        SendCommand(result)
        output(occupancy, light_level, result)
    elif (str(predictions) >= str([0.635670678])) and str(predictions) < str([0.637836886]):
        result = 1
        SendCommand(result)
        output(occupancy, light_level, result)
    elif (str(predictions) >= str([0.637836886])) and str(predictions) < str([0.640003094]):
        result = 2
        SendCommand(result)
        output(occupancy, light_level, result)
    elif (str(predictions) >= str([0.640003094])) and str(predictions) < str([0.642169302]):
        result = 3
        SendCommand(result)
        output(occupancy, light_level, result)
    elif (str(predictions) >= str([0.642169302])) and str(predictions) < str([0.64433551]):
        result = 4
        SendCommand(result)
        output(occupancy, light_level, result)
    elif (str(predictions) >= str([0.64433551])) and str(predictions):
        result = 5
        SendCommand(result)
        output(occupancy, light_level, result)
    else:
        result = 5
        SendCommand(result)
        output(occupancy, light_level, result)