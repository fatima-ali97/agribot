import serial ;
import matplotlib.pyplot as plt ;
import pandas as pd


arduino = serial.Serial(port='COM3', baudrate=9600,timeout=1)

## double check the COM number in ARDUINO ide
## make sure ARDUINO ide is closed

temps = []
humids = []
counter = 0 

plt.ion()
fig, (ax1,ax2) = plt.subplots(2,1)
while True:
    if arduino.in_waiting > 0:
        line=arduino.readline().decode('utf-8').rstrip()
        print(line)

        if line.startswith("Temperature = "):
            temp = float(line.split(" = ")[1])
            temps.append(temp)

        if line.startswith("Humidity = "):
            humid = float(line.split(" = ")[1])
            humids.append(humid)
        ax1.clear()
        ax2.clear()
        ax1.plot(temps,color='g')
        ax2.plot(humids, color='b')
        ax1.set_ylabel('Temperature', color='g')
        ax2.set_ylabel('Humidity', color='b')
        plt.draw()
        plt.pause(0.01)


        if counter % 100 ==0:
            min_length = min(len(temps), len(humids))
            temps = temps[:min_length]
            humids = humids[:min_length]


            df = pd.DataFrame({'Temperature':temps,'Humidity':humids})
            df.to_csv('temp_humid.csv', index=False)
            plt.savefig("temp_humid.png") # save graph

        counter+=1



####### ###########
import serial
import matplotlib.pyplot as plt
import pandas as pd
import plotly
import plotly.express as px
import json
from flask import Flask, jsonify, render_template, send_file, send_from_directory

import serial.tools.list_ports
import time
import threading
# Flask app
app = Flask(__name__)

# Arduino setup
try:
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
except serial.SerialException as e:
    print(f"Error: {e}")
    arduino = None

temps = []
humids = []
counter = 0

arduino_status = {"status": "connected" if arduino else "disconnected"}
# Function to monitor Arduino connection status
def check_presence(correct_port, interval=0.1):
    global arduino_status
    while True:
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        if not any(correct_port in port for port in myports):
            arduino_status["status"] = "disconnected"
        else:
            arduino_status["status"] = "connected"
        time.sleep(interval)

# Start monitoring the Arduino connection status
if arduino:
    port_controller = threading.Thread(
        target=check_presence, args=("COM3", 0.1), daemon=True
    )
    port_controller.start()


@app.route('/')
def home():
    """ ##check if sensors are installed
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    arduino_port = [port for port in myports if 'COM3' in port ][0]
    status ="connected"
    def check_presence(correct_port, interval=0.1):
        while True:
            myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
            if arduino_port not in myports:
              
              status = "disconnected!"
              break
            time.sleep(interval)

    port_controller = threading.Thread(target=check_presence, args=(arduino_port, 0.1))
    port_controller.setDaemon(True)
    port_controller.start() """
    ##humidity sensor
    df = pd.read_csv('temp_humid.csv')
    ##fig1 = px.line(df,y="Humidity", title="Humidity")
    ## convert to json & send it to html then JS will render this JSON
    ##graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

   
   
    return render_template("index.html",status=arduino_status)

@app.route('/graph')
def graph():
    return send_file("temp_humid.png", mimetype='image/png')

""" @app.route('/data',methods=["GET", "POST"])
def data():
    return send_file("temp_humid.csv", mimetype='text/csv')
 """
@app.route('/status')
def status():
    return jsonify(arduino_status)

@app.route('/data')
def data():
    return send_from_directory('.', 'temp_humid.csv')
# Data collection function
def collect_data():
    global counter, temps, humids
    while True:
        if arduino and arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').rstrip()
            ##print(line)

            if line.startswith("Temperature = "):
                temp = float(line.split(" = ")[1])
                temps.append(temp)

            if line.startswith("Humidity = "):
                humid = float(line.split(" = ")[1])
                humids.append(humid)

            # Save plot and data every 100 iterations
            if counter % 5 == 0:
                min_length = min(len(temps), len(humids))
                temps = temps[:min_length]
                humids = humids[:min_length]

                # Save data to CSV
                df = pd.DataFrame({'Temperature': temps, 'Humidity': humids})
                df.to_csv('temp_humid.csv', index=False)

                #if the file size is too big - terminate


            counter += 1

if __name__ == '__main__':
    import threading
    # Start data collection in a thread
    if arduino:
        data_thread = threading.Thread(target=collect_data)
        data_thread.daemon = True
        data_thread.start()
    else:
        print("Arduino not initialized. Please check the COM port.")

    # Start Flask app
    app.run(debug=True)
