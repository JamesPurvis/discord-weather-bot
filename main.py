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

import asyncio

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if 'yes' in message.content.lower():
        await message.channel.send("What is your location? EXAMPLE: Tupelo or Tupelo, MS")

        def check_location_response(m):
            return m.author == message.author and m.channel == message.channel

        try:
            location_message = await bot.wait_for('message', check=check_location_response, timeout=50)

            location = location_message.content

            helper.execute_query("INSERT INTO user_locations (username, location) VALUES (%s, %s)", (message.author.name, location))
            await message.channel.send("Thanks, I have added you to my database. You may now use !weather to get the current weather for your area.")

        except asyncio.TimeoutError:
            await message.channel.send("No response received. Location request timed out.")




def return_weather(ctx, results):
    location = results[2]
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


bot.run(BOT_TOKEN)

