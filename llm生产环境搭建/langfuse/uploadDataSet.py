# -*- coding: utf-8 -*-
import env_reload
import json
from langfuse import Langfuse
from langfuse.model import CreateDatasetRequest, CreateDatasetItemRequest
from tqdm import tqdm

# 调整数据格式 {"input":{...},"expected_output":"label"}
data = []
with open('./my_annotations.jsonl', 'r') as fp:
    for line in fp:
        example = json.loads(line.strip())
        item = {
            "input": {
                "outlines": example["outlines"],
                "user_input": example["user_input"]
            },
            "expected_output": example["label"]
        }
        data.append(item)


# init
langfuse = Langfuse()

# 创建数据集，如果已存在不会重复创建
langfuse.create_dataset(name="assistant-data")

# 考虑演示运行速度，只上传前50条数据
for item in tqdm(data[:50]):
    langfuse.create_dataset_item(
        dataset_name="assistant-data",
        input=item["input"],
        expected_output=item["expected_output"]
    )
