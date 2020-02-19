import requests

payload = {
    "Name": "A1",
    "Data": True

}
r = requests.post("http://192.168.137.142:1880/LEDin", data=payload)