import re
from typing import Dict, List


class SymbolsRule:
    def __init__(self):
        self.whitelist = r"「」【】[]-※(（)）*、,\＼/／.。?？!！・:%％&＆#＃+＋~～"

    def check(self, text_ad: Dict[str, str | List[str]]) -> Dict[str, bool]:
        result = {
            "emoji": False,
            "single_katakana": False,
            "headline_exclamation": False,
            "tilde_symbol": False,
            "repeated_symbols": False,
            "unexpected_symbols": False,
        }
        for key, texts in text_ad.items():
            if key in ["long_ad_title", "ad_title", "description"]:  # FIXME: 키값 매칭
                if isinstance(texts, list):
                    for text in texts:
                        self._update_result(result, text, key != "description")
                else:
                    self._update_result(result, texts, key != "description")
        return result

    def _update_result(
        self, result: Dict[str, bool], text: str, is_headline: bool
    ) -> None:
        result["emoji"] |= self._contains_emoji(text)
        result["single_katakana"] |= self._contains_single_katakana(text)
        result["tilde_symbol"] |= self._contains_tilde(text)
        result["repeated_symbols"] |= self._contains_repeated_symbols(
            text
        ) or self._contains_many_symbols(text)
        result["unexpected_symbols"] |= self._contains_unexpected_symbols(text)
        if is_headline:
            result["headline_exclamation"] |= self._contains_exclamation_headline(text)

    def _contains_emoji(self, text: str) -> bool:
        """이모지 사용 검사"""
        return any(ord(char) > 0x1F600 for char in text)

    def _contains_single_katakana(self, text: str) -> bool:
        """반각 카타카나 사용 검사"""
        return any(0xFF61 <= ord(char) <= 0xFF9F for char in text)

    def _contains_exclamation_headline(self, text: str) -> bool:
        """제목 ! 사용 검사"""
        return any(char in "!！" for char in text)

    def _contains_tilde(self, text: str) -> bool:
        """~ 사용 검사"""
        return any(char in "~～" for char in text)

    def _contains_repeated_symbols(self, text: str) -> bool:
        """동일 특수문자 연속 사용 검사"""
        return bool(re.search(r"([^\w\s])\1+", text))

    def _contains_many_symbols(self, text: str, threshold: int = 3) -> bool:
        """특수문자 연속 사용 검사"""
        return bool(re.search(rf"[^\w\s]{{{threshold},}}", text))

    def _contains_unexpected_symbols(self, text: str) -> bool:
        """whitelist에 없는 특수문자 사용 검사"""
        return any(
            char not in self.whitelist
            for char in text
            if not char.isalnum() and not char.isspace()
        )
