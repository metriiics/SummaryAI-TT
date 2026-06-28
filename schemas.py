from pydantic import BaseModel, Field
from typing import Optional

class ChunkingMetadata(BaseModel):
    length_char: int
    length_word: int
    predicted_number_tokens: float
    chunk: int

class ChunkingDocuments(BaseModel):
    content: str
    metadata: ChunkingMetadata

    @classmethod
    def adding(
        cls, 
        text: str, 
        len_char: int, 
        len_word: int, 
        num_chunk: int) -> "ChunkingDocuments":
        
        return cls(
            content=text,
            metadata=ChunkingMetadata(
                length_char=len_char,
                length_word=len_word,
                predicted_number_tokens=len_word * 2.25,
                chunk=num_chunk
            )
        )

class DocMetadata(BaseModel):
    file_type: str
    length_char: int
    length_word: int
    predicted_number_tokens: float

class Documents(BaseModel):
    name_docs: str
    content: str
    metadata: DocMetadata

    is_chunked: bool = False
    chunks: Optional[list[ChunkingDocuments]] = None

    def set_chunk(
        self, 
        status: bool, 
        chunks: list[ChunkingDocuments] | None = None
    ) -> "Documents":
        return self.model_copy(
            update={
                "is_chunked": status,
                "chunks": chunks
            }
        )
    
class ExtractField(BaseModel):
    value: str | None = None
    resource: str | None = None

class Extract(BaseModel):
    """
        attrs:
            license - Информация о лицензиях или наличии других разрешительных документов у поставщика
            experience_accreditation - Информация о наличии дополнительной аккредитации у заказчика. Наличие требования к опыту работы поставщика в аналогичной сфере
            delivery_basis - Базис поставки
            delivery_terms - Условия поставки
            work_conditions - Условия выполнения работ - сроки и оценка времени (сроков) присутствия поставщика на объекте
            info_div_lot - Информация о делимости лота
            registry_included - Наличие в реестре Минпромторга или применения в закупке нацрежима
            technical_specifications - Тех задание для работ, спецификация для товаров
            additional_okpd2 - Наличие дополнительных ОКПД2 для комплексных закупок
            required_materials - Необходимые маетриалы (если закупка предполагает изготовление предмета закупки)
            supplied_quantity - Поставляемое количество
            trademark_alternatives_allowed - Торговая марка и допускает ли предложение аналогов
    """
    license: Optional[ExtractField] = None
    experience_accreditation: Optional[ExtractField] = None
    delivery_basis: Optional[ExtractField] = None
    delivery_terms: Optional[ExtractField] = None
    work_conditions: Optional[ExtractField] = None
    info_div_lot: Optional[ExtractField] = None
    registry_included: Optional[ExtractField] = None
    technical_specifications: Optional[ExtractField] = None
    additional_okpd2: Optional[ExtractField] = None
    required_materials: Optional[ExtractField] = None
    supplied_quantity: Optional[ExtractField] = None
    trademark_alternatives_allowed: Optional[ExtractField] = None

class MergedExtractField(BaseModel):
    values: list[Optional[str]] = []
    resources: list[Optional[str]] = []

class MergedExtract(BaseModel):
    license: MergedExtractField = Field(
        description="Информация о лицензиях или наличии других разрешительных документов у поставщика."
    )
    experience_accreditation: MergedExtractField = Field(
        description="Информация о наличии дополнительной аккредитации у заказчика. Наличие требования к опыту работы поставщика в аналогичной сфере"
    )
    delivery_basis: MergedExtractField = Field(
        description="Базис поставки"
    )
    delivery_terms: MergedExtractField = Field(
        description="Условия поставки"
    ) 
    work_conditions: MergedExtractField = Field(
        description="Условия выполнения работ - сроки и оценка времени (сроков) присутствия поставщика на объекте"
    )
    info_div_lot: MergedExtractField = Field(
        description="Информация о делимости лота"
    )
    registry_included: MergedExtractField = Field(
        description="Наличие в реестре Минпромторга или применения в закупке нацрежима"
    )
    technical_specifications: MergedExtractField = Field(
        description="Тех задание для работ, спецификация для товаров"
    )
    additional_okpd2: MergedExtractField = Field(
        description="Наличие дополнительных ОКПД2 для комплексных закупок"
    )
    required_materials: MergedExtractField = Field(
        description="Необходимые материалы (если закупка предполагает изготовление предмета закупки)"
    )
    supplied_quantity: MergedExtractField = Field(
        description="Поставляемое количество"
    )
    trademark_alternatives_allowed: MergedExtractField = Field(
        description="Торговая марка и допускает ли предложение аналогов"
    )

class CoreInfo(BaseModel):
    license: str = None
    experience_accreditation: str = None
    delivery_basis: str = None
    delivery_terms: str = None
    work_conditions: str = None
    info_div_lot: str = None
    registry_included: str = None
    technical_specifications: str = None
    additional_okpd2: str = None
    required_materials: str = None
    supplied_quantity: str = None
    trademark_alternatives_allowed: str = None

class ExtractorInput(BaseModel):
    content: str

class Summarization(BaseModel):
    core_info: CoreInfo

    summary: str = Field(description="саммари")
    resource: list[str] = Field(description="Источники")

class State(BaseModel):
    docs: list[Documents] 
    extracts: Optional[list[Extract]] = None
    summarization: Optional[Summarization] = None