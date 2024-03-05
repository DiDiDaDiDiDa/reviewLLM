from prompt import output_format_detail, prompt_ex

examples = """
便宜的套餐：{"sort":{"ordering"="ascend","value"="price"}}
有没有不限流量的：{"data":{"operator":"==","value":"无上限"}}
流量大的：{"sort":{"ordering"="descend","value"="data"}}
100G以上流量的套餐最便宜的是哪个：{"sort":{"ordering"="ascend","value"="price"},"data":{"operator":">=","value":100}}
月费不超过200的：{"price":{"operator":"<=","value":200}}
就要月费180那个套餐：{"price":{"operator":"==","value":180}}
经济套餐：{"name":"经济套餐"}
"""

input_text = "有没有便宜的套餐"
input_text = "有没有土豪套餐"
# input_text = "办个200G的套餐"
# input_text = "有没有流量大的套餐"
# input_text = "200元以下，流量大的套餐有啥"
input_text = "你说那个10G的套餐，叫啥名字"

# 有了例子
prompt = f"""
{output_format_detail.instruction}

{output_format_detail.output_format}

例如：
{examples}

用户输入：
{input_text}

"""

response = prompt_ex.get_completion(prompt)
print(response)
