from __future__ import annotations


class ElementBase:

    def __init__(self, datapack_name: str = "minecraft"):
        self.datapack_name = datapack_name

    def get_path(self) -> str:
        return f"data/{self.datapack_name}"

    def to_data(self) -> str:
        return ""

    def set_datapack(self, datapack_name: str) -> ElementBase:
        self.datapack_name = datapack_name
        return self
