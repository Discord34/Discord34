# This bot is poorly coded and
# has no cogs, but to be fair 
# it's just 1 command basically

# Imports
import asyncio
import discord
from discord.ext import commands
import random
import rule34 # this library sucks and has ass documentation
import os
import time



# Client setup
client = commands.Bot(command_prefix=commands.when_mentioned_or('r! ', 'r34! ', 'r!', 'r34!'))
client.remove_command('help')
r34 = rule34.Rule34(client.loop)
colors = [discord.Color.red(), discord.Color.orange(), discord.Color.gold(), discord.Color.green(), discord.Color.blue(), discord.Color.purple(), discord.Color.magenta(), discord.Color.blurple()]


# When ready
@client.event
async def on_ready():
    print('Bot ready.')
    while True:
        servers = str(len(client.guilds))
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'hentai and {servers} servers'))
        await asyncio.sleep(30)     

            
# r34 command
@client.command(aliases=['r34', 'rule34'])
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
async def _rule34(ctx, *, user_tags=None):
    if ctx.message.channel.is_nsfw() or messsage.channel.type == 'dm':
        if user_tags == None:
            await ctx.send('Hmm... maybe put some tags?')
            return
        
        async with ctx.typing():
            ### Gets the file
            file = await r34.getImages(user_tags, randomPID=True)
            # No images found.
            if not file:
                await ctx.send('No images found.')
                return


            ### Gets a random image
            file = random.choice(file)
            
            # Gets image url, tags, and score
            url = file.file_url
            image_tags = file.tags
            score = file.score


            ### Makes the tags look nice instead of being an ['array']
            t = ''
            index = 0
            for i in range(len(image_tags)-1):
                t = t + f'{image_tags[index]}, '
                index = index + 1
            t = t + f'{image_tags[index]}'
                        
            # Replace _ with \_ so italics do not exist
            t = t.replace('_', '\_')

            # If tags > 1024, discont...
            if len(user_tags) > 1024:
                t = f'{user_tags[:-3]}...'


            ### Embed
            embed = discord.Embed(color=random.choice(colors))
            embed.add_field(name='Tags', value=t, inline=False)
            embed.add_field(name='Score', value=score, inline=False)
            embed.add_field(name='Post not showing?', value='Click [here]({}) to open it in your browser.'.format(url), inline=False)
            embed.set_footer(text=f'Requested by {ctx.message.author}')
            embed.set_image(url=url)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='BONK!', description='Go to an NSFW channel!', color=random.choice(colors))
        embed.set_image(url='https://i.kym-cdn.com/entries/icons/facebook/000/033/758/Screen_Shot_2020-04-28_at_12.21.48_PM.jpg')
        embed.set_footer(text=f'Requested by {ctx.message.author}')
        await ctx.send(embed=embed)

        
# ping command
@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping(ctx):
    ping = round(client.latency * 1000) 
    if ping < 50:
        embed = discord.Embed(title='Pong!', color = discord.Color.green(), description=f'Client latency: {ping}ms')
    elif ping > 50 and ping < 100:
        embed = discord.Embed(title='Pong!', color = discord.Color.gold(), description=f'Client latency: {ping}ms')
    else:
        embed = discord.Embed(title='Pong!', color = discord.Color.red(), description=f'Client latency: {ping}ms')
    await ctx.send(embed=embed)


# help command
@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def help(ctx):
    embed=discord.Embed(title='Discord34 help!', color=random.choice(colors))
    embed.add_field(name='How do I use this bot?', value='The usage is simple! Simply go to an NSFW-marked channel and type the following:\n`r!rule34 [tags]` or `r!r34 [tags]`', inline=False)
    embed.add_field(name='What prefixes does the bot have?', value='<@833280151730126848>\n`r34!`\n`r!`', inline=False)
    embed.add_field(name='What other commands are there?', value='`r!help`\n`r!info`\n`r!ping`', inline=False)
    embed.add_field(name='Why are there not that many commands?', value='Cuz... porn.', inline=False)
    await ctx.send(embed=embed)
    

# info command
@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def info(ctx):
    servers = len(client.guilds)
    embed=discord.Embed(title='Info!', color=random.choice(colors))
    embed.add_field(name='Server count', value=servers, inline=False)
    embed.add_field(name='Links', value='[Github](https://github.com/Discord34/Discord34) | [Bot invite](https://discord.com/api/oauth2/authorize?client_id=833280151730126848&permissions=388160&scope=bot)', inline=False)
    await ctx.send(embed=embed)


# On error
@client.event
async def on_command_error(ctx, error):
    # Command not found
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found.')

    # Bot cooldown
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.add_reaction('⌛')
        
    # Max concurrency
    if isinstance(error, commands.MaxConcurrencyReached):
        await ctx.message.add_reaction('⏳')   


# runs bot
client.run(os.environ['TOKEN'])
