import discord
import asyncio
import random
from discord.ext import commands
from discord import Embed, Emoji
from itertools import cycle

#⊱⋅─────────────────────── [ VARIABLES ] ─────────────────────────⋅⊰#

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '!', intents = intents)
bot.remove_command('help') # Remove the default discord help command (post note: I don't know if it's still needed)

bot_version = '1.0'
bot_status = 'Tetris'
bot_token = ''

default_word_filter = ['bad word']

#⊱⋅──────────────────────── [ STARTUP ] ─────────────────────────⋅⊰#

# Startup - what happens when the bot starts up
@bot.event  
async def on_ready():

    print('⊱⋅─────────────────⋅⊰')
    print('Bot initialized')
    print(f'Version {bot_version}')
    print('⊱⋅─────────────────⋅⊰')
    
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.playing, name = bot_status))

#⊱⋅───────────────────────── [ EVENT ] ──────────────────────────⋅⊰#

# Reads messages and detects key words
@bot.event
async def on_message(message):
    for word in default_word_filter: # Checks for any words in the default filtered words list
        if word in message.content:
            await message.delete()
    
    await bot.process_commands(message) # Proceeds with the rest of the script

#⊱⋅──────────────────────── [ SYSTEM ] ──────────────────────────⋅⊰#

# Help - shows the list of available commands
@bot.group(invoke_without_command = True)
async def help(ctx):
    embed = discord.Embed(title = 'Help', description = 'Use !help <command> to get the details about a command', color = 0x2f3136)
    embed.add_field(name = '__System__', value = 'ping, info', inline = False)
    embed.add_field(name = '__Fun__', value = 'roll, 8ball, coinflip, shoot', inline = True)
    embed.add_field(name = '__Math__', value = 'sum, sub, mul, div', inline = False)

    await ctx.send(embed=embed)
    await asyncio.sleep(3)

# Admin help - shows the list of available admin commands
@bot.group()
@commands.has_permissions(manage_messages = True)
async def adminhelp(ctx):
    embed = discord.Embed(title = 'Admin help', description = 'Use !help <command> to get the details about a command', color = 0x2f3136)
    embed.add_field(name = '__Message__', value = 'say, dm', inline = False)
    embed.add_field(name = '__Manage__', value = 'clean, nuke, lock', inline = True)
    embed.add_field(name = '__System__', value = 'kick, ban', inline = False)

    await ctx.send(embed=embed)
    await asyncio.sleep(3)

