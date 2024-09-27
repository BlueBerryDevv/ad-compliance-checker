import os
import base64
import requests
from io import BytesIO
from PIL import Image
from langchain_community.llms import ChatOllama
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.messages import HumanMessage

from utils.prompts import OCR_INST


class Llava:
    
    def __init__(self):
        self.model = ChatOllama(
            model=os.getenv("OCR_MODEL", "llava:7b"),
            base_url=os.getenv("OCR_INFERENCE_URL", "http://localhost:11434"),
            num_ctx=int(os.getenv("OCR_CTX_SIZE", 8192)),
            temperature=float(os.getenv("OCR_TEMP", 0.01)),
            num_predict=int(os.getenv("OCR_MAX_PRED", 1024)),
            repeat_penalty=float(os.getenv("OCR_REPEAT_PEN", 1.15)),
        )
        self.chain = None

    def ask(self, image: Image) -> str:  # FIXME: 이미지 타입 매칭

        if isinstance(image, str):
            if image.startswith('http'):
                image = Image.open(requests.get(image, stream=True).raw)
            else:
                image = Image.open(image)

        query = {"text": OCR_INST, "image": self._convert_to_base64(image)}

        self.chain = (
            RunnablePassthrough() | self._prompt_func | self.model | StrOutputParser()
        )

        return self.chain.invoke(query)

    def clear(self):
        self.chain = None

    def _convert_to_base64(self, pil_image):
        """PIL 이미지를 Base64로 인코딩된 문자열로 변환합니다."""
        buffered = BytesIO()
        pil_image.save(
            buffered, format="JPEG"
        )  # 필요한 경우 형식을 변경할 수 있습니다.
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    def _prompt_func(self, data):
        """프롬프트 함수를 정의합니다."""
        text = data["text"]  # 데이터에서 텍스트를 가져옵니다.
        image = data["image"]  # 데이터에서 이미지를 가져옵니다.

        image_part = {  # 이미지 부분을 정의합니다.
            "type": "image_url",  # 이미지 URL 타입을 지정합니다.
            "image_url": f"data:image/jpeg;base64,{image}",  # 이미지 URL을 생성합니다.
        }

        content_parts = []  # 콘텐츠 부분을 저장할 리스트를 초기화합니다.

        text_part = {"type": "text", "text": text}  # 텍스트 부분을 정의합니다.

        content_parts.append(image_part)  # 이미지 부분을 콘텐츠 부분에 추가합니다.
        content_parts.append(text_part)  # 텍스트 부분을 콘텐츠 부분에 추가합니다.

        return [HumanMessage(content=content_parts)]  # HumanMessage 객체를 반환합니다.