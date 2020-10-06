import requests
import json


class webhook:
    def __init__(self, url=None, text=None, username='robot-xxx', icon_emoji=':robot_face:', link_names=1):
        self.__url = url
        self.__text = text
        self.__username = username
        self.__icon_emoji = icon_emoji
        self.__link_names = link_names

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def icon_emoji(self):
        return self.__icon_emoji

    @icon_emoji.setter
    def icon_emoji(self, icon_emoji):
        self.__icon_emoji = icon_emoji

    def post_json(self):
        in_argument_err = False
        if self.url is None:
            in_argument_err = True
            print('urlを設定してください')
        if self.text is None:
            in_argument_err = True
            print('textを設定してください')

        if in_argument_err:
            exit()

        requests.post(self.url, data=json.dumps({
            'text': self.text,  # 通知内容
            'username': self.username,  # ユーザー名
            'icon_emoji': self.icon_emoji,  # アイコン
            'link_names': self.__link_names,  # 名前をリンク化
        }))
