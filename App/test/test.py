from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field


class Student(BaseModel):
    name: str = Field(description="学生的姓名")
    age: str = Field(description="学生的年龄")

student_query = "告诉我一个学生的信息"

parser = PydanticOutputParser(pydantic_object=Student)

prompt = PromptTemplate(
    template="回答下面问题.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()+"用中文回答"},
)

_input = prompt.format_prompt(query=student_query)

output = model(_input.to_string())
print(output)
print(parser.parse(output))