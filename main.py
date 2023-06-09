import asyncio
import json

import discord
from discord.ext import commands

import requests

import config
from DatabaseHelper import DatabaseHelper
from config import API_KEY, BOT_TOKEN

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)
helper = DatabaseHelper(config.SERVER_HOST, config.SERVER_USER, config.SERVER_PASS, config.SERVER_DB)
helper.connect()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.command()
async def weather(ctx):
    results = helper.execute_query("SELECT * FROM user_locations WHERE username = %s", (ctx.author.name,))

    if results is None:
        await ctx.author.send("I haven't saved your location yet, would you like to add it into my DB")
    else:
        await send_message(ctx, return_weather(ctx, results))



def return_weather(ctx, results):
    location = results[2];
    json_data = process_request(location)
    location_name = json_data["location"]["name"]
    current_temp = json_data["current"]["temp_f"]
    current_condition_text = json_data["current"]["condition"]["text"]
    return "It is currently" + " " + str(current_temp) + " " + "and " + current_condition_text + " " + "in " + location_name


async def send_message(ctx, message):
    await ctx.author.send(message)

def process_request(param):


    response = requests.get('http://api.weatherapi.com/v1/current.json?key=' + API_KEY + '&q=' + str(param) + '&aqi=no')

    if response.status_code == 200:
        return response.json()
    else:
        print("Response failed with status code: ", response.status_code)






bot.run(BOT_TOKEN);

