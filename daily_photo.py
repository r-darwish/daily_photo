import random
import telegram
import os

def _get_photo_path():
    directory = os.environ["DAILY_PHOTO_DIRECTORY"]
    return os.path.join(directory, random.choice(os.listdir(directory)))

def main():
    photo_path = _get_photo_path()
    chat_id = os.environ["DAILY_PHOTO_CHAT_ID"]
    bot = telegram.Bot(token=os.environ["DAILY_PHOTO_BOT_TOKEN"])

    with open(photo_path, "rb") as f:
        bot.send_photo(chat_id=chat_id, photo=f)

    os.unlink(photo_path)

if __name__ == '__main__':
    main()
