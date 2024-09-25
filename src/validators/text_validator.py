import os
import re
import json_repair
import logging

from models.gemma_model import Gemma
from utils.exceptions import (
    ResultNotFoundError,
    NotSupportModeError,
    MaxTokenExceededError,
)
from validators.rule_base_validator import (
    SymbolsRule,
)  # FIXME: 임시 규칙기반 검수 로직 적용중


def text_validate(
    data: dict[str, str],
    mode: str = "text",
    retry: int = 0,
):
    def _parsing(response: str) -> dict:
        """응답 Dict 변환 함수"""
        result = json_repair.loads(response)  # json 없으면 빈 문자열 반환
        if isinstance(result, dict):
            return result
        else:
            raise ResultNotFoundError

    try:
        # LLM API 요청
        model = Gemma()
        response = model.ask(data, mode)

        try:
            result = _parsing(response)  # 응답 파싱
        except Exception as e:
            response_formatting = model.ask(
                response, "formatting"
            )  # 응답 JSON 규격화 요청
            result = _parsing(response_formatting)

        # 텍스트 소재 검수시 규칙기반 특수문자 검사
        if mode.lower() == "text":
            # FIXME: 임시 규칙기반 검수 로직 적용중
            symbol_rule = SymbolsRule()
            symbol_result = symbol_rule.check(data)
            if any(symbol_result.values()):
                result["Style and Spelling"] = "Risk"

        # TODO: 응답 DB 저장

        return result

    except (ResultNotFoundError, NotSupportModeError, MaxTokenExceededError):
        raise
    except Exception as e:
        if retry >= int(os.getenv("MAX_RETRY", 3)):
            raise e
        retry += 1
        # TODO: enqueue with retry param

        msg = f"[Try {retry}/{int(os.getenv("MAX_RETRY", 3))}] Text process got ERROR: {e}"
        logging.info(msg)
        return msg
