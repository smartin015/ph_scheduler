# - Neon API Specification: https://developer.neoncrm.com/api-v2/#/
import requests
import json
import time

with open("neonone_api_key.txt", "r") as f:
    api_key = f.read().strip()

def postPaginatedData(endpoint, dataKey, headers, data):
  allData = []
  currentPage = 0
  totalPages = 1
  while currentPage < totalPages:
    resp = requests.post(baseUrl + endpoint, headers=headers, data=json.dumps(data))
    respData = resp.json()
    print(respData)

    if len(respData) == 1 and respData[0]["code"] is not None:
        raise Exception(respData)

    if respData["pagination"] != "":
        totalPages = int(respData["pagination"]["totalPages"]) or 1
    

    if respData[dataKey] != "":
        newData = respData[dataKey]
        allData.append(newData)
    
    currentPage += 1
    # Update the currentPage in the body of POST requests
    data["pagination"]["currentPage"] = currentPage

    if currentPage < totalPages:
        time.sleep(1.1) # Prevent throttling

  return allData

baseUrl = "https://api.neoncrm.com/v2"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic ' + api_key,
}

from datetime import datetime
from dateutil.relativedelta import relativedelta
three_yrs_ago = (datetime.now() - relativedelta(years=3)).isoformat().split('T')[0]

body = {
          'searchFields': [
               {
                   'field': 'Event Start Date',
                   'operator': 'GREATER_THAN',
                   'value': three_yrs_ago,
               }
          ],
          'outputFields': [
              'Event ID',
              'Event Name',
              'Event Summary',
              'Event Start Date',
              'Event Start Time',
              'Event End Date',
              'Event End Time',
              'Event Capacity',
              'Event Archive',
              'Event Registration Attendee Count',
              'Campaign Start Date',
              'Campaign End Date'
          ],
          'pagination': {
              'currentPage': 0,
              'pageSize': 200
          }
      }

# Fetch event data and create a dict keyed by event ID
# Exclude "archived" events that aren't actively shown.
eventData = postPaginatedData("/events/search", "searchResults", headers, body)
print(eventData)

dedupedNamesAndDescriptions = {}
for e in eventData[0]:
    dedupedNamesAndDescriptions[e["Event Name"]] = {
        "description": e["Event Summary"],
        "to_schedule": 0,
    }
with open("existing_classes.json", "w") as f:
    json.dump(dedupedNamesAndDescriptions, f, indent=4)
