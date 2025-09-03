from typing import Union, List
import os
from langchain.agents import tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
# from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool
from langchain.tools.render import render_text_description

from dotenv import load_dotenv
from callbacks import AgentCallbackHandler

load_dotenv()

OLLAMA_HOST = os.environ.get('OLLAMA_HOST')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL')


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"\n[Tool Called] get_text_length enter with {text=}")
    # The LLM might pass the string with quotes, so we strip them
    text = text.strip("'\n").strip('"')
    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    """Finds a tool in a list by its name."""
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")


if __name__ == "__main__":
    print("--- Hello ReAct LangChain! ---")
    tools = [get_text_length]

    # --- THE FIX IS HERE ---
    # We add a clear, complete example to the prompt to guide the LLM.
    template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Here is an example of a successful run:

Question: What is the length of the word: PYTHON
Thought: I need to find the length of the word 'PYTHON'. I can use the get_text_length tool.
Action: get_text_length
Action Input: "PYTHON"
Observation: 6
Thought: I have the result. The length is 6. I can now provide the final answer.
Final Answer: 6

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = OllamaLLM(
        temperature=0,
        model=OLLAMA_MODEL,
        base_url=OLLAMA_HOST,
        stop=["\nObservation"],  # Only stop on observation to allow multi-step thoughts
        callbacks=[AgentCallbackHandler()],
    )

    agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
            }
            | prompt
            | llm
            | ReActSingleInputOutputParser()
    )

    intermediate_steps = []
    agent_step = None

    # Set a max number of iterations to prevent infinite loops
    max_iterations = 5
    for i in range(max_iterations):
        print(f"\n--- Step {i + 1} ---")

        # Check if the process has finished
        if isinstance(agent_step, AgentFinish):
            break

        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {
                "input": "What is the length of the word: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi",
                "agent_scratchpad": intermediate_steps,
            }
        )

        print(f"\n[Agent Output] {agent_step}")

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input

            observation = tool_to_use.func(str(tool_input))
            print(f"[Tool Observation] {observation=}")
            intermediate_steps.append((agent_step, str(observation)))

    if isinstance(agent_step, AgentFinish):
        print("\n--- Agent Finished ---")
        print(f"Final Answer: {agent_step.return_values['output']}")
    else:
        print("\n--- Agent Stopped (Max Iterations Reached) ---")

