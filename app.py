import json
import requests
from flask import Flask
from flask import request

app = Flask(__name__)

TOKEN = *


def upload_sticker(sticker_url):  # загружаем стикер в Основу
    response = requests.post(
        url='https://api.tjournal.ru/v1.6/uploader/extract',
        data={'url': sticker_url}
    )
    print(response.json())
    sticker = json.dumps(response.json()['result'])
    return sticker


def send_comment(post_id, parent_id, sticker):  # отправляем коммент со стикером
    try:
        response = requests.post(
            url='https://api.tjournal.ru/v1.6/comment/add',
            headers={'X-Device-Token': TOKEN},
            data={'id': post_id,
                  'reply_to': parent_id,
                  'text': '',
                  'attachments': sticker
                  }
        )
        print(response.json())
        return response.json()['result']['id'], response.json()['result']['text']

    except requests.exceptions.RequestException as e:
        return f'Exception {e}'


def detect_sticker(text):  # определяем наличие и номер стикера
    sticker = None
    flag = False
    stickers_text = ['[no thanks]', None, None, None, None, None, None, None,
                     '[look]', '[tired]', '[feed]', None, None, None, '[evil]', None,
                     '[lick]', '[huy]', '[scream]', None, '[stare]', '[wake]', '[stop]', None,
                     '[hell]', None, '[wink]', None, '[hole]', '[bad trip]', '[oh shit]', '[awesome]',
                     None, None, None, None, '[rasta]', '[i\'m stupid]', '[bye]', '[sleep]',
                     '[aaa]', '[let\'s party]', '[u sure?]', None, '[all right]', '[bowl]', '[tie]',
                     '[two chairs]', '[aww]', '[all is bad]', None, '[autism]', '[knife]', '[vroom]',
                     '[santa]', '[zapoy]', '[blep]', None, '[wat]', '[omg]', None, '[boyan]', '[party]',
                     '[narco]', '[evolution]', '[space]', '[ty pidor]', None, '[new year]',
                     '[what have u done]', '[jeez]', '[u sick]', '[holodno]', '[panda]',
                     '[ment]', '[triggered]', '[amazing]', '[kukusiki]',
                     '[why]', '[mda]']
    stickers_emoji = ['[🤐]', '[😖]', '[🤓]', '[😕]', '[😐]', '[👻]', '[😱]', '[😔]',
                      '[😘]', '[✍️]', '[🍔]', '[😓]', '[👽]', '[👀]', '[🌒]', '[😪]',
                      '[😍]', '[😋]', '[😫]', '[😢]', '[😳]', '[😴]', '[⛔]', '[😲]',
                      '[💀]', '[🙀]', '[😉]', '[😟]', '[💩]', '[🍄]', '[🌑]', '[👍]',
                      '[👎]', '[🤕]', '[😚]', '[😦]', '[🚬]', '[🙆‍️]', '[👋]', '[💤]',
                      '[🙄]', '[🎉]', '[😭]', '[😏]', '[✌️]', '[🏆]', '[👔]', '[🤔]',
                      '[❤️]', '[😑]', '[😼]', '[👤]', '[🔪]', '[🚗]', '[🎅]', '[🍾]',
                      '[💋]', '[☹️]', '[❓]', '[😰]', '[😒]', '[🎹]', '[💃]', '[🚨]',
                      '[🦍]', '[🚀]', '[🌈]', '[🌝]', '[🎄]', '[😩]', '[✝️]', '[🚑]',
                      '[❄️]', '[🐼]', '[👮‍️]', '[😡]', '[🆒]', '[💕]', '[🗞]', '[💔]']

    for idx, val in enumerate(stickers_text):
        if val is not None:
            if text.find(val) != -1:
                flag = True
                sticker = idx

    for idx, val in enumerate(stickers_emoji):
        if text.find(val) != -1:
            flag = True
            sticker = idx

    if flag:
        return sticker
    else:
        return None


def get_sticker(sticker_id):  # получаем json стикера
    filename = str(sticker_id) + '.png'
    sticker_url = 'http://pavero.fvds.ru/ave-gosha/' + filename
    sticker = upload_sticker(sticker_url)
    return sticker


@app.route('/', methods=['POST'])
def process_comment():
    if not request.is_json:
        raise Exception(f'Wrong response')

    json_data = request.get_json()
    if json_data['data']['text'] is None:
        raise Exception(f'No text')
    text = json_data['data']['text']

    post_id = json_data['data']['content']['id']

    if json_data['data']['reply_to'] is None:
        parent_id = None
    else:
        parent_id = json_data['data']['reply_to']['id']

    sticker_id = detect_sticker(text)
    if sticker_id is not None:
        sticker = get_sticker(sticker_id)
        send_comment(post_id, parent_id, sticker)

    return 'OK'


@app.route('/hello')
def hello():
    return "hello world"


if __name__ == '__main__':
    app.run()
