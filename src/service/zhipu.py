from zhipuai import ZhipuAI
class LLM(object):
    def syncCompletion(self, content):
        client = ZhipuAI(api_key="1bc8f78bc82254732f0c86576d36fa3e.dvNx3wdxIQN7jyhB") # 填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4-0520",  # 填写需要调用的模型编码
            messages=[
                {"role": "user", "content": content},
                {"role": "user", "content": "请帮我概括以上内容"},
            ],
        )
        msg = response.choices[0].message.content
        print(msg)
        return msg
