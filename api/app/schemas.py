from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PromptBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)
    category: str = Field(min_length=1, max_length=50)
    tags: list[str] = []
    is_favorite: bool = False


class PromptCreate(PromptBase):
    pass


class PromptUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    body: str | None = Field(default=None, min_length=1)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    tags: list[str] | None = None
    is_favorite: bool | None = None


class TagRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class PromptRead(PromptBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagRead] = []
    model_config = ConfigDict(from_attributes=True)
