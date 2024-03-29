## Prompt 的典型构成

- **角色**：给 AI 定义一个最匹配任务的角色，比如：「你是一位软件工程师」「你是一位小学老师」
- **指示**：对任务进行描述
- **上下文**：给出与任务相关的其它背景信息（尤其在多轮交互中）
- **例子**：必要时给出举例，学术中称为 one-shot learning, few-shot learning 或 in-context learning；实践证明其对输出正确性有很大帮助
- **输入**：任务的输入信息；在提示词中明确的标识出输入
- **输出**：输出的格式描述，以便后继模块自动解析模型的输出结果，比如（JSON、XML）



### 为什么有效

大模型对 prompt 开头和结尾的内容更敏感

先定义角色，其实就是在开头把问题域收窄，减少二义性。

### 自洽性（Self-Consistency）
一种对抗「幻觉」的手段。就像我们做数学题，要多次验算一样。

同样 prompt 跑多次
通过投票选出最终结果