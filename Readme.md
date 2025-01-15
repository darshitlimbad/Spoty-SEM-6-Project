# Spoty - Your Discord Music Companion

![Spoty Logo](SpotyWeb/favicon.ico)  <!-- Replace with your logo path -->

<br>

[Spoty Web](http://spoty.ct.ws/)  : http://spoty.ct.ws/
## Introduction

Spoty is a Discord music bot designed to elevate your listening experience. It allows you to seamlessly play high-quality audio in your Discord servers, manage your music queue, and enjoy a range of features – with both free and premium options. This repository contains the code for the bot and its companion website.

## Preview Video

<video width="640" height="360" controls autoplay loop >
  <source src="SpotyWeb/Media/SpotyHomePageAnimation.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Key Features

*   **High-Quality Audio:** Stream music in crystal-clear quality directly to your Discord server.
*   **Seamless Playback Controls:** Easy-to-use commands in Discord for play, pause, skip, queue management, and more.
*   **Queue Management:** Add songs to a queue, view the current queue, and rearrange the playlist.
*   **24/7 Uptime (Premium):** Enjoy uninterrupted music playback with the premium plan.
*   **Ad-Free Experience (Premium):** Say goodbye to interruptions with the premium, ad-free option.
*   **Priority Support (Premium):** Get faster support with a premium membership.
*   **User-Friendly Interface:** An intuitive and easy-to-understand interface for all users.
*   **Command Categories:** Commands are categorized for ease of use like: `Song Players`, `Playback Control`, `Sources` etc.
*   **Subscription Plans:** Clear distinction between free and premium features, allowing users to choose the right plan for them.

## Website Features

The Spoty website serves as a companion platform to the Discord bot, offering:

*   **Landing Page:** A home page that introduces the bot with information and login buttons.
*   **Features Page:** Showcases the bot's key features in a structured and visually appealing manner.
*   **Subscription Page:** Displays a comparison of the free and premium plans, including a breakdown of the command categories.
*   **Profile Page:** Shows the user's profile, including details fetched from a database (if user is logged in).
*   **Dynamic Navbar:** A navbar that changes based on user authentication state (`Sign In` or user profile icon).

## Technology Stack

*   **Discord.py:** The core library for developing the Discord bot.
*   **Python:** The primary programming language for the bot's backend.
*   **HTML, CSS, JavaScript:** Used for the bot's companion website's frontend.
*   **PHP:** Used for fetching user information in the profile page.
*   **MySQL:** For database management.
*   **FFmpeg:** Used for audio processing.

## Setup Instructions

### Discord Bot Setup

1.  **Create a Discord Application:**
    *   Go to the [Discord Developer Portal](https://discord.com/developers/applications).
    *   Create a new application and copy its **token**.
2.  **Invite the Bot to Your Server:**
    *   Use the OAuth2 URL generator in the Developer Portal to invite the bot to your Discord server.
3.  **Environment Setup:**
    *   Install Python 3.7 or higher.
    *   Install necessary Python packages using `pip install -r requirements.txt`.
4.  **Configuration:**
    *   rename the file `config.json.example` to `config.json`.
    * Do the same with other `json.example` files and enter correct data.
    *   Add your Discord bot's token and admin id, prefix and website info in this file. Example:

        ```json
        {
          "discord": {
            "TOKEN": "YOUR_DISCORD_BOT_TOKEN",
            "ADMINID": "YOUR_DISCORD_ADMIN_ID",
             "PREFIX" : "!",
          },
           "website": {
            "PREMIUM_URL": "URL_TO_YOUR_PREMIUM_MEMBERSHIP_PAGE",
            }
        }
       ```
5.  **Run the Bot:**
    *   Execute the main Python file (e.g., `main.py`) or any python file to run the bot.

### Website Setup

1.  **HTML, CSS, JS Setup:**
    *   Copy all of the `CSS`, `Scripts` folders in your website base directory. Also ensure the `PHP` directory is in same path.
    *   Create the `json` folder in your website base directory with json files.
     *  Ensure `navBar` folder is placed correctly in the website base directory with navbar code.
    *   Make sure the PHP folder contains a `config.json` file with your database credentials.
2.  **Database Setup:**
    *   The database will be created automatically with tables.
    *   Add database credentials to `config.json` file in `PHP` directory
3.  **Access your website**: Open your `index.html` file.
    *You can create two separate files one for premium commands and other for profile page


## Available Commands

The bot includes a range of commands in categorized form. To see the list of command in the bot use `/help` command in discord channel.

## Contributing

If you'd like to contribute to Spoty, feel free to fork the repository and submit a pull request.

## License

    SEM-6 Project Spoty
    Copyright (C) 2025  Darshit Limbad

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Contact

For any questions or feedback, feel free to reach out at Nowhere -_-.