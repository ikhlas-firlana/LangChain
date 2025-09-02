from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.tools import DuckDuckGoSearchRun
import os
import time  # Import the time module
from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

load_dotenv()

OLLAMA_HOST = os.environ.get('OLLAMA_HOST')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL')

tools = [DuckDuckGoSearchRun()]

react_prompt = hub.pull("hwchase17/react")

output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"],
).partial(format_instructions=output_parser.get_format_instructions())

llm = OllamaLLM(temperature=0, model=OLLAMA_MODEL, base_url=OLLAMA_HOST)

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_format_instructions,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

extract_output = RunnableLambda(lambda x: x["output"])
parse_output = RunnableLambda(lambda x: output_parser.parse(x))

chain = agent_executor | extract_output | parse_output


def main():
    # Record the start time
    result = None
    start_time = time.perf_counter()
    try:
        result = chain.invoke(
            {
                "input": "search for 3 job postings for an ai engineer using langchain in remote full time on linkedin and "
                         "list their details",
            }
        )
    except NameError:
        print('NameError')

    # Record the end time
    end_time = time.perf_counter()

    # Calculate and print the elapsed time
    elapsed_time = end_time - start_time

    print("\n--- Execution Summary ---")
    print(result)
    print(f"Process took {elapsed_time:.2f} seconds to complete.")


if __name__ == "__main__":
    main()
