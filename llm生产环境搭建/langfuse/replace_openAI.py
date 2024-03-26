# -*- coding: utf-8 -*-
import env_reload
from langfuse.openai import openai
from langfuse import Langfuse

trace = Langfuse().trace(
    name="hello-world",
    user_id="wzr1111111111",
    release="v0.0.1"
)

completion = openai.chat.completions.create(
    name="hello-world",
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "对我说'Hello, World!'"}
    ],
    temperature=0,
    trace_id=trace.id,
)

print(completion.choices[0].message.content)
