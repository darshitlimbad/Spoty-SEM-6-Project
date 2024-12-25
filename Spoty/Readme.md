# Spoty Discord Bot

Welcome to Spoty, your ultimate Discord music companion! Spoty offers seamless audio streaming and management within your Discord server. Below is a guide to using the bot and its commands.

## Commands

- **`join`**: Joins the bot to the voice channel that you are currently in.
- **`play`**: Plays a song from the given song query.
- **`playnow`**: Stops current playback, clears the queue, and immediately plays the specified song.
- **`sourceplay`**: Plays media from the given URL or query. For a list of supported URLs, see `sitelist`.
- **`playlist`**: Accepts a YouTube playlist URL and fetches the entire playlist, then starts playing it.
- **`pause`**: Pauses the current song.
- **`resume`**: Resumes the current song.
- **`skip`**: Skips the currently playing song and plays the next song in the queue.
- **`stop`**: Stops the current song and clears the queue.
- **`disconnect`**: Disconnects the bot from the voice channel.
- **`queue`**: Lists all upcoming songs in the queue with their indexes.
- **`repeat`**: Toggles repeat mode for the currently playing media.
- **`sitelist`**: Lists the websites from which you can play audio.
- **`help`**: Shows this help message.

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/darshitlimbad/Spoty.git
   ``` 

2. **Install Dependencies:**

   Ensure you have Python 3.8+ installed. Then install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

    Additionally, make sure you have [FFMPEG](https://ffmpeg.org/download.html) downloaded and installed.

3. **Configure Your Bot:**

    Create a `config.json` file in the root directory with the following structure:

    ```json
    {
        "TOKEN": "YOUR_DISCORD_BOT_TOKEN",
        "PREFIX": "!",
        "ADMINID": "YOUR_DISCORD_ADMIN_ID"  
    }
    ``` 
    Note: `ADMINID` is optional. If you don't want to provide an admin ID, you can use any number like `1232`.

4. **Run the Bot:**

   Execute the bot script:

   ```bash
   python main.py
   ``` 

## Development

To contribute or customize the bot, follow these steps:

1. **Fork the Repository** and create a new branch for your changes.
2. **Make Your Changes** and test thoroughly.
3. **Submit a Pull Request** with a clear description of your modifications.

## License

Spoty - Discord Music Companion Built using Python and YT_dlp
```
    Spoty - Discord Music Companion Built using Python and YT_dlp
    Copyright (C) 2024  Darshit Limbad

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

## Contact

For further information or support, please reach out at:
- **Email:** darshitlimbad+git@example.com
- **LinkedIn:** [Darshit Limbad](https://www.linkedin.com/in/darshit-limbad/)