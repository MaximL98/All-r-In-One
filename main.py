""" import discord
from tok import TOKEN
from discord import Intents
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import random

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

token = TOKEN

@bot.event
async def on_ready():
    print(f"Loggend in as {bot.user.name} (ID:{bot.user.id})")


@bot.command()
async def repeat(ctx, *, arg):
    await ctx.send(arg)

@bot.command()
async def remindIn(ctx, time, *, message):
    # Parse the time
    units = {
        "s": "seconds",
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks"
    }
    unit = time[-1]
    if unit not in units:
        await ctx.send("Invalid time format. Use a format like 5s, 3m, 2h, 1d, or 1w.")
        return

    time = int(time[:-1])
    future = datetime.now() + timedelta(**{units[unit]: time})

    # Wait for the specified time
    await asyncio.sleep((future - datetime.now()).total_seconds())

    # Send the reminder
    await ctx.send(f"Reminder: {message}")



class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return f'{ctx.author} slapped {to_slap} because *{argument}*'

@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)


bot.run(token) """