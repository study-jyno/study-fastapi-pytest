from typing import Optional, List
from pydantic import BaseModel


class BaseItem(BaseModel):
    item_data: str


class ShowItem(BaseItem):
    id: int

    class Config:
        orm_mode = True


class UpdateItem(BaseItem):
    id: int


class CreateItem(BaseItem):
    pass


class BaseItemParent(BaseModel):
    data: str


class ShowItemParent(BaseItem):
    id: int

    class Config:
        orm_mode = True


class UpdateItemParent(BaseItem):
    id: int


class CreateItemParent(BaseItem):
    pass


class BaseItemChild(BaseModel):
    data: str


class ShowItemChild(BaseItem):
    id: int

    class Config:
        orm_mode = True


class UpdateItemChild(BaseItem):
    id: int


class CreateItemChild(BaseItem):
    pass
