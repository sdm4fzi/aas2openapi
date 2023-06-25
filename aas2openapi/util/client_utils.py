import base64


def get_base64_from_string(string: str) -> str:
    b = base64.b64encode(bytes(string, "utf-8"))  # bytes
    base64_str = b.decode("utf-8")  # convert bytes to string
    return base64_str