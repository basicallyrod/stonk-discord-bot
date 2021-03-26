import discord
import os
from discord.ext import tasks, commands
from dotenv import load_dotenv
import asyncio
import tracemalloc
import numpy
import pandas
import requests
import asyncpg

from iexdiscordbot.database.config import config

#tracemalloc.start()

async def connect():
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database...')
        connection = await asyncpg.connect(**params)

        #create a cursor
        async with connection.transaction():
            crsr = await connection.cursor('SELECT version()')
            #await crsr.execute('SELECT version()') #use this coroutine to execute an SQL command

        #run the query SQL input here, have atleast the watchlist command output here
            db_version = await crsr.fetchrow()
            print(f'PostgreSQL database version: {db_version}')


            #print(db_version)
            #await crsr.close() #We do not need to use close because it is done automatically
    # except(Exception, asyncpg.DatabaseError) as error:
    #     print(f'Exception: {error}')
    #     print(error)
    finally:
        if connection is not None:
            await connection.close()
            print('Database connection terminated.')

#loop = asyncio.get_event_loop().run_until_complete(connect)

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

#client = discord.Client()
client = commands.Bot(command_prefix = '$')

@client.command(pass_context=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command(pass_context=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


if __name__ == "__main__":
    asyncio.run(connect())
    asyncio.run(client.run(DISCORD_TOKEN))
