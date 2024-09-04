from celery import chain
from flask import Blueprint, request
from src.service.wx_access_token import get_access_token_from_cache
from src.service.wx_media import wx_media_get_byid, wx_voice_addvoicetorecofortext, get_complete_voice_reco 
from src.service.zhipu import LLM
from src.service.summary import get_by_userid
from src.worker import task
from src.worker.wx_task import get_reco_task
from src.worker.llm_task import summarize_content
from src.worker.summary_task import save_by_userid_task
from src.utils import reply
from src.utils import receive

import hashlib
import uuid


wx_blueprint = Blueprint('wx_blueprint', __name__, url_prefix="/wx")

wx_get_token = "DjrCSEGsNPiW2hE9gwiKOFOhiwDJRBrz" #请按照公众平台官网\基本配置中信息填写
wx_access_token = "84_9xZshOOZrE9NGlclI99FPrWWuHgvmzmUipiugNvNZFyAXEwgAi5k2cJW_nbqxNb_wJL9PDbWlAZg8P2NH62fURLUMorEjD-sRP-W0gppsEsO2oq_xEm4vvCa9NQBRBcAFAOEO"

@wx_blueprint.route('', methods=['GET'])
def wxGet():
    try:
        data = request.args
        if len(data) == 0:
            return "wx handle get with no signature, no timestamp, no nonce and no echostr."
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        token = wx_get_token

        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()

        sha1.update("".join(list).encode("utf-8"))
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
        if hashcode == signature:
            return echostr
        else:
            return ""
    except Exception as inst:
        return inst.args

@wx_blueprint.route('', methods=['POST'])
def wxPOST():
    print(request)
    ttask = task.test_task.delay(10, 20)
    print(ttask)
    # res = test_task.AsyncResult(task.id)
    # print(res)
    try:
        # webData = web.data()
        webData = request.data
        print("Handle Post webdata is ", webData)
        #后台打日志
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = recMsg.Content
            rep = bytes(content).decode()
            if bytes(content).decode() == "#总结":
                rep_list = map(lambda x: bytes(x).decode(), get_by_userid(toUser))
                rep = "\n".join(rep_list)
            replyMsg = reply.TextMsg(toUser, fromUser, rep)
            return replyMsg.send()
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'voice':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            mediaId16K = recMsg.MediaId16K
            accessToken = get_access_token_from_cache()
            print(accessToken)
            fileName = wx_media_get_byid(accessToken, mediaId16K)
            print(fileName)
            voiceId=str(uuid.uuid4())
            wx_voice_addvoicetorecofortext(accessToken, fileName, voiceId)

            task_chain = chain(get_reco_task.s(accessToken, voiceId), summarize_content.s(), save_by_userid_task.s(toUser))
            task_chain.apply_async()

            # recog = get_complete_voice_reco(accessToken, voiceId)
            # print(recog)
            
            # llm = LLM()
            # msg = llm.syncCompletion(recog)
            # replyMsg = reply.TextMsg(toUser, fromUser, msg)
            # replyMsg = reply.TextMsg(toUser, fromUser, recog)
            # asyncio.set_event_loop(asyncio.new_event_loop())
            # loop = asyncio.get_event_loop()  # 尝试获取当前事件循环

            # loop.run_until_complete(replyMsg.sendToUserWithText(accessToken=accessToken, toUser=toUser, content="Hello, world"))
            # return replyMsg.send()
            return ""
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'image':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            mediaId = recMsg.MediaId
            replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
            return replyMsg.send()
        else:
            print("暂且不处理")
            return "success"
    except Exception as inst:
        print(inst.args)
        return inst.args