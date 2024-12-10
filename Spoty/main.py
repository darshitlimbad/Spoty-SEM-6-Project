# import discord
# from discord.ext import commands

from Modules.DB.database import MySQLConnection
from Modules.Bot.init import *
from Modules.utils import * 
    
from Modules.logger import logger
from Modules.PrintLicence import print_license

def main():
    # Prints LICENCE
    print_license()
    
    # Mysql Connection
    db = MySQLConnection()
    conn = db.get_connection()
    
    # Discord bot
    bot = Spoty_bot()
    bot.run(discord_token)

if __name__ == '__main__':
    main()