import os
from langchain_community.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate

from utils.prompts import (
    TEXT_INST,
    TEXT_INST_OCR,
    TEXT_QUERY,
    TEXT_QUERY_OCR,
    FORMATTING_INST,
    FORMATTING_QUERY,
)


class Gemma:
    def __init__(self):
        self.model = Ollama(
            {
                "model": os.getenv("TEXT_MODEL", "gemma2:27b"),
                "base_url": os.getenv("TEXT_INFERENCE_URL", "http://localhost:11434"),
                "num_ctx": os.getenv("TEXT_CTX_SIZE", 8192),
                "temperature": os.getenv("TEXT_TEMP", 0.01),
                "num_predict": os.getenv("TEXT_MAX_PRED", 1024),
                "repeat_penalty": os.getenv("TEXT_REPEAT_PEN", 1.15),
            }
        )
        self.prompt = PromptTemplate.from_template("{system}\n{query}")
        self.chain = None

    def ask(self, req: dict | str, mode: str = "text") -> str:
        self.chain = (
            RunnablePassthrough() | self.prompt | self.model | StrOutputParser()
        )
        match mode.lower():
            case "text":
                query = {
                    "system": TEXT_INST,
                    "query": TEXT_QUERY.format(
                        req["long_ad_title"],
                        req["ad_title"],
                        req["description"],
                        req["company_name"],
                    ),  # FIXME: 키값 매칭
                }
            case "image":
                query = {
                    "system": TEXT_INST_OCR,
                    "query": TEXT_QUERY_OCR.format(
                        req["long_ad_title"],
                        req["ad_title"],
                        req["description"],
                        req["ocr_result"],
                        req["company_name"],
                    ),  # FIXME: 키값 매칭
                }
            case "formatting":
                query = {
                    "system": FORMATTING_INST,
                    "query": FORMATTING_QUERY.format(req),
                }
            case _:
                raise Exception("NotSupportModeError")
        return self.chain.invoke(query)

    def clear(self):
        self.chain = None
