from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from schemas import Extract, Summarization, State, Documents, ExtractorInput, MergedExtract, MergedExtractField
from WorkflowAI.prompts import extract_system_prompt, summarization_system_prompt

import base64

import os
from dotenv import load_dotenv
load_dotenv()

credentials = f"{os.getenv('LOGIN')}:{os.getenv('PASSWORD')}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
auth_header = f"Basic {encoded_credentials}"

llm = ChatOpenAI(
    model="unsloth/Qwen3.6-35B-A3B-MTP-GGUF:UD-Q4_K_XL",
    temperature=0,
    api_key=os.getenv("LOCAL_API_KEY"),
    base_url=os.getenv("LOCAL_HOST"),
    default_headers={
        "Authorization": auth_header,
    }
)

extract_structured_llm = llm.with_structured_output(Extract)
summ_structured_llm = llm.with_structured_output(Summarization)

def form_input_extract_node(docs: list[Documents]) -> list[ExtractorInput]:
    """ Функция формирует бачи для передачи в экстрактор """
    form = []
    
    for doc in docs:
        if doc.is_chunked:
            for idx, chunk in enumerate(doc.chunks):
                input = ExtractorInput(
                    content=f"Информация взята из разделенного документа под названием - {doc.name_docs} деление номер - {idx}\n\nИнформация: {chunk.content}"
                )
                form.append(input)
        else:
            input = ExtractorInput(
                content=f"Информация взята из документа под названием - {doc.name_docs}\n\nИнформация: {doc.content}"
            )
            form.append(input)
    return form

def clean_merge(values: list[str | None]) -> list:
    """ 
        Очищает список:
            - Если все элементы None -> возвращает [None]
            - Если есть хотя бы один не-None -> возвращает только не-None значения
    """
    non_none = [i for i in values if i is not None]
    return non_none if non_none else [None]

def merge_extracts(extracts: list[Extract]) -> MergedExtract:
    """ Функция конкатит результат поиска ключевой информации из экстрактора в единую структуру """
    fields = Extract.model_fields.keys()

    merged = {}

    for field in fields:
        values = []
        resources = []

        for extract in extracts:
            field_obj = getattr(extract, field)
            values.append(field_obj.value)
            resources.append(field_obj.resource)

        cleaned_values = clean_merge(values)
        cleaned_resources = clean_merge(resources)

        merged[field] = MergedExtractField(
            values=cleaned_values,
            resources=cleaned_resources
        )

    return MergedExtract(**merged)

def from_input_summary_node(merge_extract: MergedExtract) -> str:
    """ Функция подготавливает входную информацию для summary node """
    fields = MergedExtract.model_fields.keys()

    content = ""

    for field in fields:
        content_field = []
        field_obj = getattr(merge_extract, field)
        desc_field = MergedExtract.model_fields[field].description
        values = field_obj.values
        resources = field_obj.resources

        title = f"{field}-{desc_field}:\n\n"
        content_field.append(title)

        if not all(val is None for val in values):
            for idx in range(len(values)):
                body = f"Источник номер {idx}: {resources[idx]}\nИнформация номер {idx}: {values[idx]}\n\n"
                content_field.append(body)
        else:
            content_field.append("None")
        content += " ".join(content_field) + "\n\n"

    return content

async def extract_node(state: State) -> dict:
    """ Нода, извлекающая ключевую информацию """
    contents = form_input_extract_node(state.docs)

    responses = await extract_structured_llm.abatch(
        [
            [
                SystemMessage(content=extract_system_prompt),
                HumanMessage(content=item.content)
            ]
            for item in contents
        ],
        config={
            "max_concurrency": 10
        }
    )

    print(from_input_summary_node(merge_extracts(responses)))

    return {"extracts": responses}

async def summary_node(state: State) -> dict:
    """ Нода, осуществляющая суммаризацию после отработки извлечения """
    
    merged = merge_extracts(state.extracts)
    contents = from_input_summary_node(merged)

    response = await summ_structured_llm.ainvoke(
        [
            SystemMessage(content=summarization_system_prompt),
            HumanMessage(content=contents)
        ]
    )       

    return {"summarization": response}