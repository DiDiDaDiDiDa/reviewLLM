import os
from dotenv import load_dotenv, find_dotenv
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain
from langchain_core.prompts import ChatPromptTemplate

_ = load_dotenv(find_dotenv())  # read local .env file

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
# prompt template 1
first_prompt = ChatPromptTemplate.from_template(
    "描述生产{product}的公司的一个最佳名称是什么？"
)

# Chain 1
chain_one = LLMChain(llm=llm, prompt=first_prompt,verbose=True)

# prompt template 2
second_prompt = ChatPromptTemplate.from_template(
    "为以下公司编写 20 个字的描述：{company_name}”"
)
# chain 2
chain_two = LLMChain(llm=llm, prompt=second_prompt,verbose=True)

# 将chain1和chain2组合在一起生成一个新的chain.
overall_simple_chain = SimpleSequentialChain(chains=[chain_one, chain_two],
                                             verbose=True)
# product = "床上用品"
# 执行新的chain
result = overall_simple_chain.invoke({"input": "床上用品"})
print(result)
