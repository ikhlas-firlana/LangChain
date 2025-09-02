from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
import os
import time  # Import the time module

load_dotenv()

OLLAMA_HOST = os.environ.get('OLLAMA_HOST')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL')

tools = [DuckDuckGoSearchRun()]

react_prompt = hub.pull("hwchase17/react")

llm = OllamaLLM(temperature=0, model=OLLAMA_MODEL, base_url=OLLAMA_HOST)

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt,
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

chain = agent_executor


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
    print(result['output'])
    print(f"Process took {elapsed_time:.2f} seconds to complete.")


if __name__ == "__main__":
    main()
