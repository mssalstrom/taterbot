import discord
import requests
from discord.ext import commands
import codecs
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import json


client = discord.Client()
bot = discord.ext.commands.Bot(command_prefix="!")
# API KEYS
load_dotenv('.env')

big_list = ['beef', 'apple', 'pork', 'chicken', 'apple', 'sugar', 'vegan', 'dessert', 'vegetarian', 'shrimp', 'asian',
            'breakfast', 'dinner', 'eggs', 'bacon', 'cheese', 'soup', 'salad', 'broccoli', 'peppers', 'stuffed'
            'italian', 'bbq', 'ice cream']



def run_bot():
    client.run(os.getenv('BOT_TOKEN'))

def request_check():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://spoonacular.com/food-api/console#")
    # driver.minimize_window()
    driver.implicitly_wait(0.8)
    already_have_acn = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/p[1]/a")
    already_have_acn.click()
    usr_login = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/input[1]")
    usr_pw = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/input[2]")
    usr_login.send_keys(os.getenv('user_name'))
    usr_pw.send_keys(os.getenv('pw'))
    login_click = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/button")
    login_click.click()


def new_request_page():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://api.spoonacular.com/spoonacular-api/callStats?apiKey=b015b2c2c8eb4ddcbd0f86bbe946eb27")
    file_save = os.path.join("C:\\Users\\salst\\Desktop\\TaterBot2.0", "PageSave.html")
    f = codecs.open(file_save, "w", "utf-8")
    h = driver.page_source
    f.write(h)


def get_request_amount():
    with open('PageSave.html') as fp:
        soup = BeautifulSoup(fp, 'lxml')
    d = json.loads(soup.find("pre").string)
    new_list = d[6]
    request_total = new_list["requests"]
    print(request_total)
    return request_total


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
    # This function takes the users input and find the intersection between our allowed tags and converts that to a
    # a string separated by commas to be used in the url.
    tags = set.intersection(set(test_list), set(big_list))
    tag_string = ",".join(tags)
    return tag_string


def get_tag(tag_string):
    payload = {
        'limitLicense': True,
        'tags': tag_string,
        'number': 1,
        'apiKey': os.getenv('API_KEY')
    }
    endpoint = "https://api.spoonacular.com/recipes/random"
    response = requests.get(endpoint, params=payload)
    print('response tags test url: ', response.url)
    return response.json()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if 'options' in message.content:
        embed_var = discord.Embed(title='A list of all tags I can currently search for', description=big_list, color=0x00ff00)
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
        test_list = []
        tag_obj = get_tested(test_list)
        print('TAG OBS', tag_obj)
        test_message = message.content
        test_list = test_message.split()
        get_tested(test_list)
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
        embed_var.add_field(name=f'Your tags for {tag_obj} have led me to this...', value=url, inline=True)
        await message.channel.send(embed=embed_var)
        return test_list
    if '!cap' in message.content:
        new_request_page()
        cap = get_request_amount()
        await message.channel.send(f'We have made {int(cap)}/150 requests {message.author}!')
    if 'good bot' in message.content:
        await message.channel.send(f'Thanks {message.author}!')
        await bot.process_commands(message)
run_bot()

