# 输出格式
from prompt import nlu, prompt_ex

output_format = """
以 JSON 格式输出
"""

# 稍微调整下咒语，加入输出格式
prompt = f"""
{nlu.instruction}

{output_format}

用户输入：
{nlu.input_text}
"""

# 调用大模型
# response = prompt_ex.get_completion(prompt)
# print(response)
