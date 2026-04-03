import re
from typing import Optional


class Regex:
    @staticmethod
    def is_match(pattern: str, text: str) -> bool:
        try:
            match = re.match(pattern, text)
            return match is not None and match.end() == len(text)
        except re.error:
            return False

    @staticmethod
    def match(pattern: str, text: str) -> Optional[re.Match[str]]:
        try:
            return re.match(pattern, text)
        except re.error:
            raise
