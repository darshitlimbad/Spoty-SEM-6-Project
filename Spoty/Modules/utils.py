import yt_dlp
import discord
from Modules.logger import logger

class Queue:
    def __init__(self):
        self.Queue = []

    def put(self, item=None):
        if item:
            self.Queue.append(item)
            return len(self.Queue) - 1
        return None
    
    def put_at(self, item, index: int):
        if 0 <= index < self.qsize():
            self.Queue.insert(index, item)
            return True
        raise IndexError("Index out of range")
    
    def merge(self, merge_list):
        if len(merge_list):
            for item in merge_list:
                self.Queue.append(item)
            return True
        return False
    
    def shuffle_index(self, from_index: int, to_index: int) -> bool :
        if 0 <= from_index < self.qsize() and 0 <= to_index < self.qsize():
            self.Queue.insert(to_index, self.Queue.pop(from_index))
            return True
        else:
            raise IndexError("Index out of range")
       
    def get(self, index: int = 0):
        if 0 <= index < self.qsize():
            return self.Queue.pop(index)
        raise IndexError("Index out of range")
       
    def queue(self):
        return self.Queue if not self.is_empty() else None 
    
    def clear(self):
        self.Queue = []
        return True
        
    def qsize(self):
        return len(self.Queue)

    def is_empty(self):
        return self.qsize() == 0


def search_song(query):
    """Search for a song on YouTube by query.

    Args:
        query (str): The search query for the song.

    Returns:
        dict: A dictionary containing the title and URL of the first result.
    """
    try:
        ydl_opts = {
            'format': 'bestaudio[abr>0]/bestaudio/best',  # Get the best audio with bitrate > 0
            'extract_flat': False, 
            'default_search': 'ytsearch',
            'quiet': True,
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"{query} Song or Music", download=False)
            if 'entries' in info:
                audio = info['entries'][0]
                return {'title': audio['title'], 'url': audio['url']}
        return {'title': None, 'url': None}

    except Exception as e:
        logger.error(f"Error occurred while fetching song: {e}")
        return {'title': None, 'url': None}

def search_by_query(query):
    """Search YouTube by query or URL and return the first result.

    Args:
        query (str): The search query or URL.

    Returns:
        dict: A dictionary containing the title and URL of the first result.
    """
    try:
        ydl_opts = {
            'format': 'bestaudio[abr>0]/bestaudio/best',
            'quiet': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if 'youtube.com' in query or 'youtu.be' in query:
                info = ydl.extract_info(query, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                
            if 'entries' in info: 
                audio = info['entries'][0]
                return {'title': audio['title'], 'url': audio['url']}
            elif 'url' in info:
                return {'title': info.get('title', "Title Not Found"), 'url': info['url']}
            
        return {'title': None, 'url': None}
    except Exception as e:
        logger.error(f"Error occurred while fetching audio: {e}")
        return {'title': None, 'url': None}

def fetch_playlist(playlist_url: str):
    """Fetch a playlist from YouTube by URL and retrieve the best audio URL for each track, The playlist should not have any unavailable songs listed.

    Args:
        playlist_url (str): The URL of the YouTube playlist.

    Returns:
        list: A list of dictionaries containing the title and best audio URL of each song in the playlist.
    """
    try:
        ydl_opts = {
            'format': 'bestaudio[abr>0]/bestaudio/best',  # Get the best audio with bitrate > 0
            'quiet': False,  # Toggle verbose mode on
            'extract_flat': False,  # Extract full metadata
            'playlist_items': '1-',  # Fetch all items in the playlist
            'noplaylist': False,  # Ensure playlist processing is enabled
            'ignoreerrors': True,  # Ignore errors for unavailable videos
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
                
            playlist_songs = []
            if 'entries' in info:
                for entry in info['entries']:
                    if entry and entry.get('title') and entry.get('formats'):
                        # Filter the formats to get the best audio URL
                        best_audio = max(
                            (f for f in entry['formats'] if f.get('acodec') != 'none' and f.get('abr') is not None),
                            key=lambda f: f.get('abr', 0) or 0,  # Choose by bitrate (abr)
                            default=None
                        )
                        if best_audio:
                            song_info = {
                                'title': entry['title'],
                                'url': best_audio['url']
                            }
                            playlist_songs.append(song_info)
                            logger.info(f"Successfully fetched song: {entry['title']}")

            return playlist_songs

    except Exception as e:
        logger.error(f"Error occurred while fetching playlist: {e}")
        return []

def format_queue(queue):
    """Format the song queue for display in embeds.

    Args:
        queue (list): A list of dictionaries where each dictionary represents a song with a 'title' key.

    Returns:
        list: A list of discord.Embed objects containing the formatted song queue.
    """
    embeds = []
    embed = discord.Embed(title="Current Queue", color=discord.Color.blue())
    
    header = "Index\t Song"
    entries = [header]
    total_length = len(header) + 4  # Initial length with some buffer

    for i, song in enumerate(queue, start=1):
        title = song.get('title', "N/A")
        short_title = ' '.join(title.split()[:4])
        entry = f"#{i:<5} {short_title:<20}"
        entry_length = len(entry) + 1  # +1 for the newline character

        if total_length + entry_length > 4096:
            embed.description = f"```\n{'\n'.join(entries)}\n```"
            embeds.append(embed)
            embed = discord.Embed(title="Current Queue (cont.)", color=discord.Color.blue())
            entries = [header]
            total_length = len(header) + 4

        entries.append(entry)
        total_length += entry_length

    if entries:
        embed.description = f"```\n{'\n'.join(entries)}\n```"
        embeds.append(embed)

    return embeds

