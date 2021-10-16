class BaseResponse:
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message

    def __str__(self):
        return "2"
