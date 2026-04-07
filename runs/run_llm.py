from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM


def run_llm_obf(model, prompt, code):
    llm = OllamaLLM(
        model=model,
        temperature=0.35,
        num_predict=3000,
        top_p=0.95,
        top_k=60,
        repeat_penalty=1.05
    )
    
    parser = StrOutputParser()
    chain = prompt | llm | parser
    return chain.invoke({"code": code})


def run_llm_deob(model, prompt, code):
    llm = OllamaLLM(
        model=model,
        temperature=0.02,
        num_predict=4000,
        top_p=0.85,
        top_k=40,
        repeat_penalty=1.2
    )

    parser = StrOutputParser()
    chain = prompt | llm | parser
    return chain.invoke({"code": code})