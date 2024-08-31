from flask import Request
import hashlib
import uuid
import asyncio
import time
import reply
import receive
from media import Media 
from zhipu import LLM
class Handle(object):
    def GET(self, request: Request):
        try:
            # data = web.input()
            data = request.args
            if len(data) == 0:
                return "hello, this is handle view"
            # signature = data.signature
            # timestamp = data.timestamp
            # nonce = data.nonce
            # echostr = data.echostr
            signature = data.get('signature')
            timestamp = data.get('timestamp')
            nonce = data.get('nonce')
            echostr = data.get('echostr')
            token = "DjrCSEGsNPiW2hE9gwiKOFOhiwDJRBrz" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            print(list)
            sha1 = hashlib.sha1()
            #2x
            #map(sha1.update, list)
            #3x
            sha1.update("".join(list).encode("utf-8"))
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except (Exception, Argument):
            return Argument
    def POST(self, request: Request):
        try:
            # webData = web.data()
            print(request.values)
            webData = request.values.get('input')
            print("Handle Post webdata is ", webData)
            #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Content 
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'voice':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                mediaId16K = recMsg.MediaId16K
                myMedia = Media()
                accessToken = "83_RuKme4gvs1Am_p5EyJjoXWFm4cWXJkPGmrJeAfXejyu3XSHyPTSAODJmb7y9oA7hto-oVLt1Xo-gUrZKCUZ4ByuUBzFj2KimhxDUWs7rE2qahaTcRGkRLVy6m-IHGReAEAPOZ"
                fileName = myMedia.get(accessToken, mediaId16K)
                print(fileName)
                voiceId=str(uuid.uuid4())
                myMedia.uploadForReco(accessToken, fileName, voiceId)
                recog = myMedia.getCompleteReco(accessToken, voiceId)
                print(recog)
                
                # llm = LLM()
                # msg = llm.syncCompletion(recog)
                # replyMsg = reply.TextMsg(toUser, fromUser, msg)
                replyMsg = reply.TextMsg(toUser, fromUser, recog)
                # asyncio.set_event_loop(asyncio.new_event_loop())
                # loop = asyncio.get_event_loop()  # 尝试获取当前事件循环

                # loop.run_until_complete(replyMsg.sendToUserWithText(accessToken=accessToken, toUser=toUser, content="Hello, world"))
                return replyMsg.send()
                # return ""
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'image':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                mediaId = recMsg.MediaId
                replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                return replyMsg.send()
            else:
                print("暂且不处理")
                return "success"
        except (Exception, Argment):
            return Argment
