import json
import requests
headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'CSRF-Token': 'jLGe5zdg-qA0EeQOVGpxU2H35E4KkuEAz5Ew',
        }   

#form_data = {"first-name":"Sujith", "last-name":"Manickam", "mail-id":"sujithmanick@outlook.com", "password": "hjfdtzFHCGFCvnnbhjv@546fghg", "phone-number":"+918695020555" , "gender":"Male", "age":23}
form_data = {"mail-id":"sujithmanick@outlook.com", "password": "hjfdtzFHCGFCvnnbhjv@546fghg"}
req = requests.post('http://127.0.0.1:5000/login', headers=headers, json=form_data)
print(req.content)