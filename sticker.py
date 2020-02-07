from pprint import pprint
import requests
import configuration
import random


def imageSearch(keyword):
    """
    Google search image url.

    The parameters are shown in https://developers.google.com/custom-search/v1/cse/list
    """
    isgif = keyword.endswith('.gif')
    # keyword = keyword[:keyword.rfind(".")]
    resp = requests.get("https://www.googleapis.com/customsearch/v1", params={
            'q': keyword,
            'num': 5,
            'hl': "zh-TW",
            # 'lr': "lang_zh-TW",
            'searchType': 'image',
            'fileType':  'gif' if isgif else None,
            'cx': configuration.search_cx,
            'key': configuration.search_key,
            'safe': "medium",
            },
            headers={'Accept': "application/json"})
    data = resp.json()
    items = data.get('items')
    print(keyword)
    pprint(items)
    links = [item for item in items if item["mime"] not in ["image/", "image/webp"]]
    # random.shuffle(links) 
    link = random.choice(links)

    if requests.get(link['link']).status_code == 200:
        return link['link']
    else:
        return link['image']['thumbnailLink']
    # raise ValueError("Cannot search good image")


def imageDownload(url, path):
    """Download image from url"""
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def imageBlock(keyword, path):
    """Construct slack block format"""
    print(keyword, path)
    return [{
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": keyword,
                },
                "image_url": path,
                "alt_text": keyword
            }]


if __name__ == "__main__":
    # testing
    import slack
    token = configuration.token
    client = slack.WebClient(token=token)
    channel_id = configuration.channel_testing

    keyword = "jojo.jpg"
    # keyword = "我就爛.jpg"
    url = imageSearch(keyword)
    """
    blocks = imageBlock(keyword, url)
    response = client.chat_postMessage(
                   channel=channel_id,
                   blocks=blocks)
    pprint(response["message"])
    """
