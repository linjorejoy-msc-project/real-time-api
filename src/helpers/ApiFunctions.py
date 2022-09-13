import requests
import time

param = {"timestart": int(time.time())}


while True:
    time.sleep(0.8)

    response = requests.get("http://127.0.0.1:7777/real/", params=param)

    print(response.json())
