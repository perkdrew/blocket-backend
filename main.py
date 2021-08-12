import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

import models
from db_conf import db_session
from schemas import AdvertisementModel, AdvertisementSchema, SortEnum

db = db_session.session_factory()

app = FastAPI()


class Query(graphene.ObjectType):
    all_advertisements = graphene.List(AdvertisementModel, sort=graphene.Int(required=False))
    advertisement_by_id = graphene.Field(AdvertisementModel, advertisement_id=graphene.Int(required=True))

    def resolve_all_advertisements(self, info: dict, sort: SortEnum = None):
        if sort == SortEnum.created_at:
            return db.query(models.Advertisement).order_by(models.Advertisement.created_at).all()
        elif sort == SortEnum.price:
            return db.query(models.Advertisement).order_by(models.Advertisement.price).all()
        else:
            return db.query(models.Advertisement).all()

    def resolve_advertisement_by_id(self, info: dict, advertisement_id: int):
        return db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()


class CreateNewAdvertisement(graphene.Mutation):
    class Arguments:
        subject = graphene.String(required=True)
        body = graphene.String(required=True)
        price = graphene.Float(required=False)
        email = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, subject: str, body: str, email: str, price: float = None):
        advertisement = AdvertisementSchema(
            subject=subject, body=body, price=price, email=email,
        )
        db_ad = models.Advertisement(
            subject=advertisement.subject,
            body=advertisement.body,
            price=advertisement.price,
            email=advertisement.email,
        )
        db.add(db_ad)
        db.commit()
        db.refresh(db_ad)
        return CreateNewAdvertisement(ok=True)


class DeleteAdvertisement(graphene.Mutation):
    class Arguments:
        advertisement_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, advertisement_id: int):
        db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).delete()
        db.commit()
        return DeleteAdvertisement(ok=True)


class AdvertisementMutations(graphene.ObjectType):
    create_new_advertisement = CreateNewAdvertisement.Field()
    delete_advertisement = DeleteAdvertisement.Field()


app.add_route(
    "/graphql",
    GraphQLApp(schema=graphene.Schema(mutation=AdvertisementMutations, query=Query)),
)
