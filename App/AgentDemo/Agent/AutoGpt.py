 


import json

from langchain.memory import ConversationTokenBufferMemory, VectorStoreRetrieverMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.tools.render import render_text_description
from langchain_core.language_models import BaseChatModel
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import BaseTool
from langchain.prompts import PromptTemplate
from typing import List, Tuple

from langchain_core.vectorstores import VectorStoreRetriever
from pydantic import ValidationError

from App.AgentDemo.Agent.Action import Action
from App.AgentDemo.Utils.CallbackHandlers import *
from App.AgentDemo.Utils.PrintUtils import THOUGHT_COLOR, ROUND_COLOR, OBSERVATION_COLOR


class AutoGpt:
    """AutoGPT :基于Langchain的自动GPT实现"""

    def __init__(
            self,
            llm: BaseChatModel,
            tools: List[BaseTool],
            work_dir: str = "./data",
            main_prompt_file: str = "./prompts/main/main.txt",
            final_prompt_file: str = "./prompts/main/file_step.txt",
            max_thought_steps: Optional[int] = 10,
            memory_retriever: Optional[VectorStoreRetriever] = None
    ):
        self.llm = llm
        self.tools = tools
        self.work_dir = work_dir
        self.main_prompt_file = main_prompt_file
        self.final_prompt_file = final_prompt_file
        self.max_thought_steps = max_thought_steps
        self.memory_retriever = memory_retriever

        # OutputFixingParse:如果输出不正确尝试修复
        self.output_parser = PydanticOutputParser(pydantic_object=Action)
        self.robust_parser = OutputFixingParser.from_llm(parser=self.output_parser, llm=self.llm)

        self.__init_prompt_templates()
        self.__init_chains()
        self.verbose_handler = ColoredPrintHandler(color=THOUGHT_COLOR)

    def run(self, task_description, verbose=False) -> str:
        # 初始化短时记忆
        short_term_memory = self.__init_short_term_memory()
        # 连接长时记忆（如果有）
        long_term_memory = self.__connect_long_term_memory()

        # 思考步数
        thought_step_count = 0
        # 开始逐步思考
        while thought_step_count < self.max_thought_steps:
            if verbose:
                color_print(f">>>>Round: {thought_step_count}<<<<", ROUND_COLOR)

            # 执行一步思考
            action, response = self.__step(
                task_description=task_description,
                short_term_memory=short_term_memory,
                long_term_memory=long_term_memory,
                verbose=verbose,
            )

            # 如果是结束指令，执行最后一步
            if action.name == "FINISH":
                break
            # 执行动作
            observation = self.__exec_action(action)
            self.__show_observation(observation, verbose)
            # 更新短时记忆
            self.__update_short_term_memory(
                short_term_memory, response, observation
            )

            thought_step_count += 1

        if thought_step_count >= self.max_thought_steps:
            # 如果思考步数达到上限，返回错误信息
            reply = "抱歉，我没能完成您的任务。"
        else:
            # 否则，执行最后一步
            reply = self.__final_step(short_term_memory, task_description)

        # 更新长时记忆
        self.__update_long_term_memory(long_term_memory, task_description, reply)

        return reply

    def __init_prompt_templates(self):
        self.main_prompt = PromptTemplate.from_file(
            self.main_prompt_file
        ).partial(
            work_dir=self.work_dir,
            tools=render_text_description(self.tools),
            format_instructions=self.__chinese_friendly(
                self.output_parser.get_format_instructions(),
            )
        )
        self.final_prompt = PromptTemplate.from_file(
            self.final_prompt_file
        )

    @staticmethod
    def __chinese_friendly(string) -> str:
        lines = string.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('{') and line.endswith('}'):
                try:
                    lines[i] = json.dumps(json.loads(line), ensure_ascii=False)
                except:
                    pass
        return '\n'.join(lines)

    def __init_chains(self):
        # 主流程的chain
        self.main_chain = (self.main_prompt | self.llm | StrOutputParser())
        # 最终一步的chain
        self.final_chain = (self.final_prompt | self.llm | StrOutputParser())



    def __init_short_term_memory(self) -> BaseChatMemory:
        short_term_memory = ConversationTokenBufferMemory(
            llm=self.llm,
            max_token_limit=4000,
        )
        short_term_memory.save_context(
            {"input": "\n初始化"},
            {"output": "\n开始"}
        )
        return short_term_memory

    def __connect_long_term_memory(self) -> BaseMemory:
        if self.memory_retriever is not None:
            long_term_memory = VectorStoreRetrieverMemory(
                retriever=self.memory_retriever,
            )
        else:
            long_term_memory = None
        return long_term_memory

    @staticmethod
    def __update_short_term_memory(
            short_term_memory: BaseChatMemory,
            response: str,
            observation: str
    ):
        short_term_memory.save_context(
            {"input": response},
            {"output": "\n返回结果:\n" + observation}
        )

    @staticmethod
    def __update_long_term_memory(
            long_term_memory: BaseMemory,
            task_description: str,
            final_reply: str
    ):
        if long_term_memory is not None:
            long_term_memory.save_context(
                {"input": task_description},
                {"output": final_reply}
            )

    def __step(self,
               task_description,
               short_term_memory,
               long_term_memory,
               verbose=False
               ) -> Tuple[Action, str]:

        """执行一步思考"""
        response = ""
        for s in self.main_chain.stream(input={
            "task_description": task_description,
            "short_term_memory": self.__format_short_term_memory(
                short_term_memory
            ),
            "long_term_memory": self.__format_long_term_memory(
                task_description,
                long_term_memory
            ) if long_term_memory is not None else "",
        }, config={
            "callbacks": [
                self.verbose_handler
            ] if verbose else []
        }):
            response += s

        action = self.robust_parser.parse(response)
        return action, response

    def __exec_action(self, action: Action) -> str:
        # 查找工具
        tool = self.__find_tool(action.name)
        if tool is None:
            observation = (
                f"Error: 找不到工具或指令 '{action.name}'. "
                f"请从提供的工具/指令列表中选择，请确保按对顶格式输出。"
            )
        else:
            try:
                # 执行工具
                observation = tool.run(action.args)
            except ValidationError as e:
                # 工具的入参异常
                observation = (
                    f"Validation Error in args: {str(e)}, args: {action.args}"
                )
            except Exception as e:
                # 工具执行异常
                observation = f"Error: {str(e)}, {type(e).__name__}, args: {action.args}"

        return observation

    @staticmethod
    def __show_observation(observation: str, verbose: bool):
        if verbose:
            color_print(f"----\n结果:\n{observation}", OBSERVATION_COLOR)

    def __final_step(self, short_term_memory, task_description) -> str:
        """最后一步, 生成最终的输出"""
        response = self.final_chain.invoke({
            "task_description": task_description,
            "short_term_memory": self.__format_short_term_memory(
                short_term_memory
            ),
        })
        return response

    @staticmethod
    def __format_short_term_memory(memory: BaseChatMemory) -> str:
        messages = memory.chat_memory.messages
        string_messages = [messages[i].content for i in range(1, len(messages))]
        return "\n".join(string_messages)

    @staticmethod
    def __format_long_term_memory(task_description: str, memory: BaseChatMemory) -> str:
        return memory.load_memory_variables(
            {"prompts": task_description}
        )["history"]

    def __find_tool(self, tool_name: str) -> Optional[BaseTool]:
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None
