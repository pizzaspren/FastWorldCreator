import io
import json
import os
import traceback
from zipfile import ZipFile, ZIP_DEFLATED


class Datapack:
    name = str()
    description = str()

    def __init__(self):
        self.datapack_files = list()

    @staticmethod
    def needs_loot_tables():
        return False

    def create_datapack_files(self, *args, **kwargs):
        self.add_datapack_file(
            path='pack.mcmeta',
            data=json.dumps(
                {
                    "pack": {
                        "pack_format": 1,
                        "description": f"{self.description}"
                    }
                },
                indent=4
            )
        )
        self._create_datapack_files(*args, **kwargs)
        return self.store()

    def _create_datapack_files(self, *args, **kwargs) -> None:
        self._create_recipes()
        self._create_functions()
        self._create_advancements()
        self._create_others(*args, **kwargs)

    def _create_recipes(self):
        self._shaped_recipes()
        self._shapeless_recipes()
        self._smelting_recipes()
        self._smoking_recipes()
        self._blasting_recipes()
        self._campfire_recipes()
        self._stonecutting_recipes()

    def _create_functions(self):
        pass

    def _create_advancements(self):
        pass

    def _create_others(self, *args, **kwargs):
        pass

    def add_datapack_file(self, path: str, data: str) -> None:
        self.datapack_files.append({
            "path": path,
            "data": data
        })

    def add_recipe_file(self, name: str, data: str) -> None:
        self.add_datapack_file(
            path=f"data/{self.name}/recipes/{name}.json",
            data=data
        )

    def add_advancement(self, advancement):
        self.add_datapack_file(
            path=advancement.get_path(),
            data=advancement.to_data()
        )

    def add_advancement_file(self, group: str, name: str, data: str) -> None:
        self.add_datapack_file(
            path=f"data/{self.name}/advancements/{group}/{name}.json",
            data=data
        )

    def store(self) -> bool:
        try:
            self._store()
            return True
        except Exception:
            traceback.print_exc()
            return False

    def _store(self) -> None:
        zip_bytes = io.BytesIO()
        with ZipFile(zip_bytes, 'w', ZIP_DEFLATED, False) as zip_f:
            for file in self.datapack_files:
                zip_f.writestr(
                    zinfo_or_arcname=file["path"],
                    data=file["data"]
                )

        output_file = os.sep.join(["datapacks", f"{self.name}.zip"])
        with open(output_file, 'wb') as file:
            file.write(zip_bytes.getvalue())

    def _shaped_recipes(self):
        pass

    def _shapeless_recipes(self):
        pass

    def _smelting_recipes(self):
        pass

    def _blasting_recipes(self):
        pass

    def _smoking_recipes(self):
        pass

    def _campfire_recipes(self):
        pass

    def _stonecutting_recipes(self):
        pass
