import discord
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
import os
client = discord.Client()
bot = discord.ext.commands.Bot(command_prefix="!")
# API KEYS
load_dotenv('.env')


def run_bot():
    client.run(os.getenv('BOT_TOKEN'))


def get_recipe():
    payload = {
        'limitLicense': True,
        'tags': 'potato',
        'number': 1,
        'apiKey': os.getenv('API_KEY')
    }
    endpoint = "https://api.spoonacular.com/recipes/random"
    response = requests.get(endpoint, params=payload)
    # test response
    print(response.status_code)
    writefile = open('recipe.json', 'w')
    writefile.write(response.text)
    writefile.close()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!TaterMe'):
        get_recipe()
        with open('recipe.json') as json_file:
            data = json.load(json_file)
            url = []
            # This loop is used to create a dict for the info we need
            for i in data:
                for k in data[i]:
                    url = k["spoonacularSourceUrl"]
                    title = k["title"]
                    summary = k["summary"]
                    # Below removes any html tags from the summary and shortens the description length
                    new_sum = summary.replace("<b>", " ")
                    new_sum2 = new_sum.replace("</b>", "")
                    if len(new_sum2) > 500:
                        new_sum2 = new_sum2[:400] + '...'
                    image = k["image"]
        json_file.close()
        # embedding information from our dict
        embed_var = discord.Embed(title=title, description=new_sum2, color=0x00ff00)
        embed_var.set_image(url=image)
        embed_var.add_field(name="FOR THE TATER LOVER IN US ALL: ", value=url, inline=True)
        await message.channel.send(embed=embed_var)

run_bot()


