import requests
import slack

import configuration

url = "https://emoji-gen.ninja/emoji_download"
params = {'align': "center",
          'back_color': "00000000",
          'color': "EC71A1FF",
          'font': "gensenmarugothic_tw_ttf_bold",
          'locale': "zh-Hant",
          'public_fg': "true",
          'size_fixed': "false",
          'stretch': "false",
          'text': ""
}
token = configuration.user_token
client = slack.WebClient(token=token)
filename = "data/tmp_emojiword.jpg"


def imageDownload(url, params):
    r = requests.get(url, params=params, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        raise ValueError("Cannot download")


def emojiUpload(name, text):
    params['text'] = text
    imageDownload(url, params)

    # upload to slack emoji
    response = client.api_call(
            "emoji.add",
            data={
                'name': name,
                'mode': 'data'},
            files={'image': filename})
    assert(response["ok"])


if __name__ == "__main__":
    emojiUpload("no", "不")
