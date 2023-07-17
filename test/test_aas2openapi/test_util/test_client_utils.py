import pytest

from aas2openapi.util.client_utils import get_base64_from_string

def test_get_base64_from_string():
    # Test with a simple string
    string = "Hello, World!"
    expected_base64 = "SGVsbG8sIFdvcmxkIQ=="
    assert get_base64_from_string(string) == expected_base64

    # Test with an empty string
    string = ""
    expected_base64 = ""
    assert get_base64_from_string(string) == expected_base64

    # Test with a string containing special characters
    string = "Hello$#@$World!123"
    expected_base64 = "SGVsbG8kI0AkV29ybGQhMTIz"
    assert get_base64_from_string(string) == expected_base64

    # Test with a Unicode string
    string = "你好，世界！"
    expected_base64 = "5L2g5aW977yM5LiW55WM77yB"
    assert get_base64_from_string(string) == expected_base64