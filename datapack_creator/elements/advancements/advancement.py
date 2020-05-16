from __future__ import annotations

import json
from typing import List, Union

from datapack_creator.elements import ElementBase
from datapack_creator.elements.advancements import AdvancementFrame


class Advancement(ElementBase):

    def __init__(self, name="empty", group="story",
                 datapack="minecraft", frame=AdvancementFrame.TASK,
                 icon_item="minecraft:grass_block", icon_nbt="",
                 title="Placeholder", background=None,
                 description="Placeholder", hidden=False, parent=None,
                 criteria=None, requirements=None, rewards=None):
        super().__init__()
        self.name = name.split("/")[-1]
        self.group = "/".join(name.split("/")[:-1]) or parent.group or group
        self.datapack_name = datapack

        self.frame = frame
        self.icon = dict(item=icon_item)
        if icon_nbt:
            self.icon["nbt"] = icon_nbt
        self.title = title
        self.background = background
        self.description = description
        self.hidden = hidden

        self.parent = parent

        self.criteria = criteria
        self.requirements = requirements
        self.rewards = rewards

    def __str__(self) -> str:
        return f"{self.datapack_name}:{self.group}/{self.name}"

    def set_frame(self, frame: AdvancementFrame) -> Advancement:
        self.frame = str(frame)
        return self

    def set_icon(self, icon: dict) -> Advancement:
        self.icon = icon
        return self

    def set_icon_item(self, item: str) -> Advancement:
        self.icon["item"] = item
        return self

    def set_icon_nbt(self, nbt: str) -> Advancement:
        self.icon["nbt"] = nbt
        return self

    def set_title(self, title: str) -> Advancement:
        self.title = title
        return self

    def set_background(self, background: str) -> Advancement:
        self.background = background
        return self

    def set_description(self, desc: str) -> Advancement:
        self.description = desc
        return self

    def set_is_hidden(self, hidden: bool) -> Advancement:
        self.hidden = hidden
        return self

    def set_parent(self, parent: Advancement) -> Advancement:
        self.parent = str(parent) or "root"
        self.group = parent.group
        return self

    def set_criteria(self, criteria: dict) -> Advancement:
        self.criteria = criteria
        return self

    def set_requirements(self, requirements: List[
        Union[List[str], str]]) -> Advancement:
        self.requirements = requirements
        return self

    def set_rewards(self, rewards: dict) -> Advancement:
        self.rewards = rewards
        return self

    def _get_display(self) -> dict:
        display = dict(
            icon=self.icon,
            title=self.title,
            frame=self.frame,
            description=self.description,
            hidden=self.hidden
        )
        if self.background:
            display["background"] = self.background
        return display

    def get_path(self) -> str:
        return f"{super().get_path()}/advancements/{self.group}/{self.name}.json"

    def to_data(self) -> str:
        root_tag = dict()
        root_tag["display"] = self._get_display()
        if self.parent:
            root_tag["parent"] = str(self.parent)
        root_tag["criteria"] = self.criteria
        if self.requirements:
            root_tag["requirements"] = self.requirements
        if self.rewards:
            root_tag["rewards"] = self.rewards
        return json.dumps(root_tag)
