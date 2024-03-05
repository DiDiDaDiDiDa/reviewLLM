## 接口的进化

UI 进化的趋势是：越来越适应人的习惯，越来越自然

1. 命令行，Command Line Interface，简称 CLI（DOS、Unix/Linux shell, Windows Power Shell）

2. 图形界面，Graphical User Interface，简称 GUI（Windows、MacOS、iOS、Android）

3. 语言界面，Conversational User Interface，简称 CUI，或 Natural-Language User Interface，简称 LUI ← **我们在这里**

4. 脑机接口，Brain–Computer Interface，简称 BCI

   ![ui-evolution](images\ui-evolution.png)

## 为什么要大模型连接外部世界？

**大模型两大缺陷：**

1. 并非知晓一切
   1. 训练数据不可能什么都有。垂直、非公开数据必有欠缺
   2. 不知道最新信息。大模型的训练周期很长，且更新一次耗资巨大，还有越训越傻的风险。所以 ta 不可能实时训练。GPT-3.5 的知识截至 2021 年 9 月，GPT-4 是 2023 年 12 月。
2. **没有「真逻辑」**。它表现出的逻辑、推理，是训练文本的统计规律，而不是真正的逻辑，所以有幻觉。

所以：大模型需要连接真实世界，并对接真逻辑系统。
