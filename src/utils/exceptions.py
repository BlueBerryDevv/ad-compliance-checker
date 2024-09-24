class ResultNotFoundError(Exception):
    """JSON 결과를 찾을 수 없을 때 발생하는 예외"""

    def __init__(self, message="LLM 응답간 JSON 데이터를 찾을 수 없습니다."):
        self.message = message
        super().__init__(self.message)


class NotSupportModeError(Exception):
    """지원하지 않는 모드를 사용할 때 발생하는 예외"""

    def __init__(self, message="지원하지 않는 모드입니다."):
        self.message = message
        super().__init__(self.message)


class MaxTokenExceededError(Exception):
    """최대 토큰 수를 초과했을 때 발생하는 예외"""

    def __init__(self, message="최대 토큰 수를 초과했습니다."):
        self.message = message
        super().__init__(self.message)
