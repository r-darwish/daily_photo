import io
import os
from random import choices
import datetime
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

            orientation_value = exif.get(orientation)

            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)

            break

    fp = io.BytesIO()
    image.save(fp, format="jpeg")
    fp.seek(0)
    return fp


def _weight(f):
    capture = datetime.datetime.strptime(Image.open(f)._getexif()[36867], '%Y:%m:%d %H:%M:%S')
    return ((datetime.datetime.now() - capture).days + 1) ** 0.4


def _get_photo_path():
    directory = os.environ["DAILY_PHOTO_DIRECTORY"]
    files = [os.path.join(directory, p) for p in os.listdir(directory)]
    weights = [_weight(f) for f in files]
    return choices(files, weights=weights)[0]


def main():
    sentry_sdk.init(os.environ.get("DAILY_PHOTO_SENTRY_DSN"))
    photo_path = _get_photo_path()
    chat_id = os.environ["DAILY_PHOTO_CHAT_ID"]
    bot = telegram.Bot(token=os.environ["DAILY_PHOTO_BOT_TOKEN"])

    bot.send_photo(chat_id=chat_id, photo=_get_resized_photo(photo_path), timeout=180)

    os.unlink(photo_path)


if __name__ == '__main__':
    main()
