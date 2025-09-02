from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_ollama import OllamaLLM

from conf import OLLAMA_MODEL, OLLAMA_HOST
from social_media.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup import lookup as linkedin_lookup_agent


def ice_break_with(name: str):
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = OllamaLLM(temperature=0, model=OLLAMA_MODEL, base_url=OLLAMA_HOST)

    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": linkedin_data})

    print(f"\n--- Result --- \n")
    print(res)


if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with(name="ikhlas firlana")
