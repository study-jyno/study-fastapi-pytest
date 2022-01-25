from datetime import timedelta, datetime
from typing import Any, Dict, Optional, Union

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.item.schemas import CreateItem, UpdateItem
from app.item.schemas import CreateItemParent, UpdateItemParent
from app.item.schemas import CreateItemChild, UpdateItemChild
from app.item.models import Item, ItemChild, ItemParent
from app.service.base import ServiceBase


class ServiceItem(ServiceBase[Item, CreateItem, UpdateItem]):
    pass


class ServiceItemParent(ServiceBase[ItemParent, CreateItemParent, UpdateItemParent]):
    pass


class ServiceItemChild(ServiceBase[ItemChild, CreateItemChild, UpdateItemChild]):
    pass


service_item = ServiceItem(Item)
service_item_parent = ServiceItemParent(ItemParent)
service_item_child = ServiceItemChild(ItemChild)
