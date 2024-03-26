# -*- coding: utf-8 -*-
import env_reload
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 定义语言模型
llm = ChatOpenAI()

# 定义Prompt模板
prompt = PromptTemplate.from_template("Say hello to {input}!")

# 定义输出解析器
parser = StrOutputParser()

chain = (
    {"input":RunnablePassthrough()}
    | prompt
    | llm
    | parser
)

print(chain.invoke("AGIClass"))