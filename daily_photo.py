import random
import telegram
import os
import io
from PIL import Image

_PHOTO_SIZE_LIMIT = 10 * 1024 ** 2

def _get_resized_photo(path):
    image = Image.open(path)
    image.thumbnail((1280, 720))

    fp = io.BytesIO()
    image.save(fp, format="jpeg")
    fp.seek(0)
    return fp


def _get_photo_path():
    directory = os.environ["DAILY_PHOTO_DIRECTORY"]
    return os.path.join(directory, random.choice(os.listdir(directory)))


def main():
    photo_path = _get_photo_path()
    chat_id = os.environ["DAILY_PHOTO_CHAT_ID"]
    bot = telegram.Bot(token=os.environ["DAILY_PHOTO_BOT_TOKEN"])

    bot.send_photo(chat_id=chat_id, photo=_get_resized_photo(photo_path))

    os.unlink(photo_path)

if __name__ == '__main__':
    main()
