import serial
import pandas as pd
import serial.tools.list_ports
import time
import threading
from flask import Flask, render_template, jsonify, send_from_directory
from datetime import datetime
#from flask_navigation import Navigation


# Flask app
app = Flask(__name__)
#nav = Navigation(app)


""" 
# initializing Navigations 
nav.Bar('top', [ 
    nav.Item('Home', 'index'), 
    nav.Item('Team', 'Team',), 
])  """
# Arduino setup
try:
    # Make sure that the COM number matches the board you have !
    arduino = serial.Serial(port='COM8', baudrate=9600, timeout=1)
except serial.SerialException as e:
    print(f"Error initializing Arduino: {e}")
    arduino = None
except PermissionError as e:
    print(f"Permission error: {e}. Ensure the port is not in use.")
    arduino = None

# DHT11 sensor variables
temps = []
humids = []
times=[]
counter = 1

#Plant Moisture Sensor
plantId=1
moistures=[]

# Air Quality Sensor
aqs=[]

# Temperature endpoint storage
temperature = {"temperature": "0"}
new_temp = "0"


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/data')
def data():
    return send_from_directory('.', 'temp_humid.csv')

# Data collection function
def collect_data():
    global counter, temps, humids, new_temp, new_time, moistures,plantId, aqs
    while True:
        try:
            if arduino and arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').rstrip()
                current_time = datetime.now().strftime('%I:%M:%S')  # Get the current time

                if line.startswith("Temperature = "):
                    temp = float(line.split(" = ")[1])
                    temps.append(temp)
                    new_temp = temp
                    new_time = current_time  # Store the current timestamp for the latest temperature

                if line.startswith("Air Quality:"):
                    aq = float(line.split(":")[1])
                    aqs.append(aq)

                if line.startswith("Humidity = "):
                    humid = float(line.split(" = ")[1])
                    humids.append(humid)

                if line.startswith("1Soil = "):
                    moisture = float(line.split(" = ")[1])
                    moistures.append(moisture)
                    plantId= line[0]

                if line.startswith("2Soil = "):
                    moisture = float(line.split(" = ")[1])
                    moistures.append(moisture)
                    plantId= line[0]

                # Save data every 10 iterations
                if counter % 10 == 0 and temps:
                    df_temp = pd.DataFrame({
                        'Time': [new_time],
                        'Temperature': [new_temp]
                    })
                    df_moisture =pd.DataFrame({
                        'ID': plantId,
                        'Moisture' : moistures
                    })
                    df_aq=pd.DataFrame({
                        'aq':aqs
                    })
                    min_length = min(len(temps), len(humids))
                    temps = temps[:min_length]
                    humids = humids[:min_length]


                    df = pd.DataFrame({'Temperature': temps, 'Humidity': humids})
                    df.to_csv('temp_humid.csv', index=False)

                    df_aq.to_csv('aq.csv', index=False)
                    df_temp.to_csv('temps.csv', index=False)
                    df_moisture.to_csv('moisture.csv', index=False)

                counter += 1
        except Exception as e:
            print(f"Error in data collection: {e}")
        time.sleep(1)

# Track temperature
@app.route('/ntemperature')
def ntemperature():
    try:
        df = pd.read_csv('temps.csv')
        latest_time = df['Time'].iloc[-1]
        latest_temp = df['Temperature'].iloc[-1]
        return jsonify({'time': latest_time, 'temperature': latest_temp})
    except Exception as e:
        print(f"Error reading temperature data: {e}")
        return jsonify({'error': 'Unable to fetch temperature data'})
    
@app.route('/moisture')
def moisture():
    df = pd.read_csv('moisture.csv')
    data = df.to_dict(orient='records')
    return jsonify(data)


@app.route('/airQuality')
def airQuality():
    return send_from_directory('.', 'aq.csv')


@app.route('/team') 
def team(): 
    return render_template('team.html') 
  
# Start data collection thread
if arduino:
    data_thread = threading.Thread(target=collect_data, daemon=True)
    data_thread.start()
else:
    print("Arduino not initialized. Please check the COM port.")

if __name__ == '__main__':
    app.run(debug=True)
