import subprocess
import re
import requests

ip_address = ""
fan_on = False
fan_speed = 0

def nslookup(host):
    global ip_address
    ip_address = ""
    try:
        # subprocess.run(["ipconfig", "/flushdns"], shell=True)
        subprocess.run(["ipconfig", "/flushdns"], shell=True)
        result = subprocess.run(["nslookup", host], capture_output=True, text=True)
        #print(result.stdout)
        ips = re.findall(r"Address:\s+(\d+\.\d+\.\d+\.\d+)", result.stdout)
        ip_address = ips[1]
        print(ip_address)
    except Exception as e:
        print("Error:", e)
        ip_address = ""
    return ip_address

def setFanSpeed(speed):
    global fan_speed
    fan_speed = speed
    error = send_data_to_esp()
    return error

def toggle_fan_status():
    global fan_on
    fan_on = not(fan_on)
    error = send_data_to_esp()
    return [fan_on,error]


def send_data_to_esp():
    global fan_on,fan_speed,ip_address
    if (ip_address!=""):
        try:
            url = f"http://{ip_address}/fan-speed"
            payload = {"fan_on": fan_on,"fan_speed": fan_speed}
            response = requests.post(url, json=payload, timeout=1)
            print(f"Status Code: {response.status_code}")
            print("Response:", response.text)
            return 0
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            ip_address = ""
            return 1
    else:
        print("Error: Device IP Not Found")
        nslookup("fan-controller")
        return -1
    
def get_meter_values():
    global ip_address
    if ip_address != "":
        try:
            url = f"http://{ip_address}/meters"
            response = requests.get(url, timeout=1)
            response.raise_for_status()  # Raises an error for non-200 codes
            data = response.json()
            # print("Meter values received:", data)
            return data  # Should be a dict or list depending on ESP response
        except requests.exceptions.RequestException as e:
            print("Failed to get meter values:", e)
            ip_address = ""
            return None
    else:
        # print("Error: Device IP Not Found")
        nslookup("fan-controller")
        return None