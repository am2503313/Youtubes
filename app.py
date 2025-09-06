from flask import Flask, request
import telebot
import yt_dlp

API_TOKEN = "7403439406:AAHjiW-mA2VStoXbeBa2qMpX7QyqUYHUW3M"
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://your-pella-app-url/" + API_TOKEN)
    return "Webhook set!", 200

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Send me a YouTube link and I'll download it for you! 🎥")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        bot.send_message(message.chat.id, "⏳ Downloading your video...")
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            with open("video.mp4", "rb") as video:
                bot.send_video(message.chat.id, video)
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Error: {e}")
    else:
        bot.send_message(message.chat.id, "Please send a valid YouTube link.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
