# 导入依赖库
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 加载 .env 文件中定义的环境变量
_ = load_dotenv(find_dotenv())

knowledge=f"""
你是运营商客服，运营商的流量包产品：

名称	流量（G/月）	价格（元/月）	适用人群
经济套餐	10	50	无限制
畅游套餐	100	180	无限制
无限套餐	1000	300	无限制
校园套餐	200	150	在校生
"""
# 初始化 OpenAI 客户端
client = OpenAI()  # 默认使用环境变量中的 OPENAI_API_KEY 和 OPENAI_BASE_URL
# 基于 prompts 生成文本
def get_completion(prompt, model="gpt-3.5-turbo"):      # 默认使用 gpt-3.5-turbo 模型
    messages = [{
        "role": "system",
        "content": knowledge  # 注入新知识
    }, {"role": "user", "content": prompt}]    # 将 prompts 作为用户输入
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,                                  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content          # 返回模型生成的文本