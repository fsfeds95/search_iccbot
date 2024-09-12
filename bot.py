import requests
from telegram import Update, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackContext, InlineQueryResultArticle
from telegram.ext import Filters

API_KEY = '74dc824830c7f93dc61b03e324070886'
BOT_TOKEN = '7299943772:AAFMZ8yI9RVwpG9GNXQBpZsMJTRW0S05kCM'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('¡Hola! Usa el buscador inline para encontrar películas.')

def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return

    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=es-ES&query={query}')
    results = response.json().get('results', [])

    articles = []
    for movie in results:
        title = movie['title']
        backdrop = f"https://image.tmdb.org/t/p/w500{movie['backdrop_path']}"
        articles.append(InlineQueryResultArticle(
            id=movie['id'],
            title=title,
            thumb_url=backdrop,
            input_message_content=InputTextMessageContent(
                f"![Backdrop]({backdrop})\n**{title}** ({movie['release_date'][:4]})\n"
                f"**Título original:** {movie['original_title']}\n"
                f"**Idioma original:** {movie['original_language']}\n"
                f"**Duración:** {movie['runtime']} min\n"
                f"**Géneros:** {', '.join([genre['name'] for genre in movie['genre_ids']])}\n"
                f"**Sinopsis:** {movie['overview']}"
            )
        ))

    update.inline_query.answer(articles)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(InlineQueryHandler(inline_query))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
