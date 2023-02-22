import re

from nornir_dispatch import REGEX_VALID_FUNCTION_STRING


def test_regex_valid_function_string() -> None:
    assert re.match(REGEX_VALID_FUNCTION_STRING, "one.two.tree")
    assert re.match(REGEX_VALID_FUNCTION_STRING, "one.123two.tree")
    assert re.match(REGEX_VALID_FUNCTION_STRING, "one.123two.Tree.Four")
    assert re.match(REGEX_VALID_FUNCTION_STRING, "one.two") is None
    assert re.match(REGEX_VALID_FUNCTION_STRING, "one") is None
