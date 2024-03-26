import uuid, defined
from langfuse.client import Langfuse


# 创建一个新trace
def create_trace(user_id):
    langfuse = Langfuse()
    # 创建一个不重复的 id
    trace_id = str(uuid.uuid4())
    trace = langfuse.trace(
        name="agiclass_assistant",
        id=trace_id,
        user_id=user_id
    )
    return trace


# 主流程
def verify_question(
        question: str,
        outlines: str,
        question_list: list,
        user_id: str,
) -> bool:
    trace = create_trace(user_id)
    handler = trace.get_langchain_handler()
    # 判断是否需要回答
    if defined.chain1.invoke(
            {"user_input": question, "outlines": outlines},
            config={"callbacks": [handler]}
    ) == 'Y':
        # 判断是否为重复问题
        if defined.chain2.invoke(
                {"user_input": question, "question_list": "\n".join(question_list)},
                config={"callbacks": [handler]}
        ) == 'N':
            question_list.append(question)
            return True
    return False


# 实际调用
ret = verify_question(
    # "LangChain和SK哪个好用",
    "LangChain支持Java吗",
    defined.outlines,
    defined.question_list,
    user_id="wzy",
)
print(ret)
