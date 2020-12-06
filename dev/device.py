import requests
import time

serverUrl="http://127.0.0.1:5000/"


def cold(settings: dict):
    requests.post( serverUrl + "cold", json=settings)

def hot(settings: dict):
    requests.post( serverUrl + "hot", json=settings)

def stop():
    requests.post( serverUrl + "stop_device")

def readTemperature():
    return float(requests.get("http://127.0.0.1:5000/read_temperature").json()["temperature"])

def status():
    return requests.get(serverUrl).json()["status_codes"]["status"]


if __name__ == "__main__":

    t_reference = 15

    cold({"objective_temperature": t_reference})
    while status() != 3:
        print( readTemperature())
        time.sleep(1)