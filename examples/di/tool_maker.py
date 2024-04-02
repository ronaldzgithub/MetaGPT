#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/01/15
@Author  : mannaandpoem
@File    : imitate_webpage.py
"""
from metagpt.roles.di.data_interpreter import DataInterpreter
from metagpt.const import METAGPT_ROOT

EXAMPLE_CODE_FILE = METAGPT_ROOT / "examples/taoaistoresample.py"
MULTI_ACTION_AGENT_CODE_EXAMPLE = EXAMPLE_CODE_FILE.read_text()

PROMPT_TEMPLATE: str = """
    ### BACKGROUND
    You are using an agent framework called metagpt to write tools for taoaistore,
    the usage of metagpt can be illustrated by the following example:
    ### EXAMPLE STARTS AT THIS LINE
    {example}
    ### EXAMPLE ENDS AT THIS LINE
    ### TASK
    Now you should create an tools based on the instruction, consider carefully about
    the PROMPT_TEMPLATE of all actions 
    ### INSTRUCTION
    {instruction}
    ### YOUR CODE
    Return ```python your_code_here ``` with NO other texts, your code:
    """

async def main():

    agent_template: str = MULTI_ACTION_AGENT_CODE_EXAMPLE
    instruction = f"""Write an tool that will take a topic and do the following:
                        1. write an overview of the topic;
                        2. create a ppt out of the overview. with full detailed code. 
                        Note, assuming all libraries have been installed.
                        """
    prompt = PROMPT_TEMPLATE.format(example=agent_template, instruction=instruction)   
    
    di = DataInterpreter(tools=["<all>"])

    await di.run(instruction)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
