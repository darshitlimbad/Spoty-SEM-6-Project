from Modules.Bot.init import *
from Modules.utils import *
from Modules.logger import logger
from Modules.PrintLicense import print_license

def main():
    # Prints LICENSE
    print_license()
    
    # Initialize and run the Discord bot
    bot = Spoty_bot()
    bot.run()

if __name__ == '__main__':
    main()