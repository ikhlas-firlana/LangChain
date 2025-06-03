from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import OllamaLLM
from conf import OLLAMA_HOST, OLLAMA_MODEL
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub

from tools.tools import get_profile_url_tavily


def lookup(name: str):
    llm = OllamaLLM(
        model=OLLAMA_MODEL,
        temperature=0,  # Lower temperature for more focused, less verbose output
        base_url=OLLAMA_HOST,
    )

    # agent_input_template_str = """Find the LinkedIn profile URL for the person named {name_of_person}."""
    agent_input_template_str = """
    You are a research assistant. Your task is to find the publicly available LinkedIn profile URL for the person named {name_of_person}.
    This information is used for professional networking and is often publicly listed by individuals themselves.
    Please use the provided tools to find this specific information.
    If a LinkedIn URL is found, your final answer should be ONLY the URL.
    If no LinkedIn URL is found after using your tools, clearly state that.
    Do not express personal opinions or refuse based on privacy if the information is typically public.
    """

    prompt_for_agent_input = PromptTemplate(
        template=agent_input_template_str,
        input=['name_of_person']
    )

    tools_for_agent = [
        Tool(
            name="GetLinkedInProfileURL",
            func=get_profile_url_tavily,
            description="Use this to find the LinkedIn profile URL for a specific person. The input to this tool "
                        "should be only the person's full name.",
        )
    ]

    # This is the standard ReAct prompt. It expects the LLM to eventually output:
    # "Final Answer: [the actual answer to the question]"
    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )

    # 3. Add handle_parsing_errors to AgentExecutor for more graceful error handling or debugging.
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True
    )

    # Format the input string for the agent.
    # This string becomes the value for the 'input' variable in the react_prompt.
    formatted_input_for_agent = prompt_for_agent_input.format_prompt(name_of_person=name).to_string()
    print(f"\n--- Feeding to Agent Executor ---\nInput: \"{formatted_input_for_agent}\"")

    result = agent_executor.invoke(
        input={"input": formatted_input_for_agent}
    )
    print(f"\n--- Agent Executor Result --- \n{result}")

    linkedin_profile_url = result.get('output') if isinstance(result, dict) else str(result)

    return linkedin_profile_url


# if __name__ == "__main__":
#     print(lookup(name="Ikhlas Firlana"))
