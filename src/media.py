import urllib.request
import json
import re
import os
import requests
import time
from pydub import AudioSegment

class Media(object):
    def get(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (
            accessToken, mediaId)
        urlResp = urllib.request.urlopen(postUrl)

        headers = dict(urlResp.getheaders())
        print(headers)
        if (headers['Content-Type'] == 'application/json' or headers['Content-Type'] == 'text/plain'):
            jsonDict = json.loads(urlResp.read())
            print(jsonDict)
        else:
            buffer = urlResp.read()  # 素材的二进制
            fileName = 'default.file'
            match = re.search(r'"([^"]+)"', headers['Content-disposition'])
            if match:
                fileName = match.group(1)
                print(fileName)
            with open(fileName, 'wb') as file:
                file.write(buffer)
            # 加载AMR文件
            amr = AudioSegment.from_file(fileName, format="amr")
            # 设置输出的MP3文件名
            file_name_without_extension, _ = os.path.splitext(fileName)
            output_file = file_name_without_extension + ".mp3"

            # 将AMR转换为MP3
            amr.export(output_file, format="mp3")
            print("get successful")
            return output_file
    def uploadForReco(self, accessToken, fileName, voiceId):
        with open(fileName, 'rb') as file:
            openFile = file.read()
            param = {'media': openFile}
            postUrl = "https://api.weixin.qq.com/cgi-bin/media/voice/addvoicetorecofortext?access_token=%s&format=mp3&voice_id=%s&lang=zh_CN" % (accessToken, voiceId)
            print(postUrl)
            response = requests.post(postUrl, files=param)
            print(response.text)

    def getReco(self, accessToken, voiceId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/voice/queryrecoresultfortext?access_token=%s&voice_id=%s&lang=zh_CN" % (accessToken, voiceId)
        print(postUrl)
        response = requests.post(postUrl)
        response.encoding = "utf-8"
        print(response.text)
        jsonDict = json.loads(response.text)
        return jsonDict
    
    def getCompleteReco(self, accessToken, voiceId):
        result = self.getReco(accessToken, voiceId)
        while not result["is_end"]:
            time.sleep(0.5)
            result = self.getReco(accessToken, voiceId)
        return result["result"]
