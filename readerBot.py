import discord
from discord.ext import commands

client = discord.AutoShardedClient()

@client.event
async def on_ready():
    print("RB ready")

datanewpath = 'bot\\learning\\data\\datanew.txt'
inputpath = 'bot\\learning\\data\\input.txt'

logs = 'bot\\learning\\data\\ReaderBotWrite.txt'

abyss_bot = client.get_user(443586695498170368)
bot = client.get_user(616769437734797323)

@client.event
async def on_message(message):
    if message.author != abyss_bot:
        if not message.author == bot:
            if message.content.startswith(""):
                if message.content.startswith("c "):
                    ModMessage = message.content[2:]

                    inp = open(inputpath, "+r")
                    datanew = open(datanewpath, '+r')

                    if str(ModMessage) in inp.read():
                        print("Already Added! " + ModMessage)
                    else:
                        inp.write(">" + ModMessage)
                        inp.write("\n")

                        print("wrote: ", ModMessage, "from: ", message.author)



                        
token = 'token'
client.run(token)