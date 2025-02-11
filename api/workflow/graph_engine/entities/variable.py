from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field
from enum import StrEnum

class VariableType(StrEnum):
    NUMBER = "number"
    STRING = "string"
    OBJECT = "object"
    SECRET = "secret"

    FILE = "file"

    ARRAY_ANY = "array[any]"
    ARRAY_STRING = "array[string]"
    ARRAY_NUMBER = "array[number]"
    ARRAY_OBJECT = "array[object]"
    ARRAY_FILE = "array[file]"

    NONE = "none"
    GROUP = "group"

class Variable(BaseModel):
    id: str = Field(
        default=lambda _: str(uuid4()),
        description="Unique identity for variable.",
    )
    name: str = Field(default="", description="Name of the variable.")
    description: str = Field(default="", description="Description of the variable.")
    optional: bool = Field(default=False, description="Whether the variable is optional.")
    selector: list[str] = Field(default_factory=list)
    value: Any = Field(default=None, description="Value of the variable.")
    type: VariableType = Field(default=VariableType.NONE, description="Type of the variable.")

    def __repr__(self):
        return f"Variable({self.name}, {self.value})"
