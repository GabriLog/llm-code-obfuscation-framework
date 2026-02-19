from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM


def run_llm(model, prompt, code):
    llm = OllamaLLM (
        model=model,
        temperature=0.2,
        num_predict=600,
        top_p=0.9
    )
    parser = StrOutputParser()
    chain = prompt | llm | parser
    return chain.invoke({"code": code})