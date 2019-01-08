import io
import os
import random
import sentry_sdk
import telegram
from PIL import Image, ExifTags

_PHOTO_SIZE_LIMIT = 10 * 1024 ** 2


def _get_resized_photo(path):
    image = Image.open(path)
    image.thumbnail((1080, 1080))

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            exif = dict(image._getexif().items())

            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)

            break

    fp = io.BytesIO()
    image.save(fp, format="jpeg")
    fp.seek(0)
    return fp


def _get_photo_path():
    directory = os.environ["DAILY_PHOTO_DIRECTORY"]
    return os.path.join(directory, random.choice(os.listdir(directory)))


def main():
    sentry_sdk.init(os.environ.get("DAILY_PHOTO_SENTRY_DSN"))
    photo_path = _get_photo_path()
    chat_id = os.environ["DAILY_PHOTO_CHAT_ID"]
    bot = telegram.Bot(token=os.environ["DAILY_PHOTO_BOT_TOKEN"])

    bot.send_photo(chat_id=chat_id, photo=_get_resized_photo(photo_path), timeout=180)

    os.unlink(photo_path)


if __name__ == '__main__':
    main()
