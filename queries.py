import graphene

import models
from schemas import AdvertisementModel, SortEnum
from db_conf import db_session

db = db_session.session_factory()


class Query(graphene.ObjectType):
    all_advertisements = graphene.List(AdvertisementModel, sort=graphene.Int(required=False))
    advertisement_by_id = graphene.Field(AdvertisementModel, advertisement_id=graphene.Int(required=True))

    @staticmethod
    def resolve_all_advertisements(root, info: dict, sort: SortEnum = None):
        if sort == SortEnum.created_at:
            return db.query(models.Advertisement).order_by(models.Advertisement.created_at).all()
        elif sort == SortEnum.price:
            return db.query(models.Advertisement).order_by(models.Advertisement.price).all()
        else:
            return db.query(models.Advertisement).all()

    @staticmethod
    def resolve_advertisement_by_id(root, info: dict, advertisement_id: int):
        return db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
