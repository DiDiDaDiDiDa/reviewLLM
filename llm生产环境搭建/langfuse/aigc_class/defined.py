# -*- coding: utf-8 -*-
import env_reload
# 构建 PromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough


need_answer = PromptTemplate.from_template("""
*********
你是AIGC课程的助教，你的工作是从学员的课堂交流中选择出需要老师回答的问题，加以整理以交给老师回答。

课程内容:
{outlines}
*********
学员输入:
{user_input}
*********
如果这是一个需要老师答疑的问题，回复Y，否则回复N。
只回复Y或N，不要回复其他内容。""")

check_duplicated = PromptTemplate.from_template("""
*********
已有提问列表:
[
{question_list}
]
*********
新提问:
{user_input}
*********
已有提问列表是否有和新提问类似的问题? 回复Y或N, Y表示有，N表示没有。
只回复Y或N，不要回复其他内容。""")

outlines="""
LangChain
模型 I/O 封装
模型的封装
模型的输入输出
PromptTemplate
OutputParser
数据连接封装
文档加载器：Document Loaders
文档处理器
内置RAG：RetrievalQA
记忆封装：Memory
链架构：Chain/LCEL
大模型时代的软件架构：Agent
ReAct
SelfAskWithSearch
LangServe
LangChain.js
"""

question_list=[
    "LangChain可以商用吗",
    "LangChain开源吗",
]
# 创建 chain
model = ChatOpenAI(temperature=0,model_kwargs={"seed":42})
parser = StrOutputParser()

chain1 = (
    need_answer
    | model
    | parser
)

chain2 = (
    check_duplicated
    | model
    | parser
)