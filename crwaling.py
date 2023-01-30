import discord
import time
from discord.ext import commands
from discord.ext import tasks
from selenium import webdriver
from selenium.webdriver.common.by import By

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
    await refresh.start()
 
@bot.event
async def on_message(message):
    if message.content == "안녕?":
        await message.channel.send('안녕!')
 
@tasks.loop(seconds=30)
async def refresh():
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent={0}'.format(user_agent))

    driver = webdriver.Chrome('/Users/genetory/Documents/Discord/chromedriver', options=options)
    driver.get('https://coinmarketcap.com/currencies/link/')
    time.sleep(5)

    priceValue = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/span').text
    change24 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/span').text
    icon = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/span/span').get_attribute('class')

    plusMinus = "+"
    if 'down' in icon:
        plusMinus = "-"
        
    upDown = "상승"
    if plusMinus == "-":
        upDown = "하락"

    # channel = bot.get_channel(int(1068426877485727767))
    # await channel.send("리프레시 완료!\n현재 시세 {}, 변동폭 {} 입니다.".format(priceValue, plusMinus + change24 + " " + upDown))

    # await bot.user.edit(username="LINK Price Bot")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("{} | {} (24h) {}".format(priceValue, plusMinus + change24, upDown)))
    
    driver.quit()
    
bot.run('Token-Key')
