from dotenv import load_dotenv
import os
import telebot
import pytube
import threading


load_dotenv()
bot = telebot.TeleBot(os.environ['TG_TOKEN'])


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я тебе помогу скачать видео с YouTube. Просто отправь ссылку на видео и я отправлю тебе файл')


@bot.message_handler(content_types=['text'])
def download(message):
    link = message.text
    try:
        youtube = pytube.YouTube(link)
    except pytube.exceptions.RegexMatchError:
        bot.send_message(message.chat.id, '‼️ Внимание! Проверь правильность ссылки! Не удалось найти видео')
        return
    message_id = bot.send_message(message.chat.id, f'Найдено видео: "{youtube.title}"! Начинаю загрузку. Это может занять некоторое время....')
    video = youtube.streams.filter(progressive=True).desc().first()
    video.download('video', filename=f'{message.chat.id}_{youtube.title}.mp4')
    bot.edit_message_text('Ниже скаченное видео! Спасибо за использование бота! Если что, обращайтесь:)',  chat_id=message.chat.id, message_id=message_id.message_id)
    bot.send_video(
        message.chat.id,
        open(f'video/{message.chat.id}_{youtube.title}.mp4', 'rb').read(),
        message_thread_id=message_id
    )
    os.remove(f'video/{message.chat.id}_{youtube.title}.mp4')


threading.Thread(target=bot.polling).start()