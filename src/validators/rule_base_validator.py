import pandas as pd
import re

def llm_analyze_text(text_data):
    return ''


def is_japanese_char(char):
    return '\u3040' <= char <= '\u30ff' or '\u4e00' <= char <= '\u9fff'

def is_enclosed_alphanumeric(char):
    return '\u2460' <= char <= '\u24ff'  # 원문자 범위


whitelist = [
    "「", "」", "【", "】", "[", "]", "-", "※", "(", "（", 
    ")", "）", "*", "、", ", ", "\\", "＼", "/", "／", ".", 
    "。", "?", "？", "!", "！", "・", ":", "%", "％", 
    "&", "＆", "#", "＃", "+", "＋","'"
    ] + list('＃、％%/！。.,（)〘〙（）【】＞_+·×')
whitelist = list(set(whitelist))
    
def check_repeat_punctuation(text, column_name):
    status = 'Safe'
    reasons = []

    text = text.replace("^@!%#$", '')
    
    if pd.isnull(text):
        text = ''
    
    text = text.strip()

    # 1. 'long_ad_title'과 'ad_title'에서 느낌표 사용 검사
    if column_name in ['long_ad_title', 'ad_title']:
        exclamation_marks = re.findall(r'[！!]', text)
        if exclamation_marks:
            status = 'Approved_limited'
            reasons.append(f"Exclamation mark(s) used in title: {', '.join(exclamation_marks)}")

    # 2. 문장 부호나 기호를 연속으로 반복해서 사용
    repeated_chars = re.findall(r'([^\w\s])\1{1,}', text)
    if repeated_chars:
        status = 'Approved_limited'
        reasons.append(f"Repeated punctuation or symbols: {', '.join(repeated_chars)}")


    
    # 허용된 특수 문자 정의
    allowed_special_chars = ''.join(whitelist)

    # 알파벳, 일본어 문자, 숫자 앞뒤로 특수문자가 오는 경우 검사 (허용된 특수 문자 예외 처리)
    for i, char in enumerate(text):
        if char.isalnum() or is_japanese_char(char):
            if i > 0:
                prev_char = text[i-1]
                if not (prev_char.isalnum() or is_japanese_char(prev_char) or prev_char.isspace() or 
                        prev_char in allowed_special_chars):
                    status = 'Approved_limited'
                    reasons.append(f"Special character '{prev_char}' before alphanumeric or Japanese character '{char}'")
                    break
            if i < len(text) - 1:
                next_char = text[i+1]
                if not (next_char.isalnum() or is_japanese_char(next_char) or next_char.isspace() or 
                        next_char in allowed_special_chars):
                    status = 'Approved_limited'
                    reasons.append(f"Special character '{next_char}' after alphanumeric or Japanese character '{char}'")
                    break

    # 원문자 사용 검출
    enclosed_chars = re.findall(r'[\u2460-\u24ff]', text)
    if enclosed_chars:
        status = 'Approved_limited'
        reasons.append(f"Use of enclosed alphanumeric characters: {', '.join(enclosed_chars)}")
        
    # 4. 위 첨자의 비표준적인 사용
    superscripts = re.findall(r'\w\^\w?', text)
    if superscripts:
        status = 'Approved_limited'
        reasons.append(f"Non-standard use of superscript: {', '.join(superscripts)}")

    # 5. 글머리 기호, 별표 등 비표준 기호나 문자 사용
    non_standard_symbols = []
    lines = text.split('\n')
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            first_char = stripped_line[0]
            if first_char in ['*', '•', '▪', '●', '■', '◆', '★', '☆', '►', '▻', '→', '⇒', '⁃', '‣', '○', '◯', '◦', '⦿', '⁌', '⁍']:
                non_standard_symbols.append(first_char)

    if non_standard_symbols:
        status = 'Approved_limited'
        reasons.append(f"Use of non-standard symbols or characters as bullet points: {', '.join(non_standard_symbols)}")
        
    # 6. 숫자, 기호, 문장 부호를 과도하게 또는 시선을 끌 목적으로 사용
    def is_not_price(match):
        # 숫자 뒤에 '円'이 있는지 확인
        return not re.search(rf'{match.group(0)}円', text)

    # 숫자가 개 이상 연속되고 뒤에 円이 없는 경우만 찾기
    excessive_numbers = [match.group(0) for match in re.finditer(r'(\d)\1{9,}', text) if is_not_price(match)]

    # 숫자가 아닌 문자가 3개 이상 연속되는 경우 찾기
    excessive_chars = re.findall(r'([^\d\s])\1{2,}', text)

    # 문자.문자.문자 패턴 찾기
    excessive_dots = re.findall(r'(\w\.){2,}\w', text)

    all_excessive = excessive_numbers + excessive_chars + excessive_dots

    if all_excessive:
        status = 'Approved_limited'
        reasons.append(f"Excessive use of numbers, symbols, or punctuation: {', '.join(all_excessive)}")
        
    # 7. 표시 이름, 단어, 구문을 표준이 아니거나 변칙적으로 또는 불필요하게 반복
    words = text.split()
    repeated_words = [word for word in set(words) if words.count(word) > 5]
    if repeated_words:
        status = 'Approved_limited'
        reasons.append(f"Excessive repetition of words or phrases: {', '.join(repeated_words)}")

    # 8. 금지된 기호 사용 검출 (re.search 사용)
    prohibited_symbols = re.findall(r'[~☆]', text)
    if prohibited_symbols:
        status = 'Approved_limited'
        reasons.append(f"Use of prohibited symbols: {', '.join(prohibited_symbols)}")

    if not reasons:
        status = 'Safe'

    return status, reasons