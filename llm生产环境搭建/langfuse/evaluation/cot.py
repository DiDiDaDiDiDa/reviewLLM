# -*- coding: utf-8 -*-
import uuid

import env_reload
from langchain_core.output_parsers import BaseOutputParser
import re
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import run
need_answer = PromptTemplate.from_template("""
*********
你是AIGC课程的助教，你的工作是从学员的课堂交流中选择出需要老师回答的问题，加以整理以交给老师回答。

你的选择需要遵循以下原则：
1 需要老师回答的问题是指与课程内容或AI/LLM相关的技术问题；
2 评论性的观点、闲聊、表达模糊不清的句子，不需要老师回答；
3 学生输入不构成疑问句的，不需要老师回答；
4 学生问题中如果用“这”、“那”等代词指代，不算表达模糊不清，请根据问题内容判断是否需要老师回答。

课程内容:
{outlines}
*********
学员输入:
{user_input}
*********
Analyse the student's input according to the lecture's contents and your criteria.
Output your analysis process step by step.
Finally, output a single letter Y or N in a separate line.
Y means that the input needs to be answered by the teacher.
N means that the input does not needs to be answered by the teacher.""")


class MyOutputParser(BaseOutputParser):
    """自定义parser，从思维链中取出最后的Y/N"""
    def parse(self, text: str)->str:
        matches = re.findall(r'[YN]', text)
        return matches[-1] if matches else 'N'

model = ChatOpenAI(temperature=0,model_kwargs={"seed":42})

chain_v2 = (
    need_answer
    | model
    | MyOutputParser()
)

run.run_evaluation(chain_v2, "assistant-data", "cot-"+str(uuid.uuid4())[:8])