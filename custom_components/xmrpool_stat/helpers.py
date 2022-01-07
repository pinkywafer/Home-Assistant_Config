"""Helper methods"""

from typing import Any, Dict, Optional


def DefaultTo(value: str, default: str) -> str:
    return value if value != None else default


def GetDictValue(source: Dict[str, Any], key: str) -> any:
    if source is None:
        return None
    return source.get(key)
