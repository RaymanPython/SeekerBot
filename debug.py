import inspect
from config import DEBUG


def debug():
    if DEBUG:
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name
        print(caller_name)
        # caller_signature = inspect.signature(caller_frame.f_code)
        # print("Параметры вызывающей функции:", caller_signature.parameters)
