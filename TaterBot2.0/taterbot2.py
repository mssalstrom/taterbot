import discord
import requests
from dotenv import load_dotenv
import os
from discord.ext import commands

client = discord.Client()
bot = discord.ext.commands.Bot(command_prefix="!")
# API KEYS
load_dotenv('.env')

big_list = ['beef', 'apple', 'pork', 'chicken', 'apple', 'sugar', 'vegan', 'dessert', 'vegetarian', 'shrimp', 'asian']

def run_bot():
    client.run(os.getenv('BOT_TOKEN'))


def get_tater():
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
    return response.json()


def get_fish():
    payload = {
        'limitLicense': True,
        'tags': 'fish',
        'number': 1,
        'apiKey': os.getenv('API_KEY')
    }
    endpoint = "https://api.spoonacular.com/recipes/random"
    response = requests.get(endpoint, params=payload)
    return response.json()


def get_tested(test_list):
    tags = set.intersection(set(test_list), set(big_list))
    print(tags)
    return tags


def get_tag(tags):
    payload = {
        'limitLicense': True,
        'tags': tags,
        'number': 1,
        'apiKey': os.getenv('API_KEY')
    }
    endpoint = "https://api.spoonacular.com/recipes/random"
    response = requests.get(endpoint, params=payload)

    print('tag in get_tag func:', tags)
    print('response tags test url: ', response.url)
    return response.json()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    test_list = []
    tags = []
    test_message = message.content
    test_list = test_message.split()
    print(test_list)
    get_tested(test_list)
    if 'all !tags' in message.content:
        embed_var = discord.Embed(title='A list of all tags I can search for', description=big_list, color=0x00ff00)
        await message.channel.send(embed=embed_var)

    if 'tater' in message.content:
        data = get_tater()
        # Will only get the first recipe that is returned in the response
        data = data.get("recipes")[0]
        url = data.get("spoonacularSourceUrl")
        title = data.get("title")
        summary = data.get("summary")
        # Below removes any html tags from the summary and shortens the description length
        new_sum = summary.replace("<b>", " ").replace("</b>", "")
        if len(new_sum) > 500:
            new_sum = new_sum[:400] + '...'
        image = data.get("image")
        # embedding information from our dict
        embed_var = discord.Embed(title=title, description=new_sum, color=0x00ff00)
        embed_var.set_image(url=image)
        embed_var.add_field(name="FOR THE TATER LOVER IN US ALL: ", value=url, inline=True)
        await message.channel.send(embed=embed_var)

    if 'fish' in message.content:
        data = get_fish()
        data = data.get("recipes")[0]
        url = data.get("spoonacularSourceUrl")
        title = data.get("title")
        summary = data.get("summary")
        new_sum = summary.replace("<b>", " ").replace("</b>", "")
        if len(new_sum) > 500:
            new_sum = new_sum[:400] + '...'
        image = data.get("image")
        embed_var = discord.Embed(title=title, description=new_sum, color=0x00ff00)
        embed_var.set_image(url=image)
        embed_var.add_field(name="FISHY FISH FISH FISH: ", value=url, inline=True)
        await message.channel.send(embed=embed_var)

    if 'tag' in message.content:
        data = get_tag(get_tested(test_list))
        data = data.get("recipes")[0]
        url = data.get("spoonacularSourceUrl")
        title = data.get("title")
        summary = data.get("summary")
        new_sum = summary.replace("<b>", " ").replace("</b>", "")
        if len(new_sum) > 500:
            new_sum = new_sum[:400] + '...'
        image = data.get("image")
        embed_var = discord.Embed(title=title, description=new_sum, color=0x00ff00)
        embed_var.set_image(url=image)
        embed_var.add_field(name="TESTING A TAGGING LIST: ", value=url, inline=True)
        await message.channel.send(embed=embed_var)
    return test_list
run_bot()
