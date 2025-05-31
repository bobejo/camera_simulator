import pathlib
from typing import Any

import yaml
from pydantic import BaseModel, model_validator


class CameraConfig(BaseModel):
    register_description: dict[str, Any] = {}

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="before")
    @classmethod
    def load_from_file(cls, data: Any) -> Any:
        if isinstance(data, dict) and "configuration_file" in data:
            path = pathlib.Path(data["configuration_file"])
            with open(path) as f:
                raw = yaml.safe_load(f)
            return {"register_description": raw.get("RegisterDescription", {})}
        return data

    def get(self, key: str, default: Any = None) -> Any:
        return self.register_description.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.register_description[key] = value

    @classmethod
    def from_file(cls, configuration_file: pathlib.Path) -> "CameraConfig":
        return cls(configuration_file=configuration_file)
