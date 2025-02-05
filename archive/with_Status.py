import serial
import pandas as pd
import serial.tools.list_ports
import time
import threading
from flask import Flask, render_template, jsonify,  send_from_directory

# Flask app
app = Flask(__name__)

# arduino setup
try:
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
except serial.SerialException as e:
    print(f"Error initializing Arduino: {e}")
    arduino = None
except PermissionError as e:
    print(f"Permission error: {e}. Ensure the port is not in use.")
    arduino = None

# arduino status variables
""" arduino_status = {"status": "connected" if arduino else "disconnected"}
current_status=""
status_lock = threading.Lock()
print([p.device for p in serial.tools.list_ports.comports()])
 """
#DHT sensor variables
temps = []
humids = []
counter = 0

#for the temp
temperature = {"temperature":"0"}# initial value
temperature_lock = threading.Lock()#idk
new_temp = "0"
"""this is a comment"""



#==================================ARDUINO status==================================#
# Function to monitor Arduino connection status
# Ensure thread-safe access
""" def check_presence(correct_port, interval=0.1):
    global arduino_status
    global current_status
    while True:
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        with status_lock:
            if not any(correct_port in port for port in myports):
                current_status = "disconnected"
                arduino_status["status"] = "disconnected"
            else:
                arduino_status["status"] = "connected"
                current_status="connected"
        time.sleep(interval)

 """

# Start monitoring the Arduino connection status
""" while arduino:
    port_controller = threading.Thread(
        target=check_presence, args=("COM3", 0.1), daemon=True)
    port_controller.start() """

@app.route('/')
def home():
    return render_template("index.html", ntemp=temperature["temperature"])


""" 
@app.route('/status')
def status():
    with status_lock:
        return jsonify({"status": current_status})
 """




@app.route('/data')
def data():
    return send_from_directory('.', 'temp_humid.csv')



# Data collection function
def collect_data():
    global counter, temps, humids, new_temp
    while True:
        try:
            if arduino and arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').rstrip()
                if line.startswith("Temperature = "):
                    temp = float(line.split(" = ")[1])
                    temps.append(temp)
                    new_temp = temp
                    """ try:
                        with temperature_lock:
                            temperature["temperature"] = str(temp)
                    except:
                        print(e) """
                if line.startswith("Humidity = "):
                    humid = float(line.split(" = ")[1])
                    humids.append(humid)

                # Save data every 10 iterations
                if counter % 10 == 0:
                    min_length = min(len(temps), len(humids))
                    temps = temps[:min_length]
                
                    
                    humids = humids[:min_length]
                    
                    df = pd.DataFrame({'Temperature': temps, 'Humidity': humids})
                    df_temp = pd.DataFrame({'Temperature': [str(new_temp)]})  # Wrap in a list
                    df_temp.to_csv('temps.csv', index=False)
                    df.to_csv('temp_humid.csv', index=False)

                counter += 1
        except Exception as e:
            print(f"Error in data collection: {e}")
        time.sleep(1)

@app.route('/ntemperature')
def ntemperature():
    df = pd.read_csv('temps.csv')
    latest_temp = df['Temperature'].iloc[-1]  # Get the most recent value
    return jsonify({'temperature': latest_temp})
# Start data collection thread
if arduino:
    data_thread = threading.Thread(target=collect_data, daemon=True)
    data_thread.start()
else:
    print("Arduino not initialized. Please check the COM port.")

if __name__ == '__main__':
    # Start Flask app
    app.run(debug=True)
