#!/usr/bin/env python3
#Returns temperature of city in celcius
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import requests
import json

#loading tokens from env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# connecting to slack channel, sends initial message to know connection successful
client.chat_postMessage(channel='#weatherbot', text='Send Message Demo')

# Get Bot ID
BOT_ID = client.api_call("auth.test")['user_id']

@app.route('/')
def hello():
    return 'up'

# handling Message Events
@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text2 = event.get('text')
#api key obtained from open weather
    api_key = "3c8b9ffd3c8e7dddc7e649965eadc30a"
#api call to open weather
    url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=" + text2
#returning data
    response = requests.get(url)
    returning=response.json()
    justtemp = returning["main"]
#grabbing only the current temperature
    current_temperature = justtemp["temp"]
#from kelvin to celcius unit conversion
    new = current_temperature - 273.15

#temperature and text into one string
    a=( "The current temperature in " + text2 + " is " + "{:.2f}".format(new) + " degrees celcius")

#sending temperature string to slack channel
    if BOT_ID !=user_id:
        client.chat_postMessage(channel=channel_id, text=a)


if __name__ == "__main__":
    app.run(debug=True)
