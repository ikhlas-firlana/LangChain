from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv

information = """
Elon Reeve Musk is a businessman known for his leadership of Tesla, SpaceX, and X (formerly Twitter). In early 2025, he served as senior advisor to United States president Donald Trump and as the de facto head of the Department of Government Efficiency (DOGE).
"""

if __name__ == '__main__':
    load_dotenv()
    print("ice breaker")

    summary_template = """
    Based on this information:
    {information}
    
    Generate:
    1. A concise summary.
    2. Two interesting facts.
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # --- For debugging: Print the formatted prompt ---
    formatted_prompt = summary_prompt_template.format(information=information)
    print("--- Formatted Prompt being sent to LLM: ---")
    print(formatted_prompt)
    print("------------------------------------------")
    # --- End debugging ---

    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    llm = OllamaLLM(model="gemma:2b")

    chain = summary_prompt_template | llm | StrOutputParser()

    print("Attempting to invoke LLM chain...")  # New print statement
    try:
        res = chain.invoke(input={"information": information})
        print("\n--- LLM Response: ---")  # This will only print if invoke succeeds
        print(res)
    except Exception as e:
        print("\n--- ERROR DURING LLM INVOCATION: ---")
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()  # This will give you a full stack trace
    print("Script finished or error handled.")  # New print statement

