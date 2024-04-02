#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName :scratch_demo.py
# @Time :2024/4/2 15:29
# @Author :WZY
import os

import requests
import torch
import torch.nn as nn
import tiktoken
import pandas as pd

# 检查文件是否存在
if not os.path.exists("sales_textbook.txt"):
    url = ("https://huggingface.co/datasets/goendalf666/sales-textbook_for_convincing_and_selling/resolve/main"
           "/sales_textbook.txt?download=true")
    with open("sales_textbook.txt", "wb") as f:
        f.write(requests.get(url).content)

with open("sales_textbook.txt", "r", encoding="utf-8") as f:
    text = f.read()
    # print(text)

# 第一步，tokenanize化，我们选用openai的tiktoken
encoding = tiktoken.get_encoding("cl100k_base")
tokenized_text = encoding.encode(text)
tokenized_text = torch.tensor(tokenized_text, dtype=torch.long)
# print(len(tokenized_text))

# 训练数据和测试数据 9：1
train_idex = int(len(tokenized_text) * 0.9)
train_data = tokenized_text[:train_idex]
valid_data = tokenized_text[train_idex:]

# 设置超参数
context_len = 16
d_model = 64
batch_size = 4

data = train_data
idxs = torch.randint(low=0, high=len(data) - context_len, size=(batch_size,))
# print(data[idxs[0]])
x_batch = torch.stack([torch.tensor(data[i:i + context_len]) for i in idxs])
y_batch = torch.stack([torch.tensor(data[i + 1:i + context_len + 1]) for i in idxs])
# print(x_batch.shape)
# df=pd.DataFrame(x_batch[0].numpy())
# print(df)
# print(encoding.decode(x_batch[0].numpy()))


# 定义input embedding table
max_token_value = tokenized_text.max().item()
