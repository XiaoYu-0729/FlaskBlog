# encoding:utf-8
from openai import OpenAI

BASE_URL = 'https://api.minimaxi.com/v1'
API_KEY = 'sk-cp-Ng7Lqc87wwJkFagZIWbAYe5VqZZ3S65Bsn42tX0vSrRm8y9j-VCBl7qOs7P9DVqArD7wieRfm6LzaW3VAbJDmGPFXpngIx0QdjhodINTJj6fuj1gboSbzk8'

# 获取智能体回复
def get_agent_info(content, sys_content):
    # 创建 OpenAI 对象
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    # 创建 ChatCompletion 对象
    response = client.chat.completions.create(
        model='MiniMax-M2.7',
        messages=[  # type: ignore
            {"role": "system", "content": sys_content},
            {"role": "user", "content": content},
        ],
        # 设置 reasoning_split=True 将思考内容分离到 reasoning_details 字段
        extra_body={"reasoning_split": True},
    )
    text = response.choices[0].message.content
    # print(f"Thinking:\n{response.choices[0].message.reasoning_details[0]['text']}\n")
    print(f"智能体回复:\n{text}\n")
    return text