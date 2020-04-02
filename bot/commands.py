import discord
from discord.ext import commands

from bot.learning.bot import pipe, fixpunctuation
import random

client = discord.AutoShardedClient()

@client.event
async def on_ready():
    print('logged in as: ')

path = 'bot\\learning\\data\\user.txt'

serverpath = 'bot\learning\data\server_ids.txt'

dmpath = 'bot\\learning\\data\\dmid.txt'

welcomepath = 'bot\\learning\\data\\welcome_server_ids.txt'

vocapath = 'bot\\songdata\\voca.txt'

@client.event
async def on_message(message):  

    if message.content == '!bangers vocaloid':
        voca = open(vocapath)
        await message.channel.send('` Here you go!:{}`'.format(random.choice(voca.read())))

    if message.content == '!NA join':
        await message.author.send('You can add me to you server with this!')
        await message.author.send('https://discordapp.com/api/oauth2/authorize?client_id=616769437734797323&permissions=0&scope=bot')
        await message.author.send('How To use me in your server')
        await message.author.send('step 1: Create a role called `napi` and assign it to yourself or admins.')
        await message.author.send('step 2: use the command `!channel_add` to whitelist that channel.')
        await message.author.send('step 3: use the prefix `c ` + your message to begin talking to me!')
          
    with open(serverpath,) as f:
        if str(message.channel.id) in f.read():
            if message.content.startswith('c '):
                ModMessage = message.content[2:]
                p_resp, dist = pipe.predict([ModMessage])
                respnse=fixpunctuation(p_resp[0])
                await message.channel.send(respnse)

        if message.content == '!channel_add':
            with open(path) as fa:
                users = open(path)
                if "napi" in [y.name.lower() for y in message.author.roles] or str(message.author.id) in users:
                    with open(serverpath, '+r') as f:
                        if str(message.channel.id) in f.read():
                            await message.channel.send('`this channel has already been added!`')
                        else:
                            f.write(str(message.channel.id))
                            f.write('\n')
                            await message.channel.send('channel added!')
                else:
                    await message.channel.send('You dont have permission for that!, You need the `napi` role!')

client.run('token')