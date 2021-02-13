import discord
from discord.ext import commands
import requests
import json

client=commands.Bot(command_prefix=">")
client.remove_command('help')

def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    loaded = json.loads(response.text)
    quote = loaded[0]["q"] + ' -'+ loaded[0]['a']
    return quote

def getInsult(name):
    url = "https://insult.mattbas.org/api/insult.txt?who="+name
    response = requests.get(url)
    print(response.text)
    return response.text
    
def getGif(query):
    api_key="7LJ5BDjp5cDaT4HeZ30rJRyAC0Aj1Sz6"
    url = "http://api.giphy.com/v1/gifs/search"
    params ={
        "api_key": api_key,
        "q": query
    }
    response = requests.get(url=url, params=params)
    json_data = json.loads(response.text)
    return json_data["data"][0]["embed_url"]

@client.event
async def on_ready():
    print("I am online")

@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour= discord.Colour.orange()
    )

    embed.set_author(name = "Help")
    embed.add_field(name=">ping", value="Sends ping of the user", inline=False)
    embed.add_field(name=">quote", value="Sends a random motivational quote", inline=False)
    embed.add_field(name=">gif <query>", value="Sends a gif related to query", inline=False)
    embed.add_field(name="insult <name>",  value="Insults with name", inline= False)

    await ctx.send(author, embed=embed)
    
@client.command(name = 'ping', aliases =['p'])
async def ping(ctx):
  await ctx.send(f"Pong! {client.latency}")

@client.command(name = 'quote', aliases = ['q'])
async def sendQuote(ctx):
    quote = getQuote()
    await ctx.send(quote)

@client.command(name = 'gif', aliases = ['g'])
async def sendGif(ctx,  *args):
    if(len(args)!=0):
        query=' '.join(args)
        
        url = getGif(query)
        await ctx.send(url)

@client.command(name = 'insult', aliases = ['i'])
async def sendInsult(ctx, *args):
    if(len(args)!=0):
        name = ' '.join(args)
        insult = getInsult(name)
        await ctx.send(insult)

client.run('ODEwMTQ2MTQwNDg5NjQ2MDgx.YCfZYw.nJi5KshmC9D308saAFNCFrIoHzU')

#link ="https://discord.com/oauth2/authorize?client_id=810146140489646081&scope=bot"