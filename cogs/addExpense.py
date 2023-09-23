import discord
from discord.ext import commands
import asyncio
from .vars import *
from discord import ui

async def addCategory(ctx: commands.Context, args: list):
    expenses[args[0]]=[]
    return await ctx.channel.send(f"You have successfully added the {args[0]} category")

# cogs let you put related commands and functions together under a class
class AddExpense(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='add')
    async def add(self, ctx: commands.Context, *args: str):
        args = list(args)
        
        if len(args) == 1:
            if args[0] in expenses:
                return await ctx.channel.send(f"{args[0]} is already a category")
            return await addCategory(ctx, args)
        
        if len(args) >= 3:
            desc = ""
            if len(args)>=4:
                desc = " ".join(args[3:])
            if args[0] not in expenses:
                await addCategory(ctx, args)
            if [args[1], args[2], desc] in expenses[args[0]]:
                return await ctx.send("Sorry, you added that expense previously")
            expenses[args[0]].append([args[1], args[2], desc])
            return await ctx.channel.send("Success")
        return await ctx.channel.send("You have to add in one of these formats\n1. add category\n2. add category date amount decsription(optional)")
       

    @commands.command(name="show")
    async def show(self, ctx: commands.Context):
        return await ctx.send(expenses)


# add this cog to the client
async def setup(client):
    await client.add_cog(AddExpense(client))