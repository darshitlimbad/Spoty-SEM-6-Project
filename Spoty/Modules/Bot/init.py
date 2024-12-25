import json
import discord
from discord.ext import commands

from Modules.logger import logger
from Modules.utils import *
from Modules.DB import database

# Load the configuration file
with open('config.json', 'r') as file:
    config = json.load(file)

discord_token = config["discord"].get("TOKEN", None)
adminID = config["discord"].get("ADMINID", None)
prefix = config["discord"].get("PREFIX", '!')

if not discord_token:
    logger.error("DISCORD TOKEN IS MISSING")
    exit()
elif not adminID:
    adminID = "1234"
    logger.warning("Admin ID was not provided so using 1234.")

class Spoty_bot(commands.Bot):
    """Main bot class for handling commands and events."""

    def __init__(self):
        """
        Initialize the bot with a command prefix and all intents.
        Removes the default help command.
        """
        super().__init__(command_prefix=prefix, intents=discord.Intents.all())
        self.remove_command('help')

    def run(self):
        """
        Run the bot by loading cogs and starting the bot with the Discord token.
        """
        super().run(discord_token)
    
    async def on_ready(self):
        await self.tree.sync()
        logger.info("Bot is online and ready to serve.")
        print("-" * 100)

    async def setup_hook(self):
        """
        Sets up the bot by loading cogs and synchronizing the command tree.
        """
        await self.add_cog(Player(self))
        # await self.load_extension('player')
    
    async def on_command_error(self, ctx, error):
        """
        Handles errors that occur during command execution.
        Provides specific responses for common errors and logs detailed information.
        """
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Command Not Found",
                description="The command you tried to use does not exist. Please verify the command and try again.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.warning(f"CommandNotFound: {ctx.message.content}")

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Missing Argument",
                description=f"A required argument is missing: `{str(error.param)}`.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.warning(f"MissingRequiredArgument: {error}")

        else:
            embed = discord.Embed(
                title="An Error Occurred",
                description=f"An unexpected error occurred: `{str(error)}`.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Unhandled error: {error}", exc_info=True)
         
