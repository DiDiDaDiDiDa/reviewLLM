# -*- coding: utf-8 -*-
import env_reload
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    AIMessage,  # 等价于OpenAI接口中的assistant role
    HumanMessage,  # 等价于OpenAI接口中的user role
    SystemMessage  # 等价于OpenAI接口中的system role
)
from langfuse.callback import CallbackHandler

llm = ChatOpenAI(model_name="gpt-3.5-turbo")

messages = [
    SystemMessage
    (content="你是AGIClass的课程助理。"),
]
handler = CallbackHandler(
    user_id="wzy",
    session_id="my_chat_session"
)
while True:
    user_input = input("User:")
    if user_input.strip() == "":
        break
    messages.append(HumanMessage(content=user_input))
    response = llm.invoke(messages, config={"callbacks": [handler]})
    print("AGIClass:", response.content)
    messages.append(AIMessage(response.content))
