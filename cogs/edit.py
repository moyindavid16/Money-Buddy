import discord
from discord.ext import commands
import asyncio
from .vars import *
from discord import ui

class edit(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name="edit")
    async def edit(self, ctx, *args:str):       
        if len(args) == 1:
            cat = args[0]
            new_catagory =  await prompt1(self.client,ctx,'what would you like to change ' + cat + ' to?',timeout=20)
            await ctx.send(new_catagory)
            expenses[ctx.author.id][new_catagory] = expenses[ctx.author.id].pop(cat)
        elif len(args) == 2:
            args = list(args)
            new_expense = await prompt2(self.client,ctx,'what would you like to change ' + str(expenses[ctx.author.id][str(args[0])][int(args[1]) - 1]) + ' to?', timeout=20 )
            expenses[ctx.author.id][args[0]][int(args[1]) - 1] = new_expense
            update_db()
            await ctx.send("Successfully changed to " + str(new_expense)+ '!')
        else:
            await ctx.send('please format yor edit request as edit [catagory] or edit [catagory] [# of expense]')


async def prompt1(client, ctx, message: str, timeout: int):
    await ctx.send(message)
    message = await client.wait_for('message', check = lambda message: message.author == ctx.author,timeout=timeout)
    return message.content

async def prompt2(client, ctx, message: str, timeout: int):
    await ctx.send(message)
    message = await client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=timeout)
    args = message.content.split()
    try:
        args[1]=float(args[1])
    except Exception as e:
        args[1]=0
    
    if args[1] <= 0.0:
        ctx.send("Try again. The amount is invalid")
        return None
    return args



async def setup(client):
    await client.add_cog(edit(client))