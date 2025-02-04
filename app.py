from bailey import Bailey
import logging
import os
from dotenv import load_dotenv
from messageHandler import handle_text_message, handle_attachment, handle_text_command

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)

# Initialize WhatsApp bot
bot = Bailey(
    port=int(os.getenv("PORT", 8000)),
    host=os.getenv("HOST", "0.0.0.0"),
    debug=os.getenv("DEBUG", "True") == "True"
)

logging.info("KORA AI WhatsApp Bot is now running...")

# Handle text messages
@bot.event
def on_message(message):
    if message.type == "text":
        logging.info(f"Received message from {message.chat_id}: {message.text}")
        response = handle_text_message(message.text, [])
        message.reply(response)
    elif message.type in ["image", "file"]:
        media_url = message.media_url
        file_extension = message.file_extension
        message_type = message.type
        response = handle_attachment(media_url, message_type, file_extension)
        message.reply(response)

# Handle commands using buttons (you'll customize CMD functions later)
@bot.command
def cmd_handler(command, args):
    logging.info(f"Received command: /{command} {args}")
    response = handle_text_command(command, args)
    return response

# Example buttons
@bot.command
def menu():
    buttons = [
        {"id": "button1", "title": "📚 Get Info"},
        {"id": "button2", "title": "📊 Stats"},
        {"id": "button3", "title": "💡 Tips"}
    ]
    return {"text": "Select an option:", "buttons": buttons}

@bot.button_handler
def on_button_click(button_id):
    if button_id == "button1":
        return "Here’s some information for you 📚."
    elif button_id == "button2":
        return "Here are your stats 📊."
    elif button_id == "button3":
        return "Here’s a useful tip 💡."

# Start the bot
if __name__ == "__main__":
    logging.info("KORA AI Bot is ready. Scan the QR code to activate.")
    bot.run()
