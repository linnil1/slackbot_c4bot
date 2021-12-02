import os
import re
import copy
import aiohttp
from slack_sdk.web.async_client import AsyncWebClient

import configuration


class Emoji:
    """
    Create a pretty work image as emoji
    """
    url = "https://emoji-gen.ninja/emoji_download"
    url_params = {
        'align': "center",
        'back_color': "00000000",
        'color': "EC71A1FF",
        'font': "gensenmarugothic_tw_ttf_bold",
        'locale': "zh-Hant",
        'public_fg': "true",
        'size_fixed': "false",
        'stretch': "false",
    }
    rename_style = "bot-{}"
    folder = "emojis/"
    image_format = ".jpg"
    client_user = AsyncWebClient(token=configuration.user_token)
    client = AsyncWebClient(token=configuration.token)

    def __init__(self, name, word):
        """ 
        Parameter:
          name(str): filename-like string
          word(str): The text you want to generate, 
        """
        if not re.match(r"^\w+$", name):
            raise ValueError(f"Bad Name: {name}")

        self.name = self.rename_style.format(name)
        self.fname = os.path.join(self.folder, self.name) + self.image_format
        self.word = word
        os.makedirs(self.folder, exist_ok=True)

    async def imageDownload(self):
        """ Download image of the word """
        print(f"Download {self.word}...")
        self.params = copy.deepcopy(self.url_params)
        self.params['text'] = self.word
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as resp:
                with open(self.fname, 'wb') as fd:
                    async for chunk in resp.content.iter_chunked(128):
                        fd.write(chunk)
        return True

    async def emojiUpload(self):
        """ upload to slack emoji """
        print(f"Upload {self.name}(self.word)...")
        response = await self.client_user.api_call(
            "emoji.add",
            data={
                'name': self.name,
                'mode': 'data',
                '_x_reason': "customize-emoji-add",
                '_x_mode': "online",
            },
            headers={"Cookie": configuration.cookie},
            files={'image': self.fname})
        print(response)
        return True

    async def isExist(self):
        return os.path.exists(self.fname)

    async def isUpload(self):
        response = await self.client.emoji_list() 
        emojis = response.data['emoji']
        return self.name in emojis.keys()

    async def upload(self, force=False):
        """ Run all the function """
        if force or not await self.isExist():
            await self.imageDownload()
        if force or not await self.isUpload():
            await self.emojiUpload()


if __name__ == "__main__":
    # test
    import asyncio
    a = Emoji("broken", "壞了")
    asyncio.run(a.upload(force=True))
