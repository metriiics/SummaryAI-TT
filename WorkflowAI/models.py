from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from schemas import Extract, Summarization, State, Documents, ExtractorInput
from WorkflowAI.prompts import extract_system_prompt, summarization_system_prompt

import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    model="google/gemma-4-e2b",
    temperature=0,
    api_key=os.getenv("LOCAL_API_KEY"),
    base_url=os.getenv("LOCAL_HOST")
)

extract_agent = create_agent(
    model=llm,
    response_format=Extract
)
summ_agent = create_agent(
    model=llm,
    response_format=Summarization
)

def form_input_extract_node(docs: list[Documents]) -> list[ExtractorInput]:
    """ Функция формирует бачи для передачи в экстрактор """
    form = []
    
    for doc in docs:
        if doc.is_chunked:
            for chunk in doc.chunks:
                input = ExtractorInput(
                    content=f"Content: {chunk.content}\n\nInformation sources: {doc.name_docs}"
                )
                form.append(input)
        else:
            input = ExtractorInput(
                content=f"Content: {doc.content}\n\nInformation sources: {doc.name_docs}"
            )
            form.append(input)
    return form

def extract_node(state: State) -> dict:
    """ Нода, извлекающая ключевую информацию """
    
    contents = form_input_extract_node(state.docs)

    responses = extract_agent.batch(
        [
            {
                "messages": [
                    SystemMessage(content=extract_system_prompt),
                    HumanMessage(content=item.content)
                ]
            }
            for item in contents
        ],
        config={
            "max_concurrency": 4
        }
    )

    extracts = [
        response["structured_response"]
        for response in responses
    ]

    return {"extracts": extracts}

def summary_node(state: State) -> dict:
    """ Нода, осуществляющая суммаризацию после отработки извлечения """
    
    contents = "\n\n".join(
        f"Источник: {doc.resource}\n{doc.main_info}"
        for doc in state.extracts
    )

    response = summ_agent.invoke(
        {
            "messages": [
                SystemMessage(content=summarization_system_prompt),
                HumanMessage(content=contents)
            ]
        }
    )       

    output = response["structured_response"]
    return {"summarization": output}