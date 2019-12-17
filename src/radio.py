import requests
import json
import re


class RadioJavan:
    def __init__(self, url):
        self.url = url

    def scrap(self):
        media_content = re.split(r'/', self.url)[4]
        id_file = re.split(r'/', self.url)[5]
        file_name = re.split(r'([?]([^\n]+))', id_file)[0]

        session = requests.Session()
        if media_content == "mp3":
            host_url = session.get("https://www.radiojavan.com/mp3s/mp3_host/?id={}".format(file_name))
            final_url = str(json.loads(host_url.text)['host']) + "/media/mp3/" + file_name + ".mp3"
            return final_url, file_name
        else:
            return None, None
