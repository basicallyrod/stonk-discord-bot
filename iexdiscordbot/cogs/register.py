import discord
from discord.ext import commands
import asyncpg
from iexdiscordbot.database.config import config

class register(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Register Command Loaded')

    @commands.command()
    async def register(self, ctx):
        connection = None
        id = ctx.message.author.id
        name = ctx.message.author.name
        discriminator = ctx.message.author.discriminator
        print(f'{id} | {name} | {discriminator}')
        try:
            params = config()
            print('Connecting to the postgreSQL database...')
            connection = await asyncpg.connect(**params)

            #create a cursor
            # async with connection.transaction():
            #     crsr = await connection.cursor('INSERT INTO users (id, name);')

            await connection.execute('''
                INSERT INTO users (id, name, discriminator) VALUES($1, $2, $3)
            ''', id, name, discriminator)

                #await crsr.execute('SELECT version()') #use this coroutine to execute an SQL command

            #run the query SQL input here, have atleast the watchlist command output here
                # db_version = await crsr.fetchrow()
                # print(f'PostgreSQL database version: {db_version}')


                #print(db_version)
                #await crsr.close() #We do not need to use close because it is done automatically
        # except(Exception, asyncpg.DatabaseError) as error:
        #     print(f'Exception: {error}')
        #     print(error)
        finally:
            if connection is not None:
                await connection.close()
                print('Database connection terminated.')

def setup(client):
    client.add_cog(register(client))
