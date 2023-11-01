import json
import requests
import time

with open("neonone_api_key.txt", "r") as f:
    api_key = f.read().strip()


test_class = {
  "id": str(int(time.time())),
  "name": "test class",
  "summary": "a test class",
  "maximumAttendees": 0,
  "publishEvent": False,
  "enableEventRegistrationForm": False,
  "archived": True,
  "eventDescription": "a test class description",
  "eventDates": {
    "startDate": "2023-10-25",
    "endDate": "2023-10-25",
    #"startTime": "23:50",
    #"endTime": "23:50",
    "registrationOpenDate": "2023-10-23",
    "registrationCloseDate": "2023-10-24",
    "timeZone": {
      "id": "1",
      "name": "(GMT-04:00) Eastern Time - New York",
      "status": "ACTIVE"
    }
  },
  "financialSettings": {
    "feeType": "Free",
  },
}

baseUrl = "https://api.neoncrm.com/v2"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic ' + api_key,
}
resp = requests.post(baseUrl + '/events', headers=headers, data=json.dumps(test_class))

print(resp.status_code)
print(resp.content)