class Player(commands.Cog):
    """Cog to handle music playback commands."""
    def __init__(self, bot):
        self.bot = bot
        self.adminID = int(adminID)          # Admin ID for the bot
        self.current_ctx = None         # Tracks the current context for the bot
        self.current_volume = None      # Default volume level for playback
        self.Queue = Queue()            # Queue to manage upcoming songs
        self.auto_play = False          # Should auto play or not 
        self.song_repeat = False        # Repeat the song or not
        
        # self.dbObj= database.MySQLConnection() # Database object
        # if self.dbObj.is_connected():
        #     logger.info("Database connection established.")
        # else:
        #     logger.error("Database connection failed.")
        
    async def is_bot_connected_to_voice(self, ctx) -> bool:
        """Check if the bot is connected to a voice channel."""
        return ctx.voice_client is not None
       
    @commands.hybrid_command(name="join", with_app_command=True) 
    async def join(self, ctx) -> bool:
        """Connect the bot to the user's voice channel."""
        try:
            if not await self.is_bot_connected_to_voice(ctx):
                if ctx.author.voice:
                    channel = ctx.author.voice.channel
                    await channel.connect(self_deaf=True)
                    self.current_ctx = ctx
                    self.current_volume = 50     # Default volume level for playback                
                    embed = discord.Embed(title="Connected", description=f"Connected to voice channel: **{channel.name}**", color=discord.Color.green())
                    await ctx.send(embed=embed)
                    logger.info(f"Connected to voice channel: {channel.name}.")
                    return True
                else:
                    embed = discord.Embed(
                        title="Error",
                        description="You need to be in a voice channel to play music.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return False
            else:
                embed = discord.Embed(
                    title="Error",
                    description="Bot is already connected to a voice channel.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return False
        except Exception as e:
            embed = discord.Embed(
                title="Connection Error",
                description="Failed to connect to the voice channel.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Error while connecting to voice channel: {e}")
            return False
    
    async def is_user_authorized_to_control(self, ctx) -> bool:
        """Check if the user is authorized to control the bot."""
        if ctx.voice_client and ((ctx.author.voice and (ctx.voice_client.channel == ctx.author.voice.channel)) or (ctx.author.id == self.adminID) or (ctx.author.id == self.bot.user.id)): # Admin gets full permission
            return True
        elif not hasattr(ctx.author, "voice"):
            embed = discord.Embed(
                title="Error",
                description="Please connect to the voice channel.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="Error",
                description="You must be in the same voice channel as the bot to control it.",
                color=discord.Color.red()
            )
            
        await ctx.send(embed=embed)
        return False
    
    async def play_song(self, ctx):
        """Play the next song in the queue."""
        try:
            if ctx.voice_client is None:
                embed = discord.Embed(
                    title="Error",
                    description="The bot is not connected to a voice channel.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                logger.error("Error: Attempted to play a song when the bot is not connected.")
                return

            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                logger.error("Error: Attempted to play the next song while a song is already playing.")
                return
            
            if not self.Queue.is_empty():
                ffmpeg_options = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn',
                }
                
                if self.auto_play is False:
                    self.auto_play = True
                    
                song = self.Queue.get()
                
                async def play_next_song(error=None):
                    if error:
                        logger.error(f"Playback error: {error}")
                    
                    # Ensure the bot is still connected before attempting to play the next song
                    if ctx.voice_client and ctx.voice_client.is_connected():
                        if self.auto_play:
                            if self.song_repeat:
                                source = discord.FFmpegPCMAudio(song['url'], **ffmpeg_options)
                                source = discord.PCMVolumeTransformer(source, self.current_volume / 100)
                                ctx.voice_client.play(source, after=lambda e: self.bot.loop.create_task(play_next_song(e)))
                                
                                embed = discord.Embed(title="Now Playing", description=f"**{song['title']}**", color=discord.Color.blue())
                                await ctx.send(embed=embed)
                                logger.info(f"Playing song: {song['title']}")
                            else:
                                await self.play_song(ctx)
                        else:
                            logger.info("Auto play is disabled, not playing the next song.")
                    else:
                        logger.warning("Bot disconnected from the voice channel, stopping playback.")
                     
                source = discord.FFmpegPCMAudio(song['url'], **ffmpeg_options)
                source = discord.PCMVolumeTransformer(source, self.current_volume / 100)       
                ctx.voice_client.play(source, after=lambda e: self.bot.loop.create_task(play_next_song(e)))
        
                embed = discord.Embed(title="Now Playing", description=f"**{song['title']}**", color=discord.Color.blue())
                await ctx.send(embed=embed)
                logger.info(f"Playing song: {song['title']}")
            
            else:
                logger.info("Playback finished.")
                embed = discord.Embed(
                    title="Playback Finished",
                    description="All songs have been finished.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                
        except Exception as e:
            embed = discord.Embed(
                title="Playback Error",
                description="An error occurred during playback.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Error during playback: {e}", exc_info=True)
    
    @commands.hybrid_command(name="help", with_app_command=True)
    async def help_command(self, ctx, *, command: str = None):
        """Displays the help message with available commands or detailed info for a specific command."""
        embed = discord.Embed(title="Help", color=discord.Color.blue())

        if command is None:
            embed.add_field(name="Songs Players", value=(
                "`play` - Plays song from the given song query.\n"
                "`playnow` - Stops current playback, clears the queue, and immediately plays...\n"
                "`sourceplay` - Plays audio from the given URL or query...\n"
                "`playlist` - Accepts a YouTube playlist URL and fetches the songs then starts playing it.\n"
            ), inline=False)

            embed.add_field(name="Playback Control", value=(
                "`pause` - Pauses the current song.\n"
                "`resume` - Resumes the current song.\n"
                "`skip` - Skips the currently playing song and plays the next song in the queue.\n"
                "`stop` - Stops the current song and clears the queue.\n"
                "`disconnect` - Disconnects the bot from the voice channel.\n"
                "`queue` - Gives you list of upcoming songs.\n"
                "`repeat` - Toggles repeat mode."
            ), inline=False)

            embed.add_field(name="Sources", value=(
                "`sitelist` - Lists the websites from which you can play audio.\n"
            ), inline=False)

            embed.add_field(name="No Category", value="`help` - Shows this message", inline=False)
            embed.set_footer(text="Type `!help [command]` for more info on a command.")
        else:
            # Detailed info for a specific command
            command_info = {
                'join': "`join` - Joins the bot to the voice channel that you are currently in. Use this command when you want the bot to connect to your voice channel so it can start playing music or other audio.",
                'play': "`play` - Plays song from the given song query. This command starts playing the song that matches the given query.",
                'playnow': "`playnow` - Stops current playback, clears the queue, and immediately plays the specified song. This command is useful if you want to clear the queue and play a new song immediately.",
                'sourceplay': "`sourceplay` - Plays media from the given URL or query. For a list of supported URLs, use `sitelist`. This command is used to play media from a specified URL or query.",
                'playlist': "`playlist` - Accepts a YouTube playlist URL and fetches the entire playlist, then starts playing it. This command is used to queue up and play all the songs from a specified YouTube playlist. \n NOTE: The playlist should not have any unavailable songs listed.",
                'pause': "`pause` - Pauses the current song. Use this command if you want to temporarily stop the playback of the current song.",
                'resume': "`resume` - Resumes the current song. Use this command to continue playback if a song was previously paused.",
                'skip': "`skip` - Skips the currently playing song and plays the next song in the queue. This command is used to skip the current song and proceed to the next one.",
                'stop': "`stop` - Stops the current song and clears the queue. Use this command to stop the playback and remove all songs from the queue.",
                'disconnect': "`disconnect` - Disconnects the bot from the voice channel. Use this command when you want to stop the bot from playing music and disconnect it from the voice channel.",
                'queue': "`queue` - Gives you a list of all upcoming songs from the queue with their indexes. You can use the `skip` command to jump to the corresponding index of the song.",
                'repeat': "`repeat` - Toggles repeat mode for the current playing media.",
                'sitelist': "`sitelist` - Lists the websites from which you can play audio. This command provides a list of supported websites for audio playback.",
                'help': "`help` - Shows this help message. Use this command to get information about all available commands."
            }

            description = command_info.get(command.lower(), "Command not found. Please provide a valid command.")
            embed.add_field(name=f"Help for `{command}`", value=description, inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="play", with_app_command=True)
    async def play(self, ctx, *, query=None):
        """Play a song from a search query."""
        try:
            if query is None:
                embed = discord.Embed(
                    title="Error",
                    description="A required argument is missing: `query`.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            if not await self.is_bot_connected_to_voice(ctx):
                if not await self.join(ctx):
                    return
            elif not await self.is_user_authorized_to_control(ctx):
                return
            
            processing_embed = discord.Embed(
                title="Processing...",
                description="Your request is being processed. Please wait a moment.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=processing_embed)
    
            song = await self.bot.loop.run_in_executor(None, search_song, query)

            if song['url']:
                self.Queue.put(song)
                
                if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                    await self.play_song(ctx)
                    return
                
                embed = discord.Embed(
                    title="Added to Queue",
                    description=f"**{song['title']}** has been added to the `queue`.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                logger.info(f"Added song to queue: {song['title']}")
            else:
                embed = discord.Embed(
                    title="Search Error",
                    description="No results found for your query.",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description="An error occurred while processing your request.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Error in play command: {e}")
            
    @commands.hybrid_command(name="sourceplay", with_app_command=True)
    async def sourceplay(self, ctx, *, query=None):
        """Play any media from a YouTube URL or query."""
        try:
            if query is None:
                embed = discord.Embed(
                    title="Error",
                    description="A required argument is missing: `query`.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            if not await self.is_bot_connected_to_voice(ctx):
                if not await self.join(ctx):
                    return
            elif not await self.is_user_authorized_to_control(ctx):
                return
            
            processing_embed = discord.Embed(
                title="Processing...",
                description="Your request is being processed. Please wait a moment.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=processing_embed)
            
            song = await self.bot.loop.run_in_executor(None, search_by_query, query)
            
            if song['url']:
                self.Queue.put(song)
                
                if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                    await self.play_song(ctx)
                    return
                
                embed = discord.Embed(
                    title="Added to Queue",
                    description=f"**{song['title']}** has been added to the queue.",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
                logger.info(f"Added media to queue: {song['title']}")
            else:
                embed = discord.Embed(
                    title="Search Error",
                    description="No results found for your query.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description="An error occurred while processing your request.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Error in sourceplay command: {e}")
            
    @commands.hybrid_command(name="playlist", with_app_command=True)
    async def playlist(self, ctx, *, playlist_url=None):
        """Play any playlist from a YouTube playlist URL."""
        try:
            if playlist_url is None:
                embed = discord.Embed(
                    title="Error",
                    description="A required argument is missing: `playlist_url`.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            if not await self.is_bot_connected_to_voice(ctx):
                if not await self.join(ctx):
                    return
            elif not await self.is_user_authorized_to_control(ctx):
                return
                
            processing_embed = discord.Embed(
                title="Processing...",
                description="Your request is being processed. Please wait a moment.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=processing_embed)
            
            songs = await self.bot.loop.run_in_executor(None, fetch_playlist, playlist_url)
            if len(songs): 
                
                self.Queue.merge(songs)
                
                embed = discord.Embed(
                    title="Added to Queue",
                    description="Your Playlist has been added to the queue.",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
                logger.info("Added Playlist to queue")
                
                if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                    await self.play_song(ctx)
                    return
            else:
                embed = discord.Embed(
                    title="Search Error",
                    description="No Playlist found from your URL.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description="An error occurred while processing your request.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Error in playlist command: {e}")
            
    @commands.hybrid_command(name="playnow", with_app_command=True)
    async def playnow(self, ctx, *, query=None):
        try:
            
            await self.stop(ctx)
            await self.play(ctx,query=query)
            
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description="An error occurred while processing your request.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Error in playnow command: {e}")
        
    @commands.hybrid_command(name="repeat", with_app_command=True)
    async def repeat(self,ctx):
        """Toggles repeat mode."""
        if self.song_repeat is False :
            self.song_repeat=True
            embed = discord.Embed(
                title="Repeat Mode",
                description=f"Repeat mode Turned **ON** :white_check_mark:",
                color=discord.Color.blue()
            )
        else: 
            self.song_repeat=False
            embed = discord.Embed(
                title="Repeat Mode",
                description=f"Repeat mode Turned **OFF** :negative_squared_cross_mark: ",
                color=discord.Color.blue()
            )
        
        logger.info(f"Repeat mode tuned : {self.song_repeat}")
        await ctx.send(embed=embed)
        
    @commands.hybrid_command(name="pause", with_app_command=True)
    async def pause(self, ctx):
        """Pause the currently playing song."""
        if await self.is_user_authorized_to_control(ctx) and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            embed = discord.Embed(title="Paused", description="Playback has been paused.", color=discord.Color.orange())
            await ctx.send(embed=embed)
            logger.info("Playback paused.")
        else:
            embed = discord.Embed(
                title="Error",
                description="No song is currently playing.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="resume", with_app_command=True)
    async def resume(self, ctx):
        """Resume the paused song."""
        if await self.is_user_authorized_to_control(ctx) and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            embed = discord.Embed(title="Resumed", description="Playback has resumed.", color=discord.Color.green())
            await ctx.send(embed=embed)
            logger.info("Playback resumed.")
        else:
            embed = discord.Embed(
                title="Error",
                description="No song is currently paused.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="skip", with_app_command=True)
    async def skip(self, ctx, index=None):
        """
        skip the current song and play the next one.

        Args:
            ctx (commands.Context): The context in which the command was invoked.
            index (int, optional): The index of the song in the queue to skip to. Defaults to None, which skips to the next song.
        """
        try:
            if not await self.is_user_authorized_to_control(ctx):
                return

            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                if index is not None:
                    index = int(index) - 1
                    self.Queue.shuffle_index(index, 0)

                # Stop the current song to skip to the next 
                ctx.voice_client.stop() # after= will call self.play_song() automatically
                embed_skip = discord.Embed(title="Song Skipped", color=discord.Color.orange())
                await ctx.send(embed=embed_skip)
                logger.info("Song skipped.")
                
            else:
                embed = discord.Embed(title="No Song Playing", description="There is currently no song playing.", color=discord.Color.red())
                await ctx.send(embed=embed)
                logger.warning("Attempted to skip when no song was playing.")
        
        except (ValueError, IndexError):
            embed = discord.Embed(
                title="Error",
                description="Please provide a valid index (e.g., 1).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Invalid input for index: {index}")
    
        except Exception as e:
            embed = discord.Embed(title="Error", description="Something went wrong!", color=discord.Color.red())
            await ctx.send(embed=embed)
            logger.error(f"Error during skip command: {e}")


    @commands.hybrid_command(name="stop", with_app_command=True)
    async def stop(self, ctx):
        """Stop the playback and clear the queue."""
        if await self.is_user_authorized_to_control(ctx):
            self.Queue.clear()
            self.auto_play = False
            self.song_repeat= False
            ctx.voice_client.stop()
            embed = discord.Embed(title="Stopped", description="Playback has been stopped, and the queue is cleared.", color=discord.Color.red())
            await ctx.send(embed=embed)
            logger.info("Playback stopped and queue cleared.")
    
    @commands.hybrid_command(name="disconnect", with_app_command=True)
    async def disconnect(self, ctx):
        """Disconnect the bot from the voice channel."""
        try:
            if await self.is_user_authorized_to_control(ctx):
                await self.stop(ctx)
                await ctx.voice_client.disconnect()
                
                self.current_ctx = None
                
                embed = discord.Embed(
                    title="Disconnected",
                    description="The bot has been successfully disconnected from the voice channel.",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
                logger.info("Bot disconnected from voice channel.")
            
        except Exception as e:
                embed = discord.Embed(
                    title="Disconnection Error",
                    description=f"An error occurred while attempting to disconnect:`.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                logger.error(f"Error during disconnection: {e}", exc_info=True)
    
    @commands.hybrid_command(name="queue", with_app_command=True)
    async def queue(self, ctx):
        """Display the current song queue."""
        try:
            if await self.is_user_authorized_to_control(ctx):
                if self.Queue.is_empty():
                    embed = discord.Embed(
                        title="Queue Empty",
                        description="There are no songs in the queue.",
                        color= discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return

                embed = format_queue(self.Queue.queue())
                await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred while retrieving the queue",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Error in queue command: {e}")
            
    @commands.hybrid_command(name="volume", with_app_command=True)
    async def volume(self, ctx, volume = None):
        """Set the volume level or return the current volume if no value is provided."""
        try:
            if True:
                if not await self.is_bot_connected_to_voice(ctx):
                    embed = discord.Embed(
                            title="Error",
                            description=f"The Bot is not connected to any voice channel.",
                            color=discord.Color.red()
                        )
                    await ctx.send(embed=embed)
                    return 
                
                if await self.is_user_authorized_to_control(ctx):
                    if volume is None:
                        embed = discord.Embed(
                            title="Current Volume",
                            description=f"The current volume is :{self.current_volume}%",
                            color=discord.Color.blue()
                        )
                        await ctx.send(embed=embed)
                    else:
                        volume= int(volume)
                        if not 0 <= volume <= 100:
                            embed = discord.Embed(
                                title="Invalid Volume",
                                description="Volume must be between 0 and 100.",
                                color=discord.Color.red()
                            )
                            await ctx.send(embed=embed)
                            return
                        
                        self.current_volume = volume
                        if ctx.voice_client.source:
                            ctx.voice_client.source.volume = self.current_volume / 100
                            
                        embed = discord.Embed(title="Volume Set", description=f"Volume has been set to {volume}%.", color=discord.Color.green())
                        await ctx.send(embed=embed)
                        logger.info(f"Volume set to {volume}%.")
                else: 
                    logger.warn("Unauthorized attempt in Volume command!")
            else:
                embed = discord.Embed(
                    title="Error",
                    description="Bot is not connected to voice channel.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
            
        except ValueError:
            embed = discord.Embed(
                title="Invalid Volume Level",
                description="Please enter a volume level between 0 to 100.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Invalid Volume Level")
            
        except Exception:
            embed = discord.Embed(
                title="Something went wrong!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            logger.error(f"Something went wrong for volume command : {volume}")
    
    @commands.hybrid_command(name="sitelist", with_app_command=True)
    async def sitelist(self, ctx):
        """Display the list of supported websites for audio playback."""
        embed = discord.Embed(
            title="Supported Websites",
            description="The bot supports playback from the following websites:\n"
                        "- YouTube\n"
                        "- more comming soon...\n",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Handles voice state updates, including when a member leaves the voice channel."""
        
        if before.channel and not after.channel:
            members_in_channel = before.channel.members
            
            # Check if the bot is the only member left in the voice channel
            if len(members_in_channel) == 1 and members_in_channel[0] == self.bot.user:
                # Notify that the bot is the only member left in the voice channel
                embed = discord.Embed(
                    title="Voice Channel Update",
                    description="The bot is now the only member in the voice channel. It will disconnect.",
                    color=discord.Color.red()
                )
                logger.info("Bot is the only member in the voice channel. Disconnecting the bot.")
                
                if self.current_ctx and self.current_ctx.channel:
                    message = await self.current_ctx.channel.send(embed=embed)
                    tempctx = await self.bot.get_context(message)
                    # Disconnect the bot from the voice channel
                    await self.disconnect(tempctx)
                    
    # this is the test command to check if the user is premium or not will be removed later
    @commands.hybrid_command(name="test", with_app_command=True)
    async def test(self, ctx):
        
        author_id = ctx.author.id
        print(author_id)
        if(self.dbObj.is_user_premium(author_id)):
            embed = discord.Embed(
                title="Premium user",
                description="Ahh.. premium user.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(
                title="Not Premium",
                description="Chiiiii tatiiii user.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        