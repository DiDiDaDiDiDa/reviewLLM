import uuid, defined
from langfuse.client import Langfuse


# ����һ����trace
def create_trace(user_id):
    langfuse = Langfuse()
    # ����һ�����ظ��� id
    trace_id = str(uuid.uuid4())
    trace = langfuse.trace(
        name="agiclass_assistant",
        id=trace_id,
        user_id=user_id
    )
    return trace


# ������
def verify_question(
        question: str,
        outlines: str,
        question_list: list,
        user_id: str,
) -> bool:
    trace = create_trace(user_id)
    handler = trace.get_langchain_handler()
    # �ж��Ƿ���Ҫ�ش�
    if defined.chain1.invoke(
            {"user_input": question, "outlines": outlines},
            config={"callbacks": [handler]}
    ) == 'Y':
        # �ж��Ƿ�Ϊ�ظ�����
        if defined.chain2.invoke(
                {"user_input": question, "question_list": "\n".join(question_list)},
                config={"callbacks": [handler]}
        ) == 'N':
            question_list.append(question)
            return True
    return False


# ʵ�ʵ���
ret = verify_question(
    # "LangChain��SK�ĸ�����",
    "LangChain֧��Java��",
    defined.outlines,
    defined.question_list,
    user_id="wzy",
)
print(ret)
