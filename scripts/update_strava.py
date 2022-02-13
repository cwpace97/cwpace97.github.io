import requests
import pandas as pd
from pandas import json_normalize
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#strava vars and tokens
client_id = os.environ.get('strava_clientid')
client_secret = os.environ.get('strava_clientsecret')
refresh_token = os.environ.get('strava_refreshtoken')
access_token = os.environ.get('strava_accesstoken')
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

header = {
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token,
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=header, verify=False)
access_token = res.json()['access_token']
header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
df = requests.get(activites_url, headers=header, params=param).json()

activities = json_normalize(df)

#Break date into start time and date
activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
activities['start_time'] = activities['start_date_local'].dt.time
activities['start_date_local'] = activities['start_date_local'].dt.date

#convert meters to ft
activities['distance'] = activities['distance']*0.000621371
activities['average_speed'] = activities['average_speed']*2.237
activities['max_speed'] = activities['max_speed']*2.237
activities['pace'] = (activities['moving_time']/60)/activities['distance']

print("Last activity logged: ",activities.loc(0)[0]['start_date_local'],"at",activities.loc(0)[0]['start_time'])

activities.to_csv(r"C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\data\strava_activities.csv")