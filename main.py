import json

import discord
from discord.ext import commands

import requests

from config import API_KEY, BOT_TOKEN

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.event
async def on_message(message):
        if message.content.startswith("!weather"):

            if "," in message.content:
                param = message.content.split(" ")
                json_data = process_request(param[1])
            else:
                param = message.content.split(" ")
                json_data = process_request(param[1])

            location_name = json_data["location"]["name"]
            current_temp = json_data["current"]["temp_f"]
            current_condition_text = json_data["current"]["condition"]["text"]

            await message.channel.send("It is currently" + " " + str(current_temp) + " " + "and " + current_condition_text + " " + "in " + location_name)

def process_request(param):
    response = requests.get('http://api.weatherapi.com/v1/current.json?key=' + API_KEY + '&q=' + str(param) + '&aqi=no')

    if response.status_code == 200:
        return response.json()
    else:
        print("Response failed with status code: ", response.status_code)






bot.run(BOT_TOKEN);

