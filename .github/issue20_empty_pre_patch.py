from __future__ import annotations

from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{path}: expected one exact hardening anchor, found {count}: {old[:100]!r}"
        )
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "aquascope/collectors/south_africa_dws.py",
    """    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._depth = 0
        self.parts: list[str] = []
""",
    """    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.seen_pre = False
        self._depth = 0
        self.parts: list[str] = []
""",
)

replace_once(
    "aquascope/collectors/south_africa_dws.py",
    """        if tag.lower() == "pre":
            self._depth += 1
""",
    """        if tag.lower() == "pre":
            self.seen_pre = True
            self._depth += 1
""",
)

replace_once(
    "aquascope/collectors/south_africa_dws.py",
    """        table = parser.text.strip()
        if table:
            return table
""",
    """        table = parser.text.strip()
        if parser.seen_pre:
            return table
""",
)

replace_once(
    "tests/test_collectors/test_south_africa_dws.py",
    """def test_plain_text_and_pre_br_tables_are_supported():
""",
    """def test_empty_pre_is_an_empty_collection():
    collector = SouthAfricaDWSCollector(
        client=FakeClient(["<html><body><pre></pre></body></html>"])
    )
    assert collector.collect(station_id="X3H023", days=1, end_date="2026-01-01") == []


def test_plain_text_and_pre_br_tables_are_supported():
""",
)

print("DWS empty-pre no-data hardening applied deterministically.")
