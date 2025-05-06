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
    print(speed)
    fan_speed = speed
    error = send_data_to_esp()
    return error

def toggle_fan_status():
    global fan_on
    fan_on = not(fan_on)
    error = send_data_to_esp()
    return [fan_on,error]


def send_data_to_esp():
    global fan_on,fan_speed
    if (ip_address!=""):
        try:
            url = f"http://{ip_address}/fan-speed"
            payload = {"fan_on": fan_on,"fan_speed": fan_speed}
            response = requests.post(url, json=payload, timeout=3)
            print(f"Status Code: {response.status_code}")
            print("Response:", response.text)
            return 0
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            return 1
    else:
        print("Error: Device IP Not Found")
        return -1