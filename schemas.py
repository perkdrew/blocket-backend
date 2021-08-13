from graphene_sqlalchemy import SQLAlchemyObjectType
from pydantic import BaseModel, EmailStr
from typing import Optional
from models import Advertisement
from enum import IntEnum


class SortEnum(IntEnum):
    """An enum for the two main types of sorting lists"""
    created_at = 0
    price = 1


class AdvertisementSchema(BaseModel):
    """An ad consists of a subject, a body, an optional price, and an email address."""
    subject: str
    body: str
    price: Optional[str]
    email: EmailStr


class AdvertisementModel(SQLAlchemyObjectType):
    class Meta:
        model = Advertisement
