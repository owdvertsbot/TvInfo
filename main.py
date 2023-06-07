import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# Replace with your bot token and TMDb API key
BOT_TOKEN = 'YOUR_BOT_TOKEN'
TMDB_API_KEY = 'YOUR_TMDB_API_KEY'

# Set up the bot
bot = Client(
    "TVShowInfoBot",
    api_id=YOUR_API_ID,
    api_hash="YOUR_API_HASH",
    bot_token=BOT_TOKEN,
)


@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    """Send a welcome message when the bot is started"""
    await message.reply_text("Welcome to the TV Show Information Bot! Use the /show command followed by the name of the TV show to get information.")


@bot.on_message(filters.command("show"))
async def show(_, message: Message):
    """Send TV show information"""
    # Get the name of the TV show from the command arguments
    show_name = ' '.join(message.command[1:])

    # Search for the TV show using the TMDb API
    search_url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={show_name}"
    search_response = requests.get(search_url).json()

    # Check if any results were found
    if search_response['total_results'] == 0:
        await message.reply_text(f"Sorry, I could not find any TV shows with the name '{show_name}'.")
        return

    # Get the first result
    show = search_response['results'][0]

    # Get the show ID and use it to get more detailed information
    show_id = show['id']
    show_url = f'https://api.themoviedb.org/3/tv/{show_id}?api_key={TMDB_API_KEY}'
    show_response = requests.get(show_url).json()

    # Get the show details
    name = show_response['name']
    overview = show_response['overview']
    first_air_date = show_response['first_air_date']
    last_air_date = show_response['last_air_date']
    number_of_seasons = show_response['number_of_seasons']
    number_of_episodes = show_response['number_of_episodes']

    # Get the list of genres
    genres = [genre['name'] for genre in show_response['genres']]

    # Get the list of networks
    networks = [network['name'] for network in show_response['networks']]

    # Get the list of production companies
    companies = [company['name'] for company in show_response['production_companies']]

    # Get the list of seasons
    seasons = [season['name'] for season in show_response['seasons']]

    # Get the poster image URL
    poster_path = show_response['poster_path']
    poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'

    # Create the message text
    message_text = f'*{name}*\n\n{overview}\n\nFirst air date: {first_air_date}\nLast air date: {last_air_date}\nNumber of seasons: {number_of_seasons}\nNumber of episodes: {number_of_episodes}\nGenres: {", ".join(genres)}\nNetworks: {", ".join(networks)}\nProduction companies: {", ".join(companies)}\nSeasons: {", ".join(seasons)}'

    # Send the poster image and message text
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=poster_url,
        caption=message_text,
        parse_mode='Markdown',
    )


# Run the bot
if __name__ == "__main__":
    bot.run()
