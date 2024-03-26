
from langfuse.callback import CallbackHandler
import env_reload


from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough


handler = CallbackHandler(
    trace_name="SayHello",
    user_id="wzy",
)

model = ChatOpenAI(model="gpt-3.5-turbo-0613")

prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template("Say hello to {input}!")
])

# 定义输出解析器
parser = StrOutputParser()

chain = (
        {"input": RunnablePassthrough()}
        | prompt
        | model
        | parser
)

result = chain.invoke(input="AGIClass", config={"callbacks": [handler]})

print(result)
