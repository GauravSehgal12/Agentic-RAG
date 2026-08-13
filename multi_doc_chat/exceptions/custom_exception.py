import sys
from typing import Optional, Union


def error_message_detail(error: Union[str, Exception], error_detail: Optional[Union[type(sys), Exception]] = None) -> str:
    if error_detail is sys or error_detail is None:
        _, _, exc_tb = sys.exc_info()
    elif isinstance(error_detail, Exception):
        exc_tb = error_detail.__traceback__
    else:
        exc_tb = None

    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return f"Error occurred in script [{file_name}] at line number [{line_number}]: {str(error)}"
    else:
        return f"Error message: {str(error)}"


class DocumentPortalException(Exception):
    def __init__(self, error_message: Union[str, Exception], error_detail: Optional[Union[type(sys), Exception]] = None):
        super().__init__(str(error_message))
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self) -> str:
        return self.error_message
