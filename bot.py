import discord
from discord.ext import commands
import requests
import json
import  random

client=commands.Bot(command_prefix=">")
client.remove_command('help')


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))
    print("I am online")

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


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
    embed.add_field(name='>tictactoe <mention1> <mention2>', value='Start a tic tac toe game with 2 people', inline=False)
    embed.add_field(name='>place <number>', value='Place a piece at our turn', inline=False)

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