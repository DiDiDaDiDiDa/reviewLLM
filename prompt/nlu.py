# 任务描述
from prompt import prompt_ex

instruction = """
你的任务是识别用户对手机流量套餐产品的选择条件。

每种流量套餐产品包含三个属性：名称，月费价格，月流量。

根据用户输入，识别用户在上述三种属性上的倾向。
"""

# 用户输入
input_text = """
办个100G的套餐。
"""

# prompts 模版。instruction 和 input_text 会被替换为上面的内容
prompt = f"""
{instruction}

用户输入：
{input_text}
"""

# 调用大模型
# response = prompt_ex.get_completion(prompts)
# print(response)