# Info - shows information about a certain user
@bot.command(aliases = ['whois'])
async def info(ctx, *, member: discord.Member):
    await ctx.channel.purge(limit = 1)

    embed = discord.Embed(title = f'Profile of {member.name}', description = member.display_name, color = 0x2f3136)
    embed.add_field(name = 'ID', value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Invoked by {ctx.author.name}')

    await ctx.send(embed = embed)
    await asyncio.sleep(3)

# Ping - shows the ping of the user using the command
@bot.command()
async def ping(ctx):
    await ctx.channel.purge(limit = 1)

    embed = discord.Embed(color=0xffc300)
    embed.add_field(name = '__Pong__', value=':hourglass: ' + f'{round(bot.latency * 1000)}ms', inline = False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Invoked by {ctx.author.name}')

    await ctx.send(embed=embed)
    await asyncio.sleep(3)

#⊱⋅───────────────────────── [ HELP ] ──────────────────────────⋅⊰#

@help.command()
async def info(ctx):
    embed = discord.Embed(title = '__Info__', description = 'Returns informations about a specific user', color = 0x666699)
    embed.add_field(name = '**Syntax**', value = '.info @<member>')

    await ctx.send(embed=embed)
@help.command()
async def ping(ctx):
    embed = discord.Embed(title = '__Ping__', description = 'Returns the ping of the bot', color = 0x666699)
    embed.add_field(name = '**Syntax**', value = '.ping')

    await ctx.send(embed=embed)
@help.command(aliases = ['whois'])
async def roll(ctx):
    embed = discord.Embed(title = '__Roll__', description = 'Returns a number between 1 and 100', color = 0x666699)
    embed.add_field(name = '**Syntax**', value = '.roll')

    await ctx.send(embed=embed)
@help.command(aliases = ['8ball'])
async def eightball(ctx):
    embed = discord.Embed(title = '__Eight ball__', description = 'Returns a random positive or negative answer', color = 0x2f3136)
    embed.add_field(name = '**Syntax**', value = '.8ball <question>')

    await ctx.send(embed=embed)
@help.command(aliases = ['coin', 'coinroll'])
async def coinflip(ctx):
    embed = discord.Embed(title = '__Coin flip__', description = 'Throws a coin and return heads or tails', color = 0x2f3136)
    embed.add_field(name = '**Syntax**', value = '.coinflip')

    await ctx.send(embed=embed)
@help.command(aliases = ['fire', 'tirer'])
async def shoot(ctx):
    embed = discord.Embed(title = '__Shoot__', description = 'Fires at a member', color = 0x2f3136)
    embed.add_field(name = '**Syntax**', value = '.shoot @<member>')

    await ctx.send(embed=embed)

#⊱⋅───────────────────────── [ MATH ] ──────────────────────────⋅⊰#

# Sum - add two numbers together
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)
    await asyncio.sleep(3)

# Sub - substract two numbers together
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def sub(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne - numTwo)
    await asyncio.sleep(3)

# Mul - multiply two numbers together
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def mul(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne * numTwo)
    await asyncio.sleep(3)

# Div - divide two numbers together
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def div(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne / numTwo)
    await asyncio.sleep(3)

#⊱⋅────────────────────────── [ FUN ] ──────────────────────────⋅⊰#

# Roll - replies a random number between 1 and 100
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def roll(ctx):
    await ctx.channel.purge(limit = 1)

    embed = discord.Embed(color = 0x7bac66)
    embed.add_field(name='__Result__', value = '<:Dice:814968523075354645> ' + f'{random.randint(1, 100)}', inline = False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Invoked by {ctx.author.name}')

    await ctx.send(embed=embed)
    await asyncio.sleep(3)

# 8Ball - replies with a random answer to the user using the command
@bot.command(aliases = ['8ball'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def eightball(ctx, question):
    await ctx.channel.purge(limit = 1)

    responses = ['of course',
                 'clearly',
                 'for sure',
                 'maybe',
                 'yes',
                 'no',
                 'i don′t think so',
                 'definitely not',
                 'never',
                 'impossible']
    embed = discord.Embed(color = 0x0f6ba4)
    embed.add_field(name = '__Question__', value = '<:Question:814968523147182111> ' + question, inline = False)
    embed.add_field(name = '__Answer__', value = '<:Info:814968523122016276> ' + f'{random.choice(responses)}', inline = False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Invoked by {ctx.author.name}')

    await ctx.send(embed = embed)
    await asyncio.sleep(3)

# Coin flip - filps a coin to get a random output
@bot.command(aliases = ['coin', 'coinroll'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def coinflip(ctx):
    await ctx.channel.purge(limit = 1)

    responses = ['heads',
                 'tails']
    embed = discord.Embed(color=0xffc905)
    embed.add_field(name = '__Result__', value = f'<:Coin:814968522086154281> {random.choice(responses)}', inline = False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Invoked by {ctx.author.name}')

    await ctx.send(embed = embed)
    await asyncio.sleep(3)

# Shoot - replies with a message saying that the user that invoked the command is shooting someone
@bot.command(aliases = ['fire', 'tirer'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def shoot(ctx, user_name : discord.User):
    await ctx.send(f'{ctx.author.mention} shoots at {user_name.mention} <a:MonkaShoot:824679435349393408>')
    
    await asyncio.sleep(3)

#⊱⋅───────────────────── [ MODERATION ] ─────────────────────⋅⊰#

# Say - makes the bot say whatever you want it to say
@bot.command()
@commands.has_permissions(administrator = True)
async def say(ctx, *, message: str):
    await ctx.channel.purge(limit = 1)

    await ctx.send(message)

# Dm - makes the bot send a private message to a user
@bot.command(aliases = ['send'])
@commands.has_permissions(administrator = True)
async def dm(ctx, member: discord.Member, *, message: str):
    await ctx.channel.purge(limit = 1)

    await member.send(message)

# Clean - cleans the amount of messages you want
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clean(ctx, *, amount: int):
    await ctx.channel.purge(limit = amount + 1)

# Nuke - nukes a channel by deleting every messages
@bot.command()
@commands.has_permissions(manage_messages = True)
async def nuke(ctx):
    await ctx.channel.purge(limit = 666)

# Kick - sends a message to the user then kicks him
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = 'No reason specified'):
    await ctx.channel.purge(limit = 1)

    await member.send('You have been kicked from **' + member.guild.name + '** for the following reason: *' + reason + '*')
    await member.kick(reason = reason)

# Ban - sends a message to the user then bans him
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = 'No reason specified'):
    await ctx.channel.purge(limit = 1)

    await member.send('You have been banned from **' + member.guild.name + '** for the following reason: *' + reason + '*')
    await member.ban(reason = reason)

# Role - example cmd adding and removing roles
@client.command()
async def role(ctx):
    global members
    guild = client.get_guild(963933760292794459)
    removeRole = guild.get_role(986014064671092806)
    addRole = guild.get_role(986014068047483011)
    members = [member for member in guild.members if removeRole in member.roles]
    for member in members:
        print(member)
        await member.remove_roles(removeRole)
        await member.add_roles(addRole)

#⊱⋅────────────────────────── [ RUN ] ─────────────────────────⋅⊰#

bot.run(bot_token) 
